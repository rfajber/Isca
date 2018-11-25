from isca import IscaCodeBase, DiagTable, Experiment, Namelist, GFDL_BASE

cb = IscaCodeBase.from_directory(GFDL_BASE)

cb.compile(debug=True)
