from secrets import SCHED_API_KEY

import sys
import os

from urllib.parse import urlparse
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from sched_data_interface import SchedDataInterface

if __name__ == "__main__":
    data_interface = SchedDataInterface("https://linaroconnectsandiego.sched.com", SCHED_API_KEY, "SAN19")
    sessions = data_interface.getSessionsData()
    print(sessions)
