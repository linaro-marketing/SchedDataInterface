import re
import requests

class SchedDataInterface:

    def __init__(self, sched_url, sched_api_key, connect_code):
        self.sched_url = sched_url
        self.connect_code = connect_code
        self.API_KEY = sched_api_key
        self._verbose = False
        # Blacklisted tracks to ignore when creating pages/resources.json
        self.blacklistedTracks = ["Food & Beverage", "Informational"]
        self.users_data = self.getUsersData()

    def getDetailedSpeakers(self, speakers):
        """Get's additional information about a speaker"""
        new_speakers = []
        try:
            for speaker in speakers:
                for user in self.users_data:
                    if speaker["username"] == user["username"]:
                        new_speakers.append(user)
            return new_speakers
        except KeyError as e:
            print(e)
            return "Invalid"


    def getUsersData(self):
        """Get's the users data from sched"""
        users_data = self.get_api_results(
            "/api/user/list?fields=id,username,name,phone,email,url,about,role,joined,lastactive,avatar,company,position,location&api_key={0}&format=json")
        return users_data

    def purge_misc_sessions(self, data):
        formatted_data = {}
        for entry in data:
            try:
                speakers = entry["speakers"]
            except Exception as e:
                speakers = None
            if speakers != None:
                speakers = self.getDetailedSpeakers(speakers)
                entry["speakers"] = speakers
            # Get the title of the session - to retrieve the session ID.
            session_title = entry["name"]
            # Fetch the main session track.
            try:
                session_track = entry["event_type"]
            except Exception:
                pass
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
                    # Add new entry to dictionary
                    formatted_data[session_id] = entry
                # If no session ID exists then skip the session and output a warning
                except Exception:
                    pass
        return formatted_data

    def getSessionsData(self):
        """Gets the export data from sched"""
        export_data = self.get_api_results(
            "/api/session/export?api_key={0}&format=json&fields=event_key,event_type,active,name,id,files,speakers")
        export_data = self.purge_misc_sessions(export_data)
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

# if __name__ == "__main__":
#     sched_data = SchedDataInterface("https://linaroconnectsandiego.sched.com", SCHED_API_KEY, "SAN19")
#     export_data = sched_data.getExportData()
#     # Do something for one session
#     print(export_data["SAN19-101"])
#     # Do Something for all sessions
#     for entry in export_data.values():
#         print(entry["session_id"])
