import click
import datetime

from mytask.database import DatabaseConnection

dc = DatabaseConnection()
c_date = datetime.date.today()

@click.command(help="Add the task.")
@click.option("--add", "-a")
def add(add):
    default_status = 'Todo'
    d = int(input("How many days will you complete the task? ") or "5")
    d_date = c_date + datetime.timedelta(days= d)
    if add:
        task_added = dc.add_task(add, status = default_status, deadline = d_date)
        if task_added:
            print("Task added successfully.")
    else:
        print("Please provide a Task")


@click.command(help="Show the task.")
@click.option("--show", "-s")
def show(show):
    view = dc.show_task()


@click.command(help="Update the task.")
@click.option("--update", "-u")
def update(update):
    update_task_id = int(click.prompt("Enter task_id which you want to modify"))
    new_task = click.prompt("Enter new task")
    dc.update_task(task_id=update_task_id, task=new_task)


@click.command(help="Delete the task.")
@click.option("--delete", "-d")
def delete(delete):
    delete_task_id = int(click.prompt("Enter task_id which you want to delete"))
    dc.delete_task(task_id=delete_task_id)


@click.command(help="Sort the task.")
@click.option("--sort", "-o")
def sort(sort):
    order_by = click.prompt("Enter the date to sort the tasks [yyyy-mm-dd]")
    dc.sort_task(date = order_by)

@click.command(help="Provide tag to the task.")
@click.option("--status", "-st")
def status(status):
    status_task_id = int(click.prompt("Enter task_id which you want to labelled"))
    update_status = click.prompt("Please update the status of task [In process/Complete]")
    dc.status_add(task_id = status_task_id, status = update_status)

@click.command(help="Delete all the tasks.")
@click.option("--clear", "-c")
def clear(clear):
    view = dc.clear_task()