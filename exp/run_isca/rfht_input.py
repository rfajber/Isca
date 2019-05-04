import os
import sys 
import numpy as np
from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

NCORES = 8
base_dir = os.path.dirname(os.path.realpath(__file__))
# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = IscaCodeBase.from_directory(GFDL_BASE)

exp_name='def_dt150_spec_T85'
cold_restart=True
i0=1
i1=21
carbon_conc=360.0
tau_bm=7200.0
rrtm_option=False #note must have rrtm_option = ~ two_stream_option
two_stream_option=not rrtm_option 
radiation_scheme='geen'
transport_diag=False
res=85
dt_atmos=150.0
output_length=25
use_external_restart=False
spinup_restart=False

f=open(sys.argv[1])
for line in f.read().split('\n'):
    exec line

if res==85:
    num_fourier=85 #Number of Fourier modes
    num_spherical=86 #Number of spherical harmonics in triangular truncation
    lon_max=256 #Lon grid points
    lat_max=128 #Lat grid points

if res==42:
    num_fourier=42 #Number of Fourier modes
    num_spherical=43 #Number of spherical harmonics in triangular truncation
    lon_max=128 #Lon grid points
    lat_max=64 #Lat grid points
    
# or it can point to a specific git repo and commit id.
# This method should ensure future, independent, reproducibility of results.
# cb = DryCodeBase.from_repo(repo='https://github.com/isca/isca', commit='isca1.1')

# compilation depends on computer specific settings.  The $GFDL_ENV
# environment variable is used to determine which `$GFDL_BASE/src/extra/env` file
# is used to load the correct compilers.  The env file is always loaded from
# $GFDL_BASE and not the checked out git repo.

#cb.compile()  # compile the source code to working directory $GFDL_WORK/codebase

# create an Experiment object to handle the configuration of model parameters
# and output diagnostics
exp = Experiment(exp_name, codebase=cb)

#RF - by default this points the field_table to srcdir/extra/model
#     this line sets the field table to be in the input_dir
#field_table_file='field_table_fv'
#exp.field_table_file=os.getcwd()+'/input/'+field_table_file

#Tell model how to write diagnostics
diag = DiagTable()
diag.add_file('4xday', 6, 'hours', time_units='days')

#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'omega', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('mixed_layer','t_surf', time_avg=True)
diag.add_field('mixed_layer','flux_t',time_avg=True)
diag.add_field('mixed_layer','flux_lhe',time_avg=True)
diag.add_field('atmosphere','precipitation', time_avg=True)
if two_stream_option:
    diag.add_field('two_stream','swdn_sfc',time_avg=True)
    diag.add_field('two_stream','lwdn_sfc',time_avg=True)
    diag.add_field('two_stream','lwup_sfc',time_avg=True)
    diag.add_field('two_stream','swdn_toa',time_avg=True)
    diag.add_field('two_stream','olr',time_avg=True)
if rrtm_option:
    diag.add_field('rrtm_radiation','olr',time_avg=True)
    diag.add_field('rrtm_radiation','toa_sw',time_avg=True)
    diag.add_field('rrtm_radiation','flux_sw',time_avg=True)
    diag.add_field('rrtm_radiation','flux_lw',time_avg=True)
diag.add_field('vert_turb','z_pbl',time_avg=True)
diag.add_field('atmosphere', 'theta', time_avg=True)
diag.add_field('dynamics','tag_O_cond',time_avg=True)
diag.add_field('dynamics','tag_O_conv',time_avg=True)
diag.add_field('dynamics','tag_O_diff',time_avg=True)
diag.add_field('dynamics','tag_O_radi',time_avg=True)
diag.add_field('atmosphere','dt_tgp_cond',time_avg=True)
diag.add_field('atmosphere','dt_tgp_conv',time_avg=True)
diag.add_field('atmosphere','dt_tgp_diff',time_avg=True)
diag.add_field('atmosphere','dt_tgp_radi',time_avg=True)
diag.add_field('atmosphere','dt_tgn_cond',time_avg=True)
diag.add_field('atmosphere','dt_tgn_conv',time_avg=True)
diag.add_field('atmosphere','dt_tgn_diff',time_avg=True)
diag.add_field('atmosphere','dt_tgn_radi',time_avg=True)
if transport_diag:
    diag.add_field('dynamics', 'sphum_v', time_avg=True)
    diag.add_field('dynamics', 'sphum_w', time_avg=True)
    diag.add_field('dynamics','tag_O_cond_v',time_avg=True)
    diag.add_field('dynamics','tag_O_conv_v',time_avg=True)
    diag.add_field('dynamics','tag_O_diff_v',time_avg=True)
    diag.add_field('dynamics','tag_O_radi_v',time_avg=True)
    diag.add_field('dynamics','tag_O_cond_w',time_avg=True)
    diag.add_field('dynamics','tag_O_conv_w',time_avg=True)
    diag.add_field('dynamics','tag_O_diff_w',time_avg=True)
    diag.add_field('dynamics','tag_O_radi_w',time_avg=True)

exp.diag_table = diag

#Empty the run directory ready to run
exp.clear_rundir()

#Define values for the 'core' namelist
exp.namelist = namelist = Namelist({
    'main_nml':{
     'days'   : output_length,
     'hours'  : 0,
     'minutes': 0,
     'seconds': 0,
     'dt_atmos':dt_atmos,
     'current_date' : [1,1,1,0,0,0],
      'calendar' : 'thirty_day',
    },

    'idealized_moist_phys_nml': {
        'do_damping': False,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual' :False,
        'do_simple': True,
        'roughness_mom':3.21e-05,
        'roughness_heat':3.21e-05,
        'roughness_moist':3.21e-05,                
        'two_stream_gray': two_stream_option,     #Use grey radiation
        'do_rrtm_radiation': rrtm_option,
        'convection_scheme': 'SIMPLE_BETTS_MILLER', #Use the simple Betts Miller convection scheme from Frierson
    },

    'vert_turb_driver_nml': {
        'do_mellor_yamada': False,     # default: True
        'do_diffusivity': True,        # default: False
        'do_simple': True,             # default: False
        'constant_gust': 0.0,          # default: 1.0
        'use_tau': False
    },
    
    'diffusivity_nml': {
        'do_entrain':False,
        'do_simple': True,
    },

    'surface_flux_nml': {
        'use_virtual_temp': False,
        'do_simple': True,
        'old_dtaudv': True    
    },

    'atmosphere_nml': {
        'idealized_moist_model': True,
        'heat_tag': True,
        'spinup_restart':spinup_restart
    },

    #Use a large mixed-layer depth, and the Albedo of the CTRL case in Jucker & Gerber, 2017
    'mixed_layer_nml': {
        'tconst' : 285.,
        'prescribe_initial_dist':True,
        'evaporation':True,   
        'depth': 2.5,                          #Depth of mixed layer used
        'albedo_value': 0.31,                  #Albedo value used             
    },

    'qe_moist_convection_nml': {
        'rhbm':0.7,
        'Tmin':160.,
        'Tmax':350.,
        'tau_bm':tau_bm, 
    },

    'betts_miller_nml': {
       'rhbm': .7   , 
       'do_simp': False, 
       'do_shallower': True,
#        'tau_bm': 1800.
    },
    
    'lscale_cond_nml': {
        'do_simple':True,
        'do_evap':False
    },
    
    'sat_vapor_pres_nml': {
        'do_simple':True
    },
    
    'damping_driver_nml': {
        'do_rayleigh': True,
        'trayfric': -0.25,              # neg. value: time in *days*
        'sponge_pbottom':  5000.,           #Bottom of the model's sponge down to 50hPa (units are Pa)
        'do_conserve_energy': True,             
    },

    'two_stream_gray_rad_nml': {
        'rad_scheme': radiation_scheme,            #Select radiation scheme to use, which in this case is Frierson'
        'do_seasonal': False,                #do_seasonal=false uses the p2 insolation profile from Frierson 2006. do_seasonal=True uses the GFDL astronomy module to calculate seasonally-varying insolation.
        'atm_abs': 0.2,                      # default: 0.0
        'carbon_conc': carbon_conc
    },

    # FMS Framework configuration
    'diag_manager_nml': {
        'mix_snapshot_average_fields': False  # time avg fields are labelled with time in middle of window
    },

    'fms_nml': {
        'domains_stack_size': 600000                        # default: 0
    },

    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    },

    'spectral_dynamics_nml': {
        'damping_order': 4,             
        'water_correction_limit': 200.e2,
        'reference_sea_level_press':1.0e5,
        'num_levels':30,               #How many model pressure levels to use
        'num_fourier':  num_fourier, #Number of Fourier modes
        'num_spherical':  num_spherical, #Number of spherical harmonics in triangular truncation
        'lon_max':  lon_max, #Lon grid points
        'lat_max':  lat_max, #Lat grid points
        'valid_range_t':[100.,800.],
        'initial_sphum':[2.e-6],
#        'vert_coord_option':'input', #Use the vertical levels from Frierson 2006
        'surf_res':0.5,
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03
    },
#    'vert_coordinate_nml': {
#        'bk': [0.000000, 0.0117665, 0.0196679, 0.0315244, 0.0485411, 0.0719344, 0.1027829, 0.1418581, 0.1894648, 0.2453219, 0.3085103, 0.3775033, 0.4502789, 0.5244989, 0.5977253, 0.6676441, 0.7322627, 0.7900587, 0.8400683, 0.8819111, 0.9157609, 0.9422770, 0.9625127, 0.9778177, 0.9897489, 1.0000000],
#        'pk': [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
#       }
})

#Lets do a run!
if __name__=="__main__":
    if cold_restart:
        exp.run(1, use_restart=False, num_cores=NCORES)
        for i in range(2,i1):
            exp.run(i, num_cores=NCORES)
    else:
        for i in range(i0,i1):
	    exp.run(i,num_cores=NCORES)
#                if use_external_restart and i==i0:
#                exp.run(i,num_cores=NCORES,restart_file=external_restart_file)
#            else:
            

