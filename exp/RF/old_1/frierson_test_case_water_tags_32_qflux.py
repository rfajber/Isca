import os

import numpy as np

from isca import GreyCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

########################################################################
# MUST CHECK THIS
########################################################################
expname='WtagsFrierson_BM_qflux'
########################################################################

#note default resolution is T42
NCORES = 32 
output_len = 30
base_dir = os.path.dirname(os.path.realpath(__file__))
# a CodeBase can be a directory on the computer,
# useful for iterative development
cb = GreyCodeBase.from_directory(GFDL_BASE)

gen_Frierson_levels=True
numlevs=30
if gen_Frierson_levels:
    z=np.linspace(0,1,numlevs+1)
    levs=np.exp(-5*(0.05*z+0.95*z**3))
    levs = levs[::-1]
    levs[0] = 0
    vert_coordinate_list=dict()
    vert_coordinate_list['bk']=list()
    vert_coordinate_list['pk']=list()
    for lev in levs:
        vert_coordinate_list['bk'].append(lev)
        vert_coordinate_list['pk'].append(0.0)

    print(vert_coordinate_list)
    print(len(levs))
# or it can point to a specific git repo and commit id.
# This method should ensure future, independent, reproducibility of results.
# cb = DryCodeBase.from_repo(repo='https://github.com/isca/isca', commit='isca1.1')

# compilation depends on computer specific settings.  The $GFDL_ENV
# environment variable is used to determine which `$GFDL_BASE/src/extra/env` file
# is used to load the correct compilers.  The env file is always loaded from
# $GFDL_BASE and not the checked out git repo.

cb.compile()  # compile the source code to working directory $GFDL_WORK/codebase

# create an Experiment object to handle the configuration of model parameters
# and output diagnostics
externalFieldTablePath='/home/rfajber/Isca/exp/RF/input/field_table'
exp = Experiment(expname, codebase=cb,
                 externalFieldTablePath=externalFieldTablePath)

#Tell model how to write diagnostics
diag = DiagTable()
#diag.add_file('atmos_4xday', 6)
diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_condensation', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_convection', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_diffusion', time_avg=True)
# diag.add_field('atmosphere', 'dt_qgp', time_avg=True)
# diag.add_field('atmosphere', 'dt_qgn', time_avg=True)
diag.add_field('atmosphere', 'rh', time_avg=True)
diag.add_field('mixed_layer', 't_surf', time_avg=True)
diag.add_field('mixed_layer', 'flux_lhe', time_avg=True)
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'temp', time_avg=True)
#diag.add_field('dynamics', 'vor', time_avg=True)
#diag.add_field('dynamics', 'div', time_avg=True)
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'wtag1', time_avg=True)
diag.add_field('dynamics', 'wtag2', time_avg=True)
diag.add_field('dynamics', 'wtag3', time_avg=True)
diag.add_field('dynamics', 'wtag4', time_avg=True)
diag.add_field('dynamics', 'wtag5', time_avg=True)
diag.add_field('dynamics', 'wtag6', time_avg=True)
diag.add_field('dynamics', 'wtag7', time_avg=True)
diag.add_field('dynamics', 'wtag8', time_avg=True)
diag.add_field('dynamics', 'sphum_v', time_avg=True)
diag.add_field('dynamics', 'wtag1_v', time_avg=True)
diag.add_field('dynamics', 'wtag2_v', time_avg=True)
diag.add_field('dynamics', 'wtag3_v', time_avg=True)
diag.add_field('dynamics', 'wtag4_v', time_avg=True)
diag.add_field('dynamics', 'wtag5_v', time_avg=True)
diag.add_field('dynamics', 'wtag6_v', time_avg=True)
diag.add_field('dynamics', 'wtag7_v', time_avg=True)
diag.add_field('dynamics', 'wtag8_v', time_avg=True)
diag.add_field('dynamics', 'sphum_w', time_avg=True)
diag.add_field('dynamics', 'wtag1_w', time_avg=True)
diag.add_field('dynamics', 'wtag2_w', time_avg=True)
diag.add_field('dynamics', 'wtag3_w', time_avg=True)
diag.add_field('dynamics', 'wtag4_w', time_avg=True)
diag.add_field('dynamics', 'wtag5_w', time_avg=True)
diag.add_field('dynamics', 'wtag6_w', time_avg=True)
diag.add_field('dynamics', 'wtag7_w', time_avg=True)
diag.add_field('dynamics', 'wtag8_w', time_avg=True)
diag.add_field('atmosphere', 'wtag1_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag2_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag3_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag4_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag5_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag6_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag7_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag8_sink', time_avg=True)
diag.add_field('atmosphere', 'wtag1_src', time_avg=True)
diag.add_field('atmosphere', 'wtag2_src', time_avg=True)
diag.add_field('atmosphere', 'wtag3_src', time_avg=True)
diag.add_field('atmosphere', 'wtag4_src', time_avg=True)
diag.add_field('atmosphere', 'wtag5_src', time_avg=True)
diag.add_field('atmosphere', 'wtag6_src', time_avg=True)
diag.add_field('atmosphere', 'wtag7_src', time_avg=True)
diag.add_field('atmosphere', 'wtag8_src', time_avg=True)

exp.diag_table = diag

#Empty the run directory ready to run
exp.clear_rundir()

#Define values for the 'core' namelist
exp.namelist = namelist = Namelist({
    'main_nml':{
     'days'   : output_len,
     'hours'  : 0,
     'minutes': 0,
     'seconds': 0,
     'dt_atmos':720,
     'current_date' : [1,1,1,0,0,0],
     'calendar' : 'thirty_day'
    },

    'idealized_moist_phys_nml': {
        'do_damping': True,
        'turb':True,
        'mixed_layer_bc':True,
        'do_virtual' :False,
        'do_simple': True,
        'roughness_mom':3.21e-05,
        'roughness_heat':3.21e-05,
        'roughness_moist':3.21e-05,                
        'two_stream_gray': True,     #Use grey radiation
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
        'water_tag': True,
    },

    #Use a large mixed-layer depth, and the Albedo of the CTRL case in Jucker & Gerber, 2017
    'mixed_layer_nml': {
        'tconst' : 285.,
        'prescribe_initial_dist':True,
        'evaporation':True,   
        'depth': 2.5,                          #Depth of mixed layer used
        'albedo_value': 0.31,                  #Albedo value used             
        'do_qflux': True        
    },

    'qe_moist_convection_nml': {
        'rhbm':0.7,
        'Tmin':160.,
        'Tmax':350.   
    },

    'betts_miller_nml': {
       'rhbm': .8   , 
       'do_simp': False, 
       'do_shallower': True, 
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
        'trayfric': -0.25,              # neg. value: time in *days8
        'sponge_pbottom':  5000.,           #Bottom of the model's sponge down to 50hPa (units are Pa)
        'do_conserve_energy': True,             
    },

    'two_stream_gray_rad_nml': {
        'rad_scheme': 'frierson',            #Select radiation scheme to use, which in this case is Frierson
        'do_seasonal': False,                #do_seasonal=false uses the p2 insolation profile from Frierson 2006. do_seasonal=True uses the GFDL astronomy module to calculate seasonally-varying insolation.
        'atm_abs': 0.2,                      # default: 0.0        
    },

    # FMS Framework configuration
    'diag_manager_nml': {
        'mix_snapshot_average_fields': False  # time avg fields are labelled with time in middle of window
    },

    'fms_nml': {
        'domains_stack_size': 12000000                        # default: 0
    },

    'fms_io_nml': {
        'threading_write': 'single',                         # default: multi
        'fileset_write': 'single',                           # default: multi
    },

    'spectral_dynamics_nml': {
        'damping_order': 8,             
#        'damping_option': 'exponential_cutoff',
        'water_correction_limit': 200.e2,
        'reference_sea_level_press':1.0e5,
        'valid_range_t':[100.,800.],
        'initial_sphum':[2.e-6],
        'vert_coord_option':'input', #Use the vertical levels from Frierson 2006
        'surf_res':0.5,
        'scale_heights' : 11.0,
        'exponent':7.0,
        'robert_coeff':0.03,
        },

    'vert_coordinate_nml': vert_coordinate_list,

})

exp.set_resolution('T85',numlevs)
overwrite=False
# start from something already spun up so that we only have to spinup the tags, which should be ~30 days ish
# this is good for diagnosing tendencies
restart_file='/home/rfajber/restarts_save/A3.year5.nc'
#Lets do a run!
if __name__=="__main__":
    exp.run(1, use_restart=False, num_cores=NCORES)
    for i in range(2,100):
        exp.run(i, num_cores=NCORES)
