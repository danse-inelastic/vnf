import sys

vinfo = sys.version_info

if vinfo[0] == 2:
    if vinfo[1] == 5:
        from safe_eval_25 import *
    elif vinfo[1] == 6:
        from safe_eval_26 import *
    else:
        raise NotImplementedError
else:
    raise NotImplementedError
