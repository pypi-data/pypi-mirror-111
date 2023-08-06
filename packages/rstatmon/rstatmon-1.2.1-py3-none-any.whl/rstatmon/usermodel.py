import sys
import shutil
import json
import subprocess
from typing import Union
from pathlib import Path
from jinja2 import Template


class UserModel():
    """Handles user-defined model described in python scripts.
    """

    def __init__(self):
        self.parent = Path(__file__).resolve().parent
        self.dst = self.parent / "config/user_model/"
        self.model_json = self.dst / "user_model.json"
        self.user_model_key = "user_model"
        self.current_model_key = "current_model"
        self.models = []
        self.import_models()

    def register_model(self, src: str):
        """Register a specified model as new one.

        Args:
            src (str): The file path to register.
        """
        src_abs = Path(src).resolve()
        self.validate_model(src_abs)
        shutil.copy(src_abs, self.dst)
        self.set_current_model(src_abs)
        self.update_json()

    def delete_model(self, src: str):
        """Delete python file corresponding to model in the dst dir.

        Args:
            src (str): File name of python to delete
        """
        path = self.parent / src
        if path.exists():
            path.unlink(src)
        self.update_json()

    def validate_model(self, path: Path) -> bool:
        if path.suffix != ".py":
            print(
                "\033[31mThe file you're trying to add have no suffix 'py'\033[0m",
                file=sys.stderr)
            sys.exit(-1)
        cmd = f"python {path}"
        ret = subprocess.check_output(cmd.split()).decode("utf-8").strip("\n")
        try:
            f = float(ret)
            int(f)
            return True
        except ValueError:
            print(
                "\033[31mThe type of return value isn't int or float\033[0m",
                file=sys.stderr)
            sys.exit(-1)

    def update_json(self):
        """Update model json

        Json consists of key and value. In case of "test.py" model, key and
        value are as follows respectively.
        test : test.py

        """
        files = list(self.dst.glob("*.py"))
        contens = {}
        tmp = []
        for i in files:
            tmp.append(str(i.stem))
        contens[self.user_model_key] = tmp

        # load the current model in json
        current = self.get_current_model()
        if current:
            contens["current_model"] = str(Path(current).stem)
        else:
            contens["current_model"] = ""

        # write the registered models and current model into json
        with open(str(self.model_json), "w") as f:
            json.dump(contens, f, indent=4)

    def set_current_model(self, model: Union[Path, str]):
        if type(model) == str:
            pass
        else:
            model = str(model.stem)
        if self.model_json.exists():
            with open(str(self.model_json), "r") as f:
                j = json.load(f)
                j[self.current_model_key] = model
            with open(str(self.model_json), "w") as f:
                json.dump(j, f, indent=4)

    def remove_current_model(self):
        if self.model_json.exists():
            with open(str(self.model_json), "r") as f:
                j = json.load(f)
                j[self.current_model_key] = ""
            with open(str(self.model_json), "w") as f:
                json.dump(j, f, indent=4)

    def import_models(self) -> list:
        if self.model_json.exists():
            with open(str(self.model_json), "r") as f:
                j = json.load(f)
                self.models = j[self.user_model_key]
                return self.models
        return []

    def get_value(self):
        f = self.get_current_model()
        return self.execute(f)

    def get_current_model(self) -> str:
        """Gets a file name corresponding to the model.

        Returns:
            str: The file name in the format of abs path.
        """
        if self.model_json.exists():
            with open(str(self.model_json), "r") as f:
                j = json.load(f)
            if self.current_model_key in j:
                current_model = j[self.current_model_key]
                if current_model:
                    self.py_file = self.parent / current_model
                    return str(self.py_file)
        return None

    def execute(self, pyfile: str):
        """Execute model file.

        Args:
            pyfile (str): The model file.
        """
        if Path(pyfile).suffix != ".py":
            pyfile += ".py"
        cmd = f"python {pyfile}"
        ret = subprocess.check_output(cmd.split()).decode("utf-8").strip("\n")
        return ret


class JinjaTemplate():

    def __init__(self, data: dict):
        self.data = data
        self.parent = Path(__file__).resolve().parent
        self.model_prop = self.parent / "config/user_model/model_prop.json"
        self.body = self.parent / "templates/jinja/body.html"
        self.dst = self.parent / "templates/user_model.html"
        self.org = self.parent / "templates/user_model.html.org"

    def parse_dict(self):
        dct = {}
        colors = ["red", "blue", "yello", "green"]
        it = iter(colors)
        for key, value in self.data.items():
            key_words = key.split("_")
            if len(key_words) == 1 and not key_words[0] == "datasets":
                dct[key_words[0]] = self.parse_int(value)
            elif len(key_words) == 2:
                if not key_words[0] in dct.keys():
                    dct[key_words[0]] = {}
                dct[key_words[0]][key_words[1]] = self.parse_int(value)
                if key_words[0] == "datasets":
                    dct[key_words[0]]["color"] = next(it)
            else:
                pass
        if "add" in dct.keys():
            dct.pop("add")
        self.json_data = dct
        with open(str(self.model_prop), "w") as f:
            json.dump(self.json_data, f, indent=4)

    def parse_int(self, data):
        try:
            return int(data)
        except ValueError:
            return data

    def load_body(self):
        with open(str(self.body), "r") as f:
            s = f.read()
        temp = Template(s)
        body = {"body": temp.render(self.json_data)}
        return body

    def load_template(self, body: dict):
        tmp = """
        {%- raw %}
        {% extends "layout.html" %}
        {% block content %}
        {%- endraw %}
        {{ body }}
        {%- raw %}
        {% endblock %}
        {%- endraw %}
        """
        temp = Template(tmp)
        html = temp.render(body)
        return html

    def make_template(self):
        self.parse_dict()
        body = self.load_body()
        html = self.load_template(body)
        UserModel().set_current_model(self.data["model"])
        self.writer(html)

    def writer(self, data: str):
        with open(str(self.dst), "w") as f:
            f.write(data)

    def remove_model(self):
        shutil.copy(self.org, self.dst)

