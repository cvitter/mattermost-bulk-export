import MySQLdb
import json

def get_user_team_channels(db_url, db_name, db_username, db_password, user_id, team_id):
    channels = []
    sql_query = "SELECT " + \
                "a.Roles AS Roles, a.NotifyProps AS NotifyProps, " + \
                "b.Name AS ChannelName, b.Type AS ChannelType " + \
                "FROM " + \
                "mattermost.ChannelMembers AS a, " + \
                "mattermost.Channels AS b " + \
                "WHERE " + \
                "a.UserId = '" + user_id + "' AND " + \
                "a.ChannelId = b.Id AND " + \
                "b.Type != 'D' AND b.DeleteAt = 0 AND " + \
                "b.TeamId = '" + team_id + "'" 

    db = connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)

    for (roles, notify_props, channel_name, channel_type) in cursor:
        channel = {
            "name": channel_name,
            "roles": roles,
            "notify_props": get_prop_obj(notify_props)
        }
        channels.append(channel)
    return channels


def get_prop_obj(notify_props):
    notify_obj = json.loads(notify_props)
    prob_obj = {
        "desktop": notify_obj["desktop"],
        "email": notify_obj["email"],
        "mark_unread": notify_obj["mark_unread"],
        "push": notify_obj["push"]
    }
    return prob_obj


def get_user_teams(db_url, db_name, db_username, db_password, user_id):
    user_teams = []
    
    sql_query = "SELECT TeamId, " + \
                "(SELECT Name from mattermost.Teams WHERE Id = " + \
                "mattermost.TeamMembers.TeamId), Roles " + \
                "FROM mattermost.TeamMembers WHERE " + \
                "UserId = '" + user_id + "' AND DeleteAt = 0"
    db = connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)

    user_teams = []
    for (team_id, team_name, roles) in cursor:
        team = {
            "name": team_name,
            "roles": roles,
            "channels": get_user_team_channels(db_url, db_name, db_username, db_password, user_id, team_id)
        }
        user_teams.append(team)
    return user_teams

def get_users(db_url, db_name, db_username, db_password, team_list,
              export_deleted_users):
    users = ""

    sql_query = "SELECT " + \
                "Id, Username, Password, AuthData, AuthService, Email, " + \
                "Nickname, FirstName, LastName, Position, Roles, " + \
                "Locale " + \
                "FROM mattermost.Users"
    if export_deleted_users is False:
        sql_query += " WHERE DeleteAt = 0"
    sql_query += ";"

    db = connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)

    for (user_id, username, password, auth_data, auth_service, email, nickname,
         first_name, last_name, position, roles, locale) in cursor:

        user = {
            "type": "user",
            "user": {
                "profile_image": "",
                "username": username,
                "email": email,
                "auth_service": auth_service,
                "auth_data": auth_data,
                "password": password,
                "nickname": nickname,
                "first_name": first_name,
                "last_name": last_name,
                "position": position,
                "roles": roles,
                "locale": locale,
                "teams": get_user_teams(db_url, db_name, db_username, db_password, user_id)
            }
        }
        users += str(user) + "\n"

    return users


def get_channels(db_url, db_name, db_username, db_password, team_list,
                 export_deleted_teams, export_deleted_channels):
    """
    Get the list of teams to retrieve channels for
    """
    team_ids = get_team_ids(db_url, db_name, db_username, db_password,
                            team_list, export_deleted_teams)

    channels = ""
    for team_id in team_ids:
        sql_query = "SELECT " + \
                    "(SELECT Name FROM mattermost.Teams WHERE " + \
                    "id = '" + team_id + "'), " + \
                    "DisplayName, Name, Type, Header, Purpose " + \
                    "FROM mattermost.Channels " + \
                    "WHERE TeamId = '" + team_id + "'"

        if export_deleted_channels is False:
            sql_query += " AND DeleteAt = 0"
        sql_query += ";"

        db = connect(db_url, db_username, db_password, db_name)
        cursor = db.cursor()
        cursor.execute(sql_query)

        for (team_name, display_name, name, type, header, purpose) in cursor:
            channel = {
                "type": "channel",
                "channel": {
                    "team": team_name,
                    "name": name,
                    "display_name": display_name,
                    "type": type,
                    "header": header,
                    "purpose": purpose,
                }
            }
            channels += str(channel) + "\n"

    return channels


def get_team_ids(db_url, db_name, db_username, db_password, team_list,
                 export_deleted_teams):
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

    if export_deleted_teams is False:
        """
        Only export teams that have a DeleteAt = 0
        """
        if len(where_clause) > 0:
            where_clause += " AND "
        else:
            where_clause += " WHERE "
        where_clause += "DeleteAt = 0"

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


def get_teams(db_url, db_name, db_username, db_password, team_list,
              export_deleted_teams):
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

    if export_deleted_teams is False:
        """
        Only export teams that have a DeleteAt = 0
        """
        if len(where_clause) > 0:
            where_clause += " AND "
        else:
            where_clause += " WHERE "
        where_clause += "DeleteAt = 0"

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
