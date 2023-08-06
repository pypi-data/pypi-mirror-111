import json
import subprocess
from pathlib import Path
from typing import Tuple

from flask import session

from rstatmon.session_manager import Session


class Settings():

    def __init__(self):
        self.rootdir = Path(__file__).resolve().parent / "config/settings/"
        self.setting_file_name = "general.json"
        self.setting_file = str(self.rootdir / self.setting_file_name)

    def set_color_theme(self):
        """Sets color properties to session variables.
        """
        with open(self.setting_file, "r") as f:
            data = json.load(f)
        Session.set_session("color_theme", data["general"]["view"]["color"]["background"])
        Session.set_session("color_emp", data["general"]["view"]["color"]["emphasis"])
        Session.set_session("label_font_color", data["general"]["view"]["color"]["label"])
        Bulma().bulma_include(data["general"]["view"]["theme"])

    def write_color_theme(self, color: str, emp: str, label: str, theme: str):
        with open(self.setting_file, "r") as f:
            data = json.load(f)
        data["general"]["view"]["color"]["background"] = color
        data["general"]["view"]["color"]["emphasis"] = emp
        data["general"]["view"]["color"]["label"] = label
        data["general"]["view"]["theme"] = theme
        with open(self.setting_file, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def delete_metadata():
        root_dir = Path(__file__).resolve().parent
        for d in ["static", "templates", "data", "config"]:
            target = str(root_dir / d)
            cmd = f"rm -rf {target}"
            try:
                subprocess.run(cmd.split())
                print(f"Delete {target}")
            except:
                print("Delete failed")
        print("Delete process sucessfully completed.")



class Bulma():

    bulma_color = {
        "dark": "is-dark",
        "white": "is-white",
        "blue": "is-info",
        "green": "is-success",
        "red": "is-danger",
        "yellow": "is-warning",
    }

    bulma_theme = {
        "default": "default",
        "jet": "cyborg",
        "flatly": "darkly",
        "touch": "lux",
        "material": "material",
        "shades": "slate",
        "brave": "superhero"
    }

    def bulma_include(self, theme: str = "default"):
        bulmaswatch = r'<link rel="stylesheet" href="https://unpkg.com/bulmaswatch/{}/bulmaswatch.min.css">'.format(Bulma.bulma_theme[theme])
        Session.set_session("bulmaswatch_theme", theme)
        Session.set_session("bulmaswatch", bulmaswatch)

    def get_bulma_color(self, key: str):
        return Bulma.bulma_color[key]

    def get_bulma_theme(self, key: str):
        return Bulma.bulma_theme[key]

    def get_colors(self) -> Tuple[dict, dict]:
        return Bulma.bulma_color, Bulma.bulma_theme

    def set_color(self, color: str):
        Session.set_session("background_color", color)
