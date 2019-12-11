import json
import sys

__app_response__["stdout"] = sys.stdout.getvalue()[:100000]
__original_stdout__.write(json.dumps(__app_response__))
