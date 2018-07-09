import MySQLdb


def get_users(db_url, db_name, db_username, db_password, team_list,
              export_deleted_users):
    users = ""

    sql_query = "SLECT " + \
                "Username, Password, AuthData, AuthService, Email, " + \
                "Nickname, FirstName, LastName, Position, Roles, " + \
                "Locale " + \
                "FROM mattermost.Users"
    if export_deleted_users is False:
        sql_query += " WHERE DeleteAt = 0"
    sql_query += ";"

    db = connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    cursor.execute(sql_query)

    for (username, password, auth_data, auth_service, email, nickname,
         first_name, last_name, postion, roles, locale) in cursor:

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
                "locale": locale
            }
        }
        users += str(user) + "\n"

    return users

"""
{
  "type": "user",
  "user": {
    "profile_image": "avatar.png",
    "username": "username",
    "email": "email@example.com",
    "auth_service": "",
    "auth_data": "",
    "password": "passw0rd",
    "nickname": "bobuser",
    "first_name": "Bob",
    "last_name": "User",
    "position": "Senior Developer",
    "roles": "system_user",
    "locale": "pt_BR",
    "teams": [
      {
        "name": "team-name",
        "roles": "team_user team_admin",
        "channels": [
          {
            "name": "channel-name",
            "roles": "channel_user",
            "notify_props": {
              "desktop": "default",
              "mark_unread": "all"
            }
          }
        ]
      }
    ]
  }
}
"""

def get_user_teams(db_url, db_name, db_username, db_password, user_id):
    user_teams = ""

    return user_teams


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
