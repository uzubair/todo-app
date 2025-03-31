import click
from tabulate import tabulate

from . import database


class TodoApp:
    """A simple class to interact with SQLite3 database"""

    DISPLAY_HEADERS = ["Id", "Task Name", "Status", "Created At", "Updated At"]

    def __init__(self):
        self._dbname = "todo.db"

    def add_task(self, task_name):
        with database.DBHelper(self._dbname) as db:
            db.add_tasks([(task_name, "pending")])

    def remove_task(self, task_id):
        with database.DBHelper(self._dbname) as db:
            db.remove_task(task_id)

    def mark_complete(self, task_id):
        with database.DBHelper(self._dbname) as db:
            db.mark_complete(task_id)

    def list_tasks(self, filter):
        with database.DBHelper(self._dbname) as db:
            tasks = db.list_tasks(filter)
            if not tasks:
                print(f"There are no tasks to display!")
                return

            all_tasks = []
            for task in tasks:
                task_id, task_name, status, created_at, updated_at = task
                all_tasks.append([task_id, task_name, status, created_at, updated_at])

            print(tabulate(all_tasks, headers=TodoApp.DISPLAY_HEADERS))


"""
Handle the command-line arguments
"""


@click.group()
def cli():
    pass


@cli.command()
@click.option("-n", "--task-name", required=True, help="Name of the task")
def add_task(task_name):
    print(f"Adding task with name: '{task_name}'")
    TodoApp().add_task(task_name)


@cli.command()
@click.option("-i", "--task-id", required=True, help="Id of the task")
def remove_task(task_id):
    print(f"Removing task with id: '{task_id}'")
    TodoApp().remove_task(task_id)


@cli.command()
@click.option("-i", "--task-id", required=True, help="Id of the task")
def mark_complete(task_id):
    print(f"Marking task with id: '{task_id}' to complete")
    TodoApp().mark_complete(task_id)


@cli.command()
@click.option(
    "-f",
    "--filter",
    required=False,
    help="Specific a filter to narrow down your results. Defaults to 'None'",
    default=None,
)
def list_tasks(filter):
    print(f"Showing tasks with filter: '{filter}'")
    TodoApp().list_tasks(filter)
