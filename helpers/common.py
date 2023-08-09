import yaml
import os

yaml_files = ['settings.yml', 'locators.yml']


class Settings:
    pass


def get_absolute_path(file_name):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.dirname(current_script_directory)
    return os.path.join(project_directory, file_name)


def load_yaml(file):
    with open(file, "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        for section_name, section_data in yaml_data.items():
            setattr(Settings, section_name, section_data)
