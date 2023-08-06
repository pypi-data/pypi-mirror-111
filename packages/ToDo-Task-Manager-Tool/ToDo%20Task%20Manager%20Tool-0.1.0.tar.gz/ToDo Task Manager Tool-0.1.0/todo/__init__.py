import click

from todo.task import add
from todo.task import show
from todo.task import update
from todo.task import delete


@click.group()
def main():
    """""Todo Manager"""""
    pass


main.add_command(add)
main.add_command(show)
main.add_command(update)
main.add_command(delete)

if __name__ == "__main__":

    main()
