from secrets import SCHED_API_KEY

import sys
import os

from urllib.parse import urlparse
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from sched_data_interface import SchedDataInterface

if __name__ == "__main__":
    data_interface = SchedDataInterface("https://bud20.sched.com", SCHED_API_KEY, "BUD20")
    sessions = data_interface.getSessionsData()
    for session in sessions.values():
        try:
            print("Files: " + str(session["files"]))
        except KeyError:
            pass
