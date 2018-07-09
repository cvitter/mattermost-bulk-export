import MySQLdb


def get_channels(db_url, db_name, db_username, db_password, team_list, 
                 export_deleted_teams, export_deleted_channels):
    """
    We need to get the list of teams to retrieve channels for based
    """
    team_ids = get_team_ids(db_url, db_name, db_username, db_password,
                            team_list, export_deleted_teams)
    for team in team_ids:
        print(team)

    channels = ""

    sql_query = ""

    where_clause = ""

    sql_query += ";"

    """
        "type": "channel",
        "channel": {
            "team": "team-name",
            "name": "channel-name",
            "display_name": "Channel Name",
            "type": "O",
            "header": "The Channel Header",
            "purpose": "The Channel Purpose",
            }
        }
    """

    return channels


def get_team_ids(db_url, db_name, db_username, db_password, team_list, export_deleted_teams):
    """
    Get list of team ids to retrieve data for based on configuration
    """
    sql_query = "SELECT Id FROM mattermost.Teams"

    where_clause = ""
    if len(team_list) > 1:
        """
        Add where and or clauses to query if we are filtering on teams
        """
        list_pos = 0
        where_clause = " WHERE "
        for team_name in team_list:
            where_clause += "DisplayName = '" + team_name + "'"
            if list_pos < len(team_list) - 1:
                where_clause += " OR "
            list_pos += 1

    if export_deleted_teams == False:
        """
        Only export teams that have a DeleteAt = 0
        """
        if len(where_clause) > 0:
            where_clause += " AND "
        else:
            where_clause += " WHERE "
        where_clause +=  "DeleteAt = 0"

    if len(where_clause) > 0:
        sql_query += where_clause

    sql_query += ";"

    db = connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)
    
    team_ids = []
    for (team_id) in cursor:
        team_ids.append(team_id[0])
    return team_ids


def get_teams(db_url, db_name, db_username, db_password, team_list, export_deleted_teams):
    teams = ""

    sql_query = "SELECT " + \
                "DisplayName, Name, Type, Description, AllowOpenInvite " + \
                "FROM mattermost.Teams"

    where_clause = ""
    if len(team_list) > 1:
        """
        Add where and or clauses to query if we are filtering on teams
        """
        list_pos = 0
        where_clause = " WHERE "
        for team_name in team_list:
            where_clause += "DisplayName = '" + team_name + "'"
            if list_pos < len(team_list) - 1:
                where_clause += " OR "
            list_pos += 1

    if export_deleted_teams == False:
        """
        Only export teams that have a DeleteAt = 0
        """
        if len(where_clause) > 0:
            where_clause += " AND "
        else:
            where_clause += " WHERE "
        where_clause +=  "DeleteAt = 0"

    if len(where_clause) > 0:
        sql_query += where_clause

    sql_query += ";"
    db = connect(db_url, db_username, db_password, db_name)
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
