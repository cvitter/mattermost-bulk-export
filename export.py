import json
from datetime import datetime
import database_functions as db


def read_config():
    """
    Read the config.json file and populate global variables
    """
    global db_url, db_name, db_username, db_password
    global team_list, export_deleted_teams
    global export_deleted_channels
    global export_inactive_users, export_direct_messages

    with open('config.json') as config_file:
        d = json.loads(config_file.read())

    db_url = d["database"]["url"]
    db_name = d["database"]["database"]
    db_username = d["database"]["user"]
    db_password = d["database"]["password"]
    team_list = d["actions"]["export_team_list"]
    export_deleted_teams = d["actions"]["export_deleted_teams"]
    export_deleted_channels = d["actions"]["export_deleted_channels"]
    export_inactive_users = d["actions"]["export_deleted_users"]
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
file_name = create_filename()
with open(file_name, "a") as output_file:
    output_file.write(str({"type": "version", "version": 1}))

    """
    Team
    """
    teams = db.get_teams(db_url, db_name, db_username, db_password,
                         team_list, export_deleted_teams)
    output_file.write(teams)

    """
    Channel
    """
    channels = db.get_channels(db_url, db_name, db_username, db_password,
                               team_list, export_deleted_teams,
                               export_deleted_channels)
    output_file.write(channels)

    """
    User
    """
    users = db.get_users(db_url, db_name, db_username, db_password,
                         team_list, export_deleted_users)
    output_file.write(users)

    
"""
Post
"""
