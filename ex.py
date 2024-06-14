import psycopg2 
class Subscriptions(): 
     
    def __init__(self, dbname, host, port, user, password): 
        self.dbname = dbname 
        self.host = host 
        self.port = port 
        self.user = user 
        self.password = password 
        self.connection = None 
        self.cursor = None 
    
    def connect(self): 
        try: 
            self.connection = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port, user=self.user, password=self.password) 
            print("Connected successfully") 
        except Exception as e: 
            print(f"Connection refused: {e}") 
        else: 
            self.cursor = self.connection.cursor()
             
    def create_Users(self, table_name, **kwargs):
        columns = ', '.join([column for column in kwargs.get('columns', [])]) 
        values = ', '.join([f"'{column}'" if type(column) == str else f"{column}" for column in kwargs.get('values', [])]) 
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})" 
        print('User added succesfully')
        try: 
            self.cursor.execute(query=query) 
            self.connection.commit() 
        except Exception as error: 
            print(f"Something gone wrong: {error}") 

    def create_Journals(self, table_name, **kwargs):
        columns = ', '.join([column for column in kwargs.get('columns', [])]) 
        values = ', '.join([f"'{column}'" if type(column) == str else f"{column}" for column in kwargs.get('values', [])]) 
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})" 
        print('Journal added succesfully')
        try: 
            self.cursor.execute(query=query) 
            self.connection.commit() 
        except Exception as error: 
            print(f"Something gone wrong: {error}")
 
    def select(self, table_name, **kwargs): 
        columns = ', '.join(kwargs.get('columns', [])) if kwargs.get('columns') else '*' 
        query = f"SELECT {columns} FROM {table_name}" 
        try: 
            self.cursor.execute(query) 
            return self.cursor.fetchall() 
        except Exception as e: 
            print(f"Something went wrong: {e}")

    def subscriptions_User(self, user_id, journal_id): 
        query = "Insert into Subscriptions (user_id, journal_id) values (%s, %s)" 
        try: 
            self.cursor.execute(query, (user_id, journal_id)) 
            self.connection.commit() 
            print(f"Succesfully subscrised {user_id}, {journal_id}") 
        except Exception as e: 
            print(f"Something went wrong: {e}") 
 
    def unsubscriptions_User(self, user_id, journal_id): 
        query = "Delete from Subscriptions where user_id = %s and journal_id = %s" 
        try: 
            self.cursor.execute(query, (user_id, journal_id)) 
            self.connection.commit() 
            print(f"Succesfully unsubscrised {user_id}, {journal_id}") 
        except Exception as e: 
            print(f"Something went wrong: {e}")

def databasa(): 
    database = Subscriptions('exam', '127.0.0.1', 5432, user='postgres', password='postgres') 
    database.connect() 

    while True:
        print("\n1. Create Users\n2. Create Journals\n3. Select Users\n4. Select Journals\n5. Subscription User\n6. Unsubscription User\n7. Select Subscription\n8. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            table = 'Users'
            name = input('Enter name of user: ')
            database.create_Users(table, columns=['name'], values=[name])
        elif choice == 2:
            table = 'Journals'
            title = input('Enter title of journal: ')
            database.create_Journals(table, columns=['title'], values=[title])
        elif choice == 3:
            table = 'Users'
            result = database.select(table)
            print(result)
        elif choice == 4:
            table = 'Journals'
            result = database.select(table)
            print(result)
        elif choice == 5:
            user_id = int(input("Enter id of user: ")) 
            journal_id = int(input("Enter id of journal : ")) 
            database.subscriptions_User(user_id, journal_id)
        elif choice == 6:
            user_id = int(input("Enter id of user: ")) 
            journal_id = int(input("Enter id of journal : ")) 
            database.unsubscriptions_User(user_id, journal_id)
        elif choice == 7:
            table = 'Subscriptions'
            result = database.select(table)
            print(result)
        elif choice == 8:
            break
        else:
            print("Choose only from 1 to 8!")

if __name__ == "__main__": 
        databasa()