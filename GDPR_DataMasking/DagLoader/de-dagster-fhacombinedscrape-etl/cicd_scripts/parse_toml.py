import os
import tomlkit
from dotenv import dotenv_values

# Define the paths to the TOML and dotenv files
pyproject_toml_path = "pyproject.toml"
dotenv_path = "variables_new.env"

# Parse the pyproject.toml file and extract the 'name' field
try:
    with open(pyproject_toml_path, "r") as toml_file:
        toml_data = tomlkit.parse(toml_file.read())
    project_name = toml_data["tool"]["poetry"]["name"]
    dagster_module_name = toml_data["tool"]["dagster"]["module_name"]
except (FileNotFoundError, KeyError):
    print("Error: Unable to parse pyproject.toml or find the 'module_name' field.")
    exit(1)

# Check if the dotenv file already exists
if os.path.isfile(dotenv_path):
    existing_env = dotenv_values(dotenv_path)
    
    if "PROJECT_NAME" in existing_env:
        print("Warning: 'PROJECT_NAME' already exists in the dotenv file. Skipping write.")
    else:
        with open(dotenv_path, "a") as dotenv_file:
            dotenv_file.write(f"\nPROJECT_NAME={project_name}\n")
        print(f"'PROJECT_NAME={project_name}' written to {dotenv_path}")
    
    if "DAGSTER_MODULE_NAME" in existing_env:
        print("Warning: 'DAGSTER_MODULE_NAME' already exists in the dotenv file. Skipping write.")
    else:
        with open(dotenv_path, "a") as dotenv_file:
            dotenv_file.write(f"\nDAGSTER_MODULE_NAME={dagster_module_name}\n")
        print(f"'DAGSTER_MODULE_NAME={dagster_module_name}' written to {dotenv_path}")
else:
    with open(dotenv_path, "w") as dotenv_file:
        dotenv_file.write(f"PROJECT_NAME={project_name}\n")
        dotenv_file.write(f"DAGSTER_MODULE_NAME={dagster_module_name}\n")
    print(f"'PROJECT_NAME={project_name}' written to {dotenv_path}")
    print(f"'DAGSTER_MODULE_NAME={dagster_module_name}' written to {dotenv_path}")
