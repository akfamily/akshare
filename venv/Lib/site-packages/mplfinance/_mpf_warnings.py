import sys as __sys
if not __sys.warnoptions:
    import os as __os
    import warnings as __warnings
    __warnings.filterwarnings("default",category=DeprecationWarning,module='mplfinance') # Change the filter in this process
    __os.environ["PYTHONWARNINGS"] = "default::DeprecationWarning:mplfinance"            # Also affect subprocesses

if __sys.version_info <= (3, 6):
    __warnings.filterwarnings("default",category=ImportWarning,module='mplfinance')   # Change the filter in this process
    __os.environ["PYTHONWARNINGS"] = "default::ImportWarning:mplfinance"              # Also affect subprocesses
    __warnings.warn('\n\n ================================================================= '+
                    '\n\n    WARNING: `mplfinance` is NOT supported for Python versions '+
                    '\n               less than 3.6'
                    '\n\n ================================================================= ',
                    category=ImportWarning)

