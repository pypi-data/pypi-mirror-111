#!/usr/bin/env python3
import os
import subprocess
import sys

if os.getuid() == 0:
    if "CI_JOB_ID" not in os.environ:
        msg = "Installing Grapejuice as root is not supported"
        print(msg, file=sys.stderr)
        raise RuntimeError(msg)

try:
    architecture = subprocess.check_output(["uname", "-m"]).decode("UTF-8").strip()
    expected_architecture = "x86_64"

    if architecture.lower() != expected_architecture:
        msg = f"Roblox Studio will only run on the {expected_architecture} CPU architecture. " \
              f"The CPU architecture of this machine is {architecture}. The installer will now exit."
        print(msg, file=sys.stderr)
        sys.exit(-1)

except subprocess.CalledProcessError:
    pass

REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7


def perform_install():
    from pathlib import Path

    subprocess.check_call([sys.executable, "setup.py", "install_locally"])

    if "CI_JOB_ID" not in os.environ:
        subprocess.check_call([
            str(Path(os.environ["HOME"], ".local", "bin", "grapejuice").resolve()),
            "install-roblox", "--only-once"
        ])


def have_tkinter():
    try:
        import tkinter
        return True
    except ImportError:
        return False


def err_tkinter(title, message):
    import tkinter
    from tkinter import messagebox

    root = tkinter.Tk()
    root.withdraw()

    messagebox.showerror(title, message)


def have_zenity():
    import os
    return os.path.exists("/usr/bin/zenity")


def err_zenity(title, message):
    subprocess.call(["zenity", "--error", title, "--no-wrap", "--text={}".format(message)])


def err_desperation(message):
    subprocess.call(["xmessage", message])


def show_err(title, message):
    if have_tkinter():
        err_tkinter(title, message)

    elif have_zenity():
        err_zenity(title, message)

    else:
        err_desperation(message)


def err_py37():
    import sys

    ver = f"{REQUIRED_MAJOR}.{REQUIRED_MINOR}"

    show_err("Out of date",
             f"Your current version of python is out of date and therefore Grapejuice cannot be installed.\n\n"
             f"Python {ver} is required. Check the Grapejuice source repository for the installation instructions.\n\n"
             f"You have:\n{sys.version}"
             )


def have_py37():
    import sys

    satisfied = sys.version_info.major >= REQUIRED_MAJOR and sys.version_info.minor >= REQUIRED_MINOR

    if not satisfied:
        exit_code = -1

        try:
            err_py37()

        except Exception as e:
            exit_code = -2
            print(e, file=sys.stderr)

        sys.exit(exit_code)

    return satisfied


if __name__ == "__main__":
    if have_py37():
        perform_install()
