import pymysql
import pymysql.cursors

class Database:

    connection : pymysql
    
    def __init__(self):
        try:
            self.connection = pymysql.connect(host='localhost',
                                    user='root',
                                    database='dcuk_mqtt_docker',
                                    cursorclass=pymysql.cursors.DictCursor)
        except(Exception) as error:
            print(f"Error connecting to database {error}")

    def insert_senzor(self,data):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO senzory(nazev, typ, misto) VALUES (%s, %s, %s)"
                cursor.execute(sql, (data['nazev'], data['typ'], data['misto']))
            self.connection.commit()
            print("Data inserted successfully")
        except Exception as e:
            print(f"Error inserting data: {str(e)}")

    def insert_zaznam(self,jmeno):
        sql = "SELECT id_sen FROM senzory WHERE nazev = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql, (jmeno,))
        id_sen = cursor.fetchone()['id_sen']
        try:
            with self.connection.cursor() as cursor:
                sql = f"INSERT INTO zaznamy(id_sen) VALUES ({id_sen})"
                cursor.execute(sql)
            self.connection.commit()
            print("Data inserted successfully")
        except Exception as e:
            print(f"Error inserting data: {str(e)}")

    def does_exists(self, jmeno):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM senzory WHERE nazev = %s"
                cursor.execute(sql, (jmeno,))
                result = cursor.fetchone()
                if result['COUNT(*)'] == 0:
                    return False
                else:
                    return True
        except Exception as e:
            print(f"Error checking if sensor exists: {str(e)}")
            return False

    def insert_senzorV3(self, data):
        try:
            with self.connection.cursor() as cursor:
                # Start transaction
                cursor.execute("START TRANSACTION;")
                
                # senzory
                sql_senzory = """
                INSERT INTO senzory (nazev, typ, misto)
                SELECT %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM senzory WHERE nazev = %s
                );
                """
                print(data['nazev'])
                cursor.execute(sql_senzory, (data['nazev'], data['typ'], data['misto'], data['nazev']))
                
                # zaznamy
                sql_zaznamy = """
                INSERT INTO zaznamy (id_sen)
                SELECT id_sen FROM senzory WHERE nazev = %s;
                """
                cursor.execute(sql_zaznamy, (data['nazev'],))
                
                # Commit transaction
                cursor.execute("COMMIT;")
            
            self.connection.commit()
            print("Data inserted successfully")
        except Exception as e:
            # Rollback transaction on error
            self.connection.rollback()
            print(f"Error inserting data: {str(e)}")

        




