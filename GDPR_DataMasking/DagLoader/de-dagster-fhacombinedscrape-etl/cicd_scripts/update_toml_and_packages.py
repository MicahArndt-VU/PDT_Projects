import tkinter as tk
from tkinter import simpledialog
import tomlkit
import os


def update_toml_file(project_name_parm):
    try:
        with open('./pyproject.toml', "r") as toml_file:
            toml_data = tomlkit.parse(toml_file.read())

            toml_data["tool"]["dagster"]["module_name"] = project_name_parm.replace("-", "_")

            toml_data["tool"]["poetry"]["name"] = project_name_parm

            toml_data["tool"]["poetry"]["packages"][0]["include"] = project_name_parm.replace("-", "_")

            toml_data["tool"]["poetry"]["authors"] = [f"{os.getlogin()} <{os.getlogin()}@veteransunited.com>"]

            with open('./pyproject.toml', "w") as toml_file:
                toml_file.write(tomlkit.dumps(toml_data))

            print("Successfully updated pyproject.toml")

    except FileNotFoundError:
        print("pyproject.toml not found. Please make sure the file exists.")


def update_python_package_names(project_name_parm):
    project_name_no_dashes = project_name_parm.replace("-", "_")
    try:
        os.rename("./de_dagster_fhacombinedscrape_etl", f"./{project_name_no_dashes}")
        os.rename("./de_dagster_fhacombinedscrape_test", f"./{project_name_no_dashes}_test")
        print("Successfully renamed python packages.")
    except:
        print("Failed to rename python packages. A package has likely already been renamed.")


def get_project_name() -> str:
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    project_name_new = simpledialog.askstring("Input", "Enter project name:", initialvalue=os.path.basename(os.getcwd()))
    return project_name_new


if __name__ == "__main__":
    project_name = get_project_name()
    if project_name:
        update_toml_file(project_name)
        update_python_package_names(project_name)
    else:
        print("No project name entered.")
