__version__ = '1.0'

import sys
if "xray" in sys.argv[0]:
    run_type = 'xray'
else:
    run_type = 'v2ray'

from .util_core.trans import _