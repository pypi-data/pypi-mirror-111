import mysql.connector
from tabulate import tabulate

mydb = mysql.connector.connect(

    host = 'localhost',
    user = 'PythonScript',
    password = 'Nvkc49OsipuUSjFz3txor9ELRIFaCep',
    db = "Discord_Bot_IHK"
)

print(mydb)

class DatabaseConnector():

    def insert_user_into_database(name):
        bool = DatabaseConnector.check_if_user_exists(name)

        if bool == False:
            mycursor = mydb.cursor()

            sql_statement = "INSERT INTO users (Name) VALUES (%s)"
            sql_values = (str(name), )
            mycursor.execute(sql_statement, sql_values)

            mydb.commit()

            res = mycursor.fetchall()

            print(mycursor.rowcount)
            print(res)

            mycursor.close()

        else:
            return

    def insert_message_into_database(message, user, channel):
        mycursor = mydb.cursor()

        sql_statement = "INSERT INTO history (Content, User, Channel, Date) VALUES (%s, (SELECT UserID FROM users where Name = %s), %s, NOW())"
        sql_values = (str(message), str(user), str(channel))
        mycursor.execute(sql_statement, sql_values)

        mydb.commit()

        rows = mycursor.fetchall()
        print("rows: " + str(rows))

        mycursor.close()

    def check_if_user_exists(value):

        mycursor = mydb.cursor()

        sql_statement = "SELECT COUNT(*) FROM users WHERE Name = %s"
        sql_values = (str(value), )
        mycursor.execute(sql_statement, sql_values)

        rows = mycursor.fetchone()
        print("rows" + str(rows))

        print("res: " + str(mycursor.rowcount))

        if rows[0] >= 1:
            mycursor.close()
            print(True)
            return True
        else:
            mycursor.close()
            print(False)
            return False

    def get_history():
        mycursor = mydb.cursor()

        sql_statement = "SELECT Content, Date FROM history WHERE User != 2 AND User != 3"
        mycursor.execute(sql_statement)

        rows = mycursor.fetchall()
        print("rows")
        print(rows)

        print("res: " + str(mycursor.rowcount))

        print(tabulate(rows, headers=['Message', 'Time'], tablefmt='psql'))

        return tabulate(rows, headers=['Message', 'Time'], tablefmt='psql')

    def get_stats_messages_user():
        mycursor = mydb.cursor()

        sql_statement = "SELECT COUNT(*) FROM history WHERE User != 2 AND User != 3"
        mycursor.execute(sql_statement)

        res = mycursor.fetchone()[0]

        print(res)

        return res

    def get_stats_messages_all():
        mycursor = mydb.cursor()

        sql_statement = "SELECT COUNT(*) FROM history"
        mycursor.execute(sql_statement)

        res = mycursor.fetchone()[0]

        print(res)

        return res

    def get_stats_messages_date(date):

        mycursor = mydb.cursor()

        sql_statement = "SELECT COUNT(*) FROM Discord_Bot_IHK.history WHERE Date LIKE '" + "%" + str(date) + "%" + "' ;"

        print(sql_statement)
        mycursor.execute(sql_statement)

        res = mycursor.fetchone()[0]

        print(res)

        return res