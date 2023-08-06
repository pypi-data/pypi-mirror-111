import sqlite3
from tabulate import tabulate
import datetime

c_date = datetime.date.today()

class DatabaseConnection:
    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.cur = self.conn.cursor()

        self.cur.execute(
            """Create table IF NOT EXISTS myroutine
            (task_id INTEGER primary key AUTOINCREMENT, task TEXT, date TEXT, time TEXT, status TEXT, deadline TEXT)"""
        )
        self.conn.commit()

    def add_task(self, task, status,deadline):
        self.task = task
        self.status = status
        self.deadline = deadline
        global c_date
        start = datetime.datetime.now()
        time = start.strftime("%H:%M:%S")
        self.cur.execute("""INSERT INTO myroutine(task, date, time, status, deadline) VALUES(?, ?, ?, ?, ?)""",
                            (self.task, c_date, time, self.status, self.deadline),)
        self.conn.commit()
        print("task added successfully.")

    def show_task(self):
        self.cur.execute("""SELECT * FROM myroutine""")
        data_for_table = self.cur.fetchall()
        table = tabulate(data_for_table, headers=["ID", "Task", "Date", "Time", "Status", "Deadline"], tablefmt="fancy_grid")
        print(table)

    def update_task(self, task, task_id):
        self.task = task
        self.task_id = task_id
        global c_date
        start = datetime.datetime.now()
        time = start.strftime("%H:%M:%S")
        self.cur.execute(
            """UPDATE myroutine
                SET task = ?,
                date = ?,
                time = ?
                WHERE task_id = ?""",
            (self.task, c_date, time, self.task_id),
        )
        self.conn.commit()
        print("Task updated successfully.")

    def delete_task(self, task_id):
        self.task_id = task_id
        self.cur.execute(
            """DELETE FROM myroutine
                WHERE task_id = ?""",
            (self.task_id,),
        )
        self.conn.commit()
        print("Task deleted successfully.")

    def sort_task(self,date):
        self.date = date
        self.cur.execute("""SELECT date,
                            task
                            FROM myroutine
                            WHERE date = ?
                            ORDER BY date""",
                         (self.date,),   
                        )
        sort = self.cur.fetchall()
        print(tabulate(sort, headers=["date","Task"], tablefmt="fancy_grid"))

    def status_add(self, task_id, status):
        self.task_id = task_id
        self.status = status
        self.cur.execute("""UPDATE myroutine
                               SET status = ?
                               WHERE task_id = ?""",
                            (self.status,self.task_id),)
        self.conn.commit()
        print("Status added successfully")

    def clear_task(self):
        self.cur.execute(
            """DELETE FROM myroutine""")
        self.conn.commit()
        print("Tasks deleted successfully.")

