from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

cb = IscaCodeBase.from_directory(GFDL_BASE)
#cb.compile_flags.append('-DRRTM_NO_COMPILE')
#cb.log.info('RRTM compilation disabled.')
cb.compile(debug=True)
