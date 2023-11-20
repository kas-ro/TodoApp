import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-database.db")
        self.cursor = self.con.cursor()
        self.create_task_table()


    # Creation de la table
    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL)")
        self.con.commit()

    # Creation d'une tache
    def create_task(self, task):
        self.cursor.execute("INSERT INTO tasks (task) VALUES(?)", [task])
        self.con.commit()

    # Recuperation des taches
    def get_tasks(self):
        item = self.cursor.execute("SELECT task FROM tasks").fetchall()
        return item

    # Suppression d'une tache
    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE task = ?", (task_id,))
        self.con.commit()

    # Fermeture de la base de donnee
    def close_db(self):
        self.con.close()
