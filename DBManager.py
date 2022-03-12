import pyodbc


class DBManager:
    def __init__(self):
        self.conn = pyodbc.connect(r'Driver=SQL Server; Server=.\SQLEXPRESS;Database=WordleLeaderBoard;Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()
        self.table_name = "PeopleInfo"

    def createTable(self):
        self.cursor.execute('''
        CREATE TABLE PeopleInfo (
            ID INTEGER PRIMARY KEY IDENTITY(1,1),
            Name VARCHAR(100) NOT NULL,
            Score INTEGER NOT NULL,
            );''')
        self.conn.commit()
        
    def tableExists(self):
        if self.cursor.tables(table='PeopleInfo').fetchone():
            return True
        else:
            return False

    def update(self, players):
        for player in players.keys():
            command = "SELECT * FROM PeopleInfo WHERE Name = ?"
            if self.cursor.execute(command, (str(player))).fetchone():
                command = "UPDATE PeopleInfo SET Score = ? WHERE Name = ?"
                self.cursor.execute(command, (str(players[player]), str(player)))
                self.conn.commit()
            else:
                command = "INSERT INTO PeopleInfo(Name, Score) values (?, ?)"
                self.cursor.execute(command, (str(player), str(players[player])))
                self.conn.commit()
