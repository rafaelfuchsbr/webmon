import logger
from dbconnection import DBConnection 

def init():
    conn = DBConnection()

    sql = open('sql/database.sql').read()
    conn.getCursor().execute(sql)
    conn.commit()

    sql = open('sql/initial_data.sql').read()
    conn.getCursor().execute(sql)
    conn.commit()

    conn.close()

if __name__ == '__main__':
    init()