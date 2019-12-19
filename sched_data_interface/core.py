
from secrets import SCHED_API_KEY
import re
import requests

class SchedDataInterface:

    def __init__(self, sched_url, sched_api_key):
        self.sched_url = sched_url
        self.API_KEY = sched_api_key
        self._verbose = False
        # Blacklisted tracks to ignore when creating pages/resources.json
        self.blacklistedTracks = ["Food & Beverage", "Informational"]

    def purge_misc_sessions(self, data):
        for entry in data:
            # Get the title of the session - to retrieve the session ID.
            session_title = entry["name"]
            # Fetch the main session track.
            try:
                session_track = entry["event_type"]
            except Exception as e:
                if self._verbose:
                    print(e)
                data.pop(entry)
            # Check the current track is not in the blacklisted tracks
            if session_track not in self.blacklistedTracks:
                # Get the session id from the title
                try:
                    # Compile the session ID regex
                    session_id_regex = re.compile(
                        '{}-[A-Za-z]*[0-9]+K*[0-9]*'.format(self.connect_code.upper()))
                    # Get the first item found based on the regex
                    session_id = session_id_regex.findall(session_title)[0]
                    entry["session_id"] = session_id
                # If no session ID exists then skip the session and output a warning
                except Exception as e:
                    data.pop(entry)

    def getExportData(self):
        """Gets the export data from sched"""
        export_data = self.get_api_results(
            "/api/session/export?api_key={0}&format=json&fields=event_key,event_type,active,name,id,files,speakers")
        return export_data

    def get_api_results(self, endpoint):
        """
            Gets the results from a specified endpoint
        """
        endpoint = self.sched_url + endpoint.format(self.API_KEY)
        if self._verbose:
            print("Fetch data from: {} ".format(endpoint))
        try:
            resp = requests.get(url=endpoint)
            data = resp.json()
            return data
        except Exception as e:
            print(e)
            return False



if __name__ == "__main__":
    sched_data = SchedDataInterface("https://linaroconnectsandiego.sched.com", SCHED_API_KEY)
