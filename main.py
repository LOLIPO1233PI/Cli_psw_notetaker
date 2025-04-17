import base64
import json
import os
import platform
import subprocess
import sys


class Colors:
    """
    Class containing a list of ANSI color escape codes
    """

    Black: str = "\033[30m"
    Red: str = "\033[31m"
    Green: str = "\033[32m"
    Yellow: str = "\033[33m"
    Blue: str = "\033[34m"
    Magenta: str = "\033[35m"
    Cyan: str = "\033[36m"
    White: str = "\033[37m"
    Black_Background: str = "\033[40m"
    Red_Background: str = "\033[41m"
    Green_Background: str = "\033[42m"
    Yellow_Background: str = "\033[43m"
    Blue_Background: str = "\033[44m"
    Magenta_Background: str = "\033[45m"
    Cyan_Background: str = "\033[46m"
    White_Background: str = "\033[47m"
    Reset_Color: str = "\033[39m"
    Reset_Background: str = "\033[49m"


def get_psw_path(dir_name: str = "_") -> str:
    path = os.path.abspath(dir_name)
    # this code has been taken from
    # >> https://github.com/dwoctor/hide-or-unhide-a-directory-python/blob/master/portable.py
    if platform.system()== "Windows":
        subprocess.call(["attrib", "+H", f"{path}"])
    elif platform.system() == "Darwin":
        subprocess.call(["chflags", "hidden", f"{path}"])
    # end
    return path


def create_default_list(path: str = get_psw_path()) -> None:
    placeholder: str = """{"name":[]}"""
    try:
        with open(os.path.join(path, "data"), "wb") as f:
            f.write(base64.b85encode(bytes(placeholder, encoding="utf-8")))
    except (OSError, IOError):
        print(
            f"{Colors.Red}Couldnt create default list (try doing it manually), exiting ...{Colors.Reset_Color} %s",
        )
        sys.exit(1)


def choice_handler() -> int:
    try:
        value = int(input(f">> {Colors.Green}Enter your choice: {Colors.Reset_Color}"))
        if 1 <= value <= 2:
            return value
        raise ValueError
    except ValueError:
        print(f"{Colors.Red}Invalid choice !{Colors.Reset_Color}")
        return choice_handler()


def entry_adding() -> None:
    name = input(f">> {Colors.Green}Enter your entry name: {Colors.Reset_Color}")
    psw = input(f">> {Colors.Green}Enter your password: {Colors.Reset_Color}")
    email_username = input(
        f">> {Colors.Green}Enter your email / username: {Colors.Reset_Color}"
    )
    try:
        with open(os.path.join(get_psw_path(), "data"), "rb") as f:
            file_data = f.read()
            file_data = base64.b85decode(file_data).decode()
            data: dict = json.loads(file_data)
            data["name"].append(
                {"entry": name, "password": psw, "email": email_username}
            )
            data = base64.b85encode(bytes(json.dumps(data), encoding="utf-8"))
        with open(os.path.join(get_psw_path(), "data"), "wb") as f:
            f.write(data)
    except ValueError:
        print(
            f"{Colors.Red}The password list file is Corrupted, exiting ...{Colors.Reset_Color}"
        )
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"{Colors.Red}The password list file is Malformed, exiting ...{Colors.Reset_Color}"
        )
        sys.exit(1)


def entry_reading() -> None:
    try:
        with open(os.path.join(get_psw_path(), "data"), "rb") as f:
            file_data = f.read()
            file_data = base64.b85decode(file_data).decode()
            data: dict = json.loads(file_data)
            for i in data["name"]:
                print(
                    f"\nPassword of {Colors.Magenta}{i['entry'] or 'Undefined'}{Colors.Reset_Color}\n",
                    f"  {Colors.Red}Email{Colors.Reset_Color}: {i['email'] or (f'{Colors.Blue_Background}Nothing{Colors.Reset_Background}')}",
                    f"\n   {Colors.Magenta}Password{Colors.Reset_Color}: {i['password'] or (f'{Colors.Blue_Background}Nothing{Colors.Reset_Background}')}\n",
                )
    except ValueError:
        print(
            f"{Colors.Red}The password list file is Corrupted, exiting ...{Colors.Reset_Color}",
        )
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"{Colors.Red}The password list file is Malformed, exiting ...{Colors.Reset_Color}"
        )
        sys.exit(1)


def cli_interface() -> None:
    print(
        f"{Colors.Magenta}-- Welcome to the Open Source cli Psw manager --{Colors.Reset_Color}"
    )
    print(
        f"{Colors.Green}1.{Colors.Reset_Color} {Colors.Blue}Add password entry{Colors.Reset_Color}"
    )
    print(
        f"{Colors.Green}2.{Colors.Reset_Color} {Colors.Cyan}Access password entry{Colors.Reset_Color}"
    )
    path = get_psw_path()
    dir_name = "_"
    if not os.path.isfile(os.path.join(path, "data")):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        create_default_list(path)
    choice: int = choice_handler()
    if choice == 1:
        entry_adding()
    else:
        entry_reading()


if __name__ == "__main__":
    cli_interface()
