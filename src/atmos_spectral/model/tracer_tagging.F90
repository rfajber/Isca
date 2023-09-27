module tracer_tagging

    use transforms_mod, only: get_sin_lat, get_deg_lat

    use spectral_dynamics_mod, only: get_axis_id

    use time_manager_mod, only: time_type

    use diag_manager_mod, only: register_diag_field, send_data

    use tracer_manager_mod, only: get_tracer_names

    use  field_manager_mod, only: MODEL_ATMOS

    use constants_mod, only: grav

    implicit none

    private
    !=================================================================================================================================
    
    character(len=128) :: version= &
    '$Id: Tracer Tagging Module $'
    
    character(len=128) :: tagname= &
    '$Name:  $'
    character(len=10), parameter :: mod_name='atmosphere'
    
    !=================================================================================================================================

    public :: tagged_tracers_init, water_tagged_tendencies, water_tagged_tendency_update, water_tagged_tendency_update_surf, tagged_tracers_end, water_tagged_tendencies_reset, tagged_tracers_diag,  water_tagged_tracer_finish
    
    logical :: water_tag = .true.

    integer :: num_tag0, num_tag1

    real, parameter :: a_small_number = 1.0e-6

    real, dimension(:,:,:), allocatable :: dt_qgp, dt_qgp_cond, dt_qgp_conv, dt_qgp_diff
    real, dimension(:,:,:), allocatable :: dt_qgn, dt_qgn_cond, dt_qgn_conv, dt_qgn_diff

    real, allocatable, dimension(:,:,:,:) :: tracer_mask
    real, allocatable, dimension(:,:,:,:) :: sink, src
!    real, dimension(5) :: sn = (/-1.0, -0.5, 0.0, 0.5, 1.0/)
    real, dimension(9) :: ln = (/-90., -48.5904, -30., -14.4775, 0.0, 14.4775, 30., 48.5904, 90./)
    !real, dimension(5) :: ln = (/-90., -30., 0.0, 30., 90./)
    real, dimension(:), allocatable :: deg_lat
    integer :: is,ie,js,je,nsphum,num_levels,num_tracers,j,ntr

    integer, dimension(:), allocatable :: id_tr_sink, id_tr_src
    integer :: id_dt_qgp
    integer :: id_dt_qgn
    real,dimension(:,:,:), allocatable :: dt_qgp_temp, dt_qgn_temp
    
    contains

    !=================================================================================================================================

    subroutine tagged_tracers_init(is_in,ie_in,js_in,je_in,num_levels_in,num_tracers_in,Time)
        !input dimensions 
        integer, intent(in) :: is_in,ie_in,js_in,je_in,num_levels_in,num_tracers_in
        !diagnostic variables 
        integer, dimension(4) :: axes
        type(time_type), intent(in) :: Time
        !real, allocatable, dimension(:,:,:,:):: 
        
        !RFTT
        character(len=128) :: tname, longname, units

        ! don't want to have to keep passing these, so store internal copies
        ! all are integers, so cost is trivial
        is = is_in
        ie = ie_in
        js = js_in
        je = je_in
        num_levels = num_levels_in
        num_tracers = num_tracers_in

        ! allocate variables 
        allocate(dt_qgp_temp (is:ie,js:je,num_levels) )
        allocate(dt_qgn_temp (is:ie,js:je,num_levels) )
        allocate(tracer_mask (is:ie,js:je,num_levels,num_tracers))
        allocate(sink (is:ie,js:je,num_levels,num_tracers))
        allocate(src (is:ie,js:je,num_levels,num_tracers))

        allocate(deg_lat(js:je))
        call get_deg_lat(deg_lat)

        allocate(id_tr_sink(num_tracers))
        allocate(id_tr_src(num_tracers))

        ! initialize variables
        dt_qgp=0.
        dt_qgn=0.
        dt_qgp_conv=0.
        dt_qgn_conv=0.
        dt_qgp_cond=0.
        dt_qgn_cond=0.
        dt_qgp_diff=0.
        dt_qgn_diff=0.
        dt_qgp_temp=0.
        dt_qgn_temp=0.

        ! initialize outputs
        axes = get_axis_id()
        id_dt_qgp = register_diag_field(mod_name,'dt_qgp', &
        axes(1:3), Time , 'dt_qgp', 'kg/kg/s')
        id_dt_qgn = register_diag_field(mod_name,'dt_qgn', &
        axes(1:3), Time , 'dt_qgn', 'kg/kg/s')

        tracer_mask=0.0
        ! don't bother updating water vapor
        !tracer_mask(:,:,:,1) = 1.0
        do ntr=2,num_tracers
          do j = js, je
            if ( (deg_lat(j) .gt. ln(ntr-1)) .and. (deg_lat(j) .le. ln(ntr)) ) then
                tracer_mask(:,j,:,ntr) = 1.0
            end if
          end do     
        end do

    axes = get_axis_id()
    do ntr=1,num_tracers
        call get_tracer_names(MODEL_ATMOS, ntr, tname, longname, units)
        id_tr_sink(ntr) = register_diag_field(mod_name, trim(tname)//trim('_sink'), axes(1:3), Time, trim(longname)//trim(' sink'), trim(units)//trim('/s')) 
        id_tr_src(ntr) =  register_diag_field(mod_name, trim(tname)//trim('_src'),  axes(1:3), Time, trim(longname)//trim(' src'),  trim(units)//trim('/s')) 
    enddo        

    print*, 'finished tracer tagging intialization'

    return

    end subroutine tagged_tracers_init

    !=================================================================================================================================
!        conv_dt_qg,& ! tendency from convection
!        cond_dt_qg,& ! tendency from condensation
    subroutine water_tagged_tendencies(&
        phys_dt_qg,&
        grid_tracers, &! grid tags
        Time,&
        flux_q,&
        bottom_layer_mass,&
        dt_tracers& ! grid tracer tendency
        )     

        ! variable declaration
        real, intent(in), dimension(:,:,:) :: phys_dt_qg
        real, intent(in), dimension(:,:,:,:) :: grid_tracers ! note shape is different because we're only using 1 time level
        type(time_type), intent(in) :: Time
        real, intent(in), dimension(:,:) :: flux_q
        real, intent(in), dimension(:,:) :: bottom_layer_mass
        real, intent(inout), dimension(:,:,:,:) :: dt_tracers
        logical :: used
        
        do ntr=2,num_tracers

            sink(:,:,:,ntr) = 0.0
            src(:,:,:,ntr) = 0.0
    
            where(phys_dt_qg .gt. 0)
                src(:,:,:,ntr) = src(:,:,:,ntr) + phys_dt_qg * &
                tracer_mask(:,:,:,ntr)
            elsewhere
                sink(:,:,:,ntr) = sink(:,:,:,ntr) + phys_dt_qg * &
                grid_tracers(:,:,:,ntr) / (grid_tracers(:,:,:,nsphum) + a_small_number)
            endwhere

            where(flux_q .gt. 0)
                src(:,:,num_levels,ntr) = src(:,:,num_levels,ntr) + flux_q/bottom_layer_mass * &
                tracer_mask(:,:,num_levels,ntr)
            elsewhere
                sink(:,:,num_levels,ntr) = sink(:,:,num_levels,ntr) + flux_q/bottom_layer_mass * &
                grid_tracers(:,:,num_levels,ntr) / (grid_tracers(:,:,num_levels,nsphum) + a_small_number)
            endwhere
            
            dt_tracers(:,:,:,ntr) = src(:,:,:,ntr) + sink(:,:,:,ntr)

        enddo

        do ntr=2,num_tracers
            if(id_tr_sink(ntr) > 0) used = send_data(id_tr_sink(ntr), sink(:,:,:,ntr), Time)
            if(id_tr_src(ntr) > 0) used = send_data(id_tr_src(ntr), src(:,:,:,ntr), Time)
        end do
   
        return

    end subroutine water_tagged_tendencies
    !=================================================================================================================================
    subroutine water_tagged_tendencies_reset()

        sink = sink * 0.0
        src = src * 0.0 

        return  

    end subroutine water_tagged_tendencies_reset
    !=================================================================================================================================
    subroutine water_tagged_tendency_update(tendency,grid_tracers)

        real,intent(in),dimension(:,:,:) :: tendency
        real,intent(in),dimension(:,:,:,:) :: grid_tracers
!        real,intent(inout),dimension(:,:,:,:) :: dt_tracers

        ! where(tendency .gt. 0.0)
        !     dt_qgp_temp = tendency
        ! elsewhere
        !     dt_qgn_temp = tendency
        ! end where

        do ntr=2,num_tracers
            ! where (tendency .ge. 0)
            !     src(:,:,:,ntr) = src(:,:,:,ntr) + tendency * tracer_mask(:,:,:,ntr)
            ! endwhere
            ! where (tendency .lt. 0)
            !     sink(:,:,:,ntr) = sink(:,:,:,ntr) + tendency * grid_tracers(:,:,:,ntr) / (grid_tracers(:,:,:,nsphum) + a_small_number)
            ! endwhere
            sink(:,:,:,ntr) = sink(:,:,:,ntr) + tendency &
            * grid_tracers(:,:,:,ntr) / (grid_tracers(:,:,:,nsphum) + a_small_number)
        end do
    
!        spread(dt_qgn_temp,4,num_tracers)

!        sink = sink + spread(dt_qgn_temp,4,num_tracers) * grid_tracers &
!        / ( spread(grid_tracers(:,:,:,nsphum),4,num_tracers) + 1e-6)

!        sink = sink + spread(tendency,4,num_tracers)

!        sink = sink + spread(dt_qgn_temp,4,num_tracers) * grid_tracers &
!        / ( spread(grid_tracers(:,:,:,nsphum),4,num_tracers) + 1e-6)
    
 !       src = src + tracer_mask * spread(dt_qgp_temp,4,num_tracers)
    
 !       dt_tracers(:,:,:,2:num_tracers) = dt_tracers(:,:,:,2:num_tracers)+&
 !       src(:,:,:,2:num_tracers) + sink(:,:,:,2:num_tracers)

!        print *, 'update main'
        
        return 

    end subroutine water_tagged_tendency_update
    !=================================================================================================================================
    subroutine water_tagged_tendency_update_surf(surf_flux,grid_tracers,bottom_layer_mass)

        real,intent(in),dimension(:,:) :: surf_flux
        real,intent(in),dimension(:,:,:,:) :: grid_tracers
!        real,intent(inout),dimension(:,:,:,:) :: dt_tracers
        real,intent(in), dimension(:,:) :: bottom_layer_mass

        do ntr=2,num_tracers
            ! where (surf_flux .ge. 0)
            !     src(:,:,num_levels,ntr) = src(:,:,num_levels,ntr) + &
            !     surf_flux/bottom_layer_mass * tracer_mask(:,:,num_levels,ntr)
            ! endwhere
            ! where (surf_flux .lt. 0)
            !     sink(:,:,num_levels,ntr) = sink(:,:,num_levels,ntr) + &
            !     surf_flux/bottom_layer_mass * grid_tracers(:,:,num_levels,ntr) / (grid_tracers(:,:,num_levels,nsphum) + a_small_number)
            ! endwhere
            src(:,:,num_levels,ntr) = src(:,:,num_levels,ntr) + &
            surf_flux/bottom_layer_mass * tracer_mask(:,:,num_levels,ntr)
    end do


        ! where(surf_flux .gt. 0)
        !     dt_qgp_temp(:,:,num_levels) = 
        ! elsewhere
        !     dt_qgn_temp(:,:,num_levels) = surf_flux/bottom_layer_mass
        ! end where

        ! sink(:,:,num_levels,:) = sink(:,:,num_levels,:) + spread(dt_qgn_temp(:,:,num_levels),3,num_tracers) * grid_tracers(:,:,num_levels,:) &
        ! / ( spread(grid_tracers(:,:,num_levels,nsphum),3,num_tracers) + 1e-6) 
    
        ! src(:,:,num_levels,:) = src(:,:,num_levels,:) + tracer_mask(:,:,num_levels,:) * spread(dt_qgp_temp(:,:,num_levels),3,num_tracers)
    
!        dt_tracers(:,:,num_levels,2:num_tracers) = dt_tracers(:,:,num_levels,2:num_tracers)+&
!        src(:,:,num_levels,2:num_tracers) + sink(:,:,num_levels,2:num_tracers)

!        print *, 'update surf'

        return

    end subroutine water_tagged_tendency_update_surf    
    !=================================================================================================================================

    !=================================================================================================================================
    subroutine water_tagged_tracer_finish(dt_tracers,Time) 

        logical :: used 
        type(time_type), intent(in) :: Time
        real, intent(inout), dimension(:,:,:,:) :: dt_tracers

        do ntr=2,num_tracers
            dt_tracers(:,:,:,ntr) = dt_tracers(:,:,:,ntr) + sink(:,:,:,ntr) + src(:,:,:,ntr) 
            if(id_tr_sink(ntr) > 0) used = send_data(id_tr_sink(ntr), sink(:,:,:,ntr), Time)
            if(id_tr_src(ntr) > 0) used = send_data(id_tr_src(ntr), src(:,:,:,ntr), Time)
        end do

        return 

    end subroutine water_tagged_tracer_finish
    !=================================================================================================================================

    subroutine tagged_tracers_diag(Time)

        logical :: used 
        type(time_type), intent(in) :: Time

        do ntr=2,num_tracers
            if(id_tr_sink(ntr) > 0) used = send_data(id_tr_sink(ntr), sink(:,:,:,ntr), Time)
            if(id_tr_src(ntr) > 0) used = send_data(id_tr_src(ntr), src(:,:,:,ntr), Time)
        end do

        return

    end subroutine tagged_tracers_diag
    !=================================================================================================================================
    subroutine tagged_tracers_end

        deallocate(dt_qgp_temp )
        deallocate(dt_qgn_temp )
        deallocate(tracer_mask )
        deallocate(sink)
        deallocate(src)
        deallocate(deg_lat)
        deallocate(id_tr_sink)
        deallocate(id_tr_src)
    
        return 

    end subroutine tagged_tracers_end 
    !=================================================================================================================================
end module tracer_tagging