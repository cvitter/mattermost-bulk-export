import MySQLdb


def get_teams(team_list):
    """
    Takes
    """
    teams = {}
    
    return teams


def connect(url, user, password, database):
    """
    Connects to the database and returns the database object
    """
    db = MySQLdb.connect(host=url, user=user, passwd=password, db=database)
    return db
