import MySQLdb


def get_teams(db_url, db_name, db_user, db_password, team_list):
    """
    Takes
    """
    teams = {}
    team_row = 0;

    if len(team_list) == 0:
        sql_query = "SELECT " + \
                    "DisplayName, Name, Type, Description, AllowOpenInvite " + \
                    "FROM mattermost.Teams;"

    db = connect(db_url, db_user, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)

    for (DisplayName, Name, Type, Description, AllowOpenInvite) in cursor:
        teams[team_row] = {
            "name": Name,
            "display_name": DisplayName,
            "type": Type,
            "description": Description,
            "allow_open_invite": AllowOpenInvite
        }
    team_row += 1
        
    return teams


def connect(url, user, password, database):
    """
    Connects to the database and returns the database object
    """
    db = MySQLdb.connect(host=url, user=user, passwd=password, db=database)
    return db
