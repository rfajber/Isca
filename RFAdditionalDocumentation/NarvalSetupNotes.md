# SETUP notes

Note, right now this only works with the intel compiler. Is that a problem for AMD nodes? Hopefully not?

## Python
- Needs to be configured using python 3.9, this can be done using the file in Isca/ci
- Have to set sh to 1.9 using pip, currently a bug with sh>2. can do this with pip install sh==1.9
- this should be fixed now, but if you get a stdoutput error that might be it.

## narval specific files 
- set GFDL_ENV to narval.ifort
- Isca/src/extra/env/narval.ifort 
- Isca/src/extra/python/isca/templates/mkmft.template.narval.ifort 

## environment file 
- GFDL_ENV sets the name of the environment file
- contains the commands to load the module
- sets the name of the template to use
- stored in Isca/src/extra/env/

## templates
- for some reason the ones in Isca/bin are fake 
- have to set includes manually,$EBROOTGENTOO corresponds to equivalent of /usr
- have to add flexiblas to library flags 

## flexiblas 
- by default on narval uses blis, maybe worth configuring manually in the future?