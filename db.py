import psycopg2


def open_db(db_config):
    """
    This function open posgresql-session with db-config
    :param db_config: dict of db-parameters
    :type db_config: dict
    :return: 2 objects - connect-object and cursor-object
    :rtype: object
    """
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["address"]
    port = db_config["port"]
    db_name = db_config["db_name"]
    connect = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    cursor = connect.cursor()
    return cursor, connect


def close_db(cursor, connect):
    """
    This function close the connection to db
    :param database: database-object
    :param connect: connection-object
    :type database: object
    :type connect: object
    """
    cursor.close()
    connect.close()


def get_user_by_chat_id(db_config, tg_chat_id):
    """
    This function add an event to db.
    :param db_config: db config dict
    :param event_id: event id to add
    :type db_config: dict
    :type event_id: int
    """
    cursor, connect = open_db(db_config)
    cursor.execute("SELECT * FROM \"USERS\" WHERE \"TG_CHAT_ID\" = (%i);", (tg_chat_id,))
    result = cursor.fetchall()
    close_db(cursor, connect)
    print("result {}".format(result))
