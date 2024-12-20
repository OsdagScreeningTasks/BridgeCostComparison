import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_data (
                Material TEXT,
                BaseRate REAL,
                MaintenanceRate REAL,
                RepairRate REAL,
                DemolitionRate REAL,
                EnvironmentalFactor REAL,
                SocialFactor REAL,
                DelayFactor REAL
            )
        """)
        self.conn.commit()

    def fetch_all_cost_data(self):
        self.cursor.execute("SELECT * FROM cost_data")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
