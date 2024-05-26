from typing import Tuple

from src.Homeworks.Homework_2.PerformedCommandStorage import *

AVAILABLE_COMMANDS = "Available commands:\n\t " + "\n\t ".join(REGISTRY.classes.keys()) + "\n\t Undo\n\t Show\n\t Exit"


def create_storage() -> PerformedCommandStorage:
    try:
        collection_type = input("Choose collection's type: ")
        numbers = input("Enter integers (for example: 1 2 3): ")
        collection = eval(f"{collection_type}(map(int, numbers.split()))")
    except NameError:
        raise NameError("Invalid collection type")
    except ValueError:
        raise ValueError("Expected int for storage")
    else:
        return PerformedCommandStorage(collection)


def parse_command(line: str) -> Tuple[str, list[str]]:
    command_line = line.split()
    return command_line[0], command_line[1:]


def get_output(cms: PerformedCommandStorage, command: str, arguments: list[str]) -> None:
    try:
        action = REGISTRY.dispatch(command)
    except ValueError:
        print("Incorrect action was entered")

    else:
        try:
            args: list[int] = list(map(int, arguments))
        except ValueError:
            print("Expected integer for arguments")

        else:
            try:
                cms.apply(action(*args))
            except TypeError:
                print("Incorrect number of arguments")


def running(cms: PerformedCommandStorage, command: str, arguments: list[str]) -> None:
    if command == "Undo":
        try:
            cms.undo()
        except IndexError as e:
            print(e)
    elif command == "Show":
        print(cms.collection)

    else:
        get_output(cms, command, arguments)


def main() -> None:
    try:
        cms = create_storage()
    except Exception as e:
        print(e)
    else:
        print(AVAILABLE_COMMANDS)

        while True:
            command, arguments = parse_command(input("Enter command with arg: "))
            if command == "Exit":
                break
            running(cms, command, arguments)


if __name__ == "__main__":
    main()
