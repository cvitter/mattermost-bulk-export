import json
from datetime import datetime 
import database_functions

def create_filename():
    """
    Create unique file name for each export file yyyy-mm-dd-hh-mm-ss.json
    """
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".json"

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
teams = database_functions.get_teams("")

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