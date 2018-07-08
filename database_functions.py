import MySQLdb


def get_teams(db_url, db_name, db_user, db_password, team_list):
    teams = ""
    if len(team_list) == 0:
        sql_query = "SELECT " + \
                    "DisplayName, Name, Type, Description, AllowOpenInvite " + \
                    "FROM mattermost.Teams;"

    db = connect(db_url, db_user, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)

    for (display_name, name, type, description, allow_open_invite) in cursor:
        team = {
            "type": "team",
            "team": {
                "name": name,
                "display_name": display_name,
                "type": type,
                "description": description,
                "allow_open_invite": allow_open_invite
            }
        }
        teams += str(team) + "\n"
        
    return teams


def connect(url, user, password, database):
    """
    Connects to the database and returns the database object
    """
    db = MySQLdb.connect(host=url, user=user, passwd=password, db=database)
    return db
