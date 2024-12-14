import os

import numpy as np

import argparse

from isca import GreyCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

parser = argparse.ArgumentParser()

parser.add_argument('--NCORES', 
                    default=32,
                    type=int)
parser.add_argument('--hroutput', 
                    default=False,
                    type=bool)
parser.add_argument('--carbon_conc', 
                    default=360.0,
                    type=float)
parser.add_argument('--rhbm', 
                    default=0.8,
                    type=float)
parser.add_argument('--tau_bm', 
                    default=7200.0,
                    type=float)
parser.add_argument('--resolution',
                    default='T42',
                    type=str)
parser.add_argument('--qflux_amp',
                    default=0.0,
                    type=float)
parser.add_argument('--warmpool_amp',
                    default=0.0,
                    type=float)
parser.add_argument('--expname',
                    default='WTagsNHctrl',
                    type=str)
parser.add_argument('--maxrun',
                    default=97,
                    type=int)
parser.add_argument('--restart_file',
                    default='None',
                    type=str)
parser.add_argument('--do_seasonal',
                    default=False,
                    type=bool)
parser.add_argument('--debugoutput',
                    default=False,
                    type=bool)
parser.add_argument('--convscheme',
                    default='SIMPLE_BETTS_MILLER',
                    type=str)

args = parser.parse_args()
print(args)

if args.qflux_amp==0.0:
    do_qflux=False
else:
    do_qflux=True

if args.warmpool_amp==0.0:
    do_warmpool=False
else:
    do_warmpool=True

#note default resolution is T42
NCORES = args.NCORES
print(NCORES)
if args.debugoutput:
    output_len = 5
else:
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

# create an Experiment object to handle the configuration of model parameters
# and output diagnostics
externalFieldTablePath='/home/rfajber/Isca/exp/RF/input/field_table'

exp = Experiment(args.expname,
                 codebase=cb,
                 externalFieldTablePath=externalFieldTablePath)

#Tell model how to write diagnostics
diag = DiagTable()
if args.hroutput:
    diag.add_file('atmos_4xday', 6)
if args.debugoutput:
    diag.add_file('atmos_monthly', 1, 'days', time_units='days')
else:
    diag.add_file('atmos_monthly', 30, 'days', time_units='days')

#Tell model which diagnostics to write
diag.add_field('dynamics', 'ps', time_avg=True)
diag.add_field('dynamics', 'bk')
diag.add_field('dynamics', 'pk')

# dynamics
diag.add_field('dynamics', 'ucomp', time_avg=True)
diag.add_field('dynamics', 'vcomp', time_avg=True)
diag.add_field('dynamics', 'omega',  time_avg=True) #wap
diag.add_field('dynamics', 'height', time_avg=True) #zg
diag.add_field('dynamics', 'temp', time_avg=True)
diag.add_field('dynamics', 'ucomp_sq', time_avg=True)
diag.add_field('dynamics', 'ucomp_vcomp', time_avg=True)
diag.add_field('dynamics', 'vcomp_sq', time_avg=True)
diag.add_field('dynamics', 'omega_sq', time_avg=True)
diag.add_field('atmosphere',   'flux_u', files=['atmos_monthly'], time_avg=True) #tauu - zonal component of stress
diag.add_field('atmosphere',   'flux_v', files=['atmos_monthly'], time_avg=True) #tauv

# surface and energy budget 
diag.add_field('mixed_layer', 't_surf', time_avg=True)
diag.add_field('mixed_layer', 'flux_lhe', time_avg=True)
diag.add_field('mixed_layer', 'flux_t', time_avg=True)
diag.add_field('two_stream','tdt_rad',time_avg=True)
diag.add_field('two_stream','tdt_solar',time_avg=True)
diag.add_field('two_stream','flux_lw',time_avg=True)
diag.add_field('two_stream','flux_sw',time_avg=True)

# moisture related
diag.add_field('atmosphere', 'precipitation', time_avg=True)
diag.add_field('atmosphere', 'condensation_rain', time_avg=True) #pr-pc
diag.add_field('atmosphere', 'dt_qg_condensation', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_convection', time_avg=True)
diag.add_field('atmosphere', 'dt_qg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'dt_tg_diffusion', time_avg=True)
diag.add_field('atmosphere', 'rh', time_avg=True)
diag.add_field('dynamics', 'sphum', time_avg=True)
diag.add_field('dynamics', 'sphum_v', time_avg=True)
diag.add_field('dynamics', 'sphum_w', time_avg=True)

# tag related 
for i in range(1,9):
    diag.add_field('dynamics', f'wtag{i}', time_avg=True)
    diag.add_field('dynamics', f'wtag{i}_v', time_avg=True)
    diag.add_field('dynamics', f'wtag{i}_w', time_avg=True)
    diag.add_field('atmosphere', f'wtag{i}_sink', time_avg=True)
    diag.add_field('atmosphere', f'wtag{i}_src', time_avg=True)

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
        'convection_scheme': args.convscheme, #Use the simple Betts Miller convection scheme from Frierson
    },

    'vert_turb_driver_nml': {
        'do_mellor_yamada': False,     # default: True
        'do_diffusivity': True,        # default: False
        'do_simple': True,             # default: False
        'constant_gust': 1.0,          # default: 1.0
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
        'do_qflux':do_qflux,
        'do_warmpool':do_warmpool,
    },

    'qflux_nml':{
        'qflux_amp':args.qflux_amp, 
        'warmpool_amp':args.warmpool_amp, 
    },

    'qe_moist_convection_nml': {
        'rhbm':args.rhbm,
        'Tmin':160.,
        'Tmax':350.,
        'tau_bm':args.tau_bm,   
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
        'rad_scheme': 'geen',            #Select radiation scheme to use, which in this case is Frierson
        'do_seasonal': args.do_seasonal,                #do_seasonal=false uses the p2 insolation profile from Frierson 2006. do_seasonal=True uses the GFDL astronomy module to calculate seasonally-varying insolation.
        'carbon_conc':args.carbon_conc,
    },

    # FMS Framework configuration
    'diag_manager_nml': {
        'mix_snapshot_average_fields': False  # time avg fields are labelled with time in middle of window
    },

    'fms_nml': {
        'domains_stack_size': 120000                        # default: 0
    },

    'fms_io_nml': {
        'threading_write': 'multi',                         # default: multi
        'fileset_write': 'multi',                           # default: multi
    },

    'spectral_dynamics_nml': {
        'damping_order': 8,             
        'damping_option': 'exponential_cutoff',
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

exp.set_resolution(args.resolution,numlevs)
overwrite=False

if __name__=="__main__":

    if args.restart_file=='None':
        exp.run(1,
                use_restart=False,
                num_cores=NCORES)
    else:
        restart_file=f'/project/def-rfajber/rfajber/RESTARTS/{args.restart_file}'
        exp.run(1,
                use_restart=True,
                restart_file=restart_file,
                num_cores=NCORES)
        
    for i in range(2,args.maxrun):
        exp.run(i, num_cores=NCORES)
