import unittest
import sys 

from isca import GreyCodeBase, IscaCodeBase, DryCodeBase, GFDL_BASE

def test_grey_codebase():
    cb = GreyCodeBase.from_directory(GFDL_BASE)
    cb.compile('clean')
    return None

def test_isca_codebase():
    cb = IscaCodeBase.from_directory(GFDL_BASE)
    cb.compile()
    return None

def test_dry_codebase():
    cb = DryCodeBase.from_directory(GFDL_BASE)
    cb.compile()
    return None

if __name__ == '__main__':
    opt=sys.argv[1]
    print(opt)
    if opt == "grey":
        test_grey_codebase()
    elif opt == "isca":
        test_isca_codebase()
    elif opt == "dry":
        test_dry_codebase()
    else:
        print(f'opt: {opt} not found')
