import sqlite3
from datetime import datetime

class DatabaseManager:
    ## חלוקת קוד (Coupling & Cohesion): הקובץ עוסק אך ורק מול ה-SQLite (לכידות גבוהה)
    ## זהו צימוד נמוך (Low Coupling) - שאר הקוד לא תלוי בפרטי מימוש מסד הנתונים
    ## ניהול בסיס הנתונים (Persistence)
    def __init__(self, db_name="casino.db"):
        ## self: מופע מנהל בסיס הנתונים שאחראי על החיבור והשאילתות
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        ## יצירת טבלאות המערכת
        ## טבלת שחקנים ומאזן
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                username TEXT PRIMARY KEY,
                balance INTEGER
            )
        ''')
        
        ## טבלת היסטוריית משחקים מפורטת
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                amount INTEGER,
                result TEXT,
                bet_type TEXT,
                selection TEXT,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()

    def load_player_data(self, username):
        ## טעינת נתוני שחקן או יצירת שחקן חדש
        self.cursor.execute("SELECT balance FROM players WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            initial_balance = 1000
            self.cursor.execute("INSERT INTO players (username, balance) VALUES (?, ?)", (username, initial_balance))
            self.conn.commit()
            return initial_balance

    def update_balance(self, username, new_balance):
        ## עדכון יתרת השחקן
        self.cursor.execute("UPDATE players SET balance = ? WHERE username = ?", (new_balance, username))
        self.conn.commit()

    def save_game(self, player_name, amount, result, bet_type, selection):
        ## שמירת תוצאת משחק להיסטוריה
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO history (player_name, amount, result, bet_type, selection, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (player_name, amount, result, bet_type, selection, timestamp))
        self.conn.commit()

    def get_player_history(self, username, limit=10):
        ## שליפת היסטוריית המשחקים
        query = """
            SELECT id, player_name, amount, result, timestamp, bet_type, selection 
            FROM history 
            WHERE player_name = ? 
            ORDER BY id DESC 
            LIMIT ?
        """
        self.cursor.execute(query, (username, limit))
        return self.cursor.fetchall()
