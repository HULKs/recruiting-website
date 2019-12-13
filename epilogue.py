import json
import sys

__app_response__["stdout"] = sys.stdout.getvalue()
__original_stdout__.write(json.dumps(__app_response__))
