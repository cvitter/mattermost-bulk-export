import json
from datetime import datetime 
import database_functions


def read_config():
    """
    Read the config.json file and populate global variables
    """
    global db_url, db_name, db_username, db_password
    global team_list, export_inactive_users, export_direct_messages

    with open('config.json') as config_file:
        d = json.loads(config_file.read())
        
    db_url = d["database"]["url"]
    db_name = d["database"]["database"]
    db_username = d["database"]["user"]
    db_password = d["database"]["password"]
    team_list = d["actions"]["export_team_list"]
    export_inactive_users = d["actions"]["export_inactive_users"]
    export_direct_messages = d["actions"]["export_direct_messages"]


def create_filename():
    """
    Create unique file name for each export file yyyy-mm-dd-hh-mm-ss.json
    """
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".json"

"""
--------------------------------------------------------------------------------
"""
read_config()

"""
export_object will hold each object (Version, Team, Channel, User, 
Post, DirectChannel, and DirectPost) that we create in the export
"""
export_object = {}
export_object[0] = {"type": "version", "version": 1}
file_position = 1

"""
Team
"""
teams = database_functions.get_teams(db_url, db_name, db_username, db_password, "")
print("Teams: " + str(teams))

for team in teams:
    export_object[file_position] = team


"""
Channel
"""

"""
User
"""

"""
Post
"""


"""
Open a file for writing, iterate over the export_object and write
each item onto a single line in JSONL format
"""
for key, value in export_object.iteritems():
    print value 