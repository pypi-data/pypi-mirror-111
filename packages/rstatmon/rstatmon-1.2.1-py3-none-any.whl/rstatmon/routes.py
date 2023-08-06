"""Routing module
"""
import json
from pathlib import Path

from flask import (
    render_template, url_for, flash, redirect, request, jsonify, abort, session
)
from flask_login import login_user, current_user, logout_user, login_required

from rstatmon.mylogger import MyLogger
from rstatmon.statdata import Hardware, StatData
from rstatmon.auth import RegistrationForm, LoginForm
from rstatmon.database import User
from rstatmon.passhash import bcrypt
from rstatmon.database import db
from rstatmon.usermodel import UserModel, JinjaTemplate
from rstatmon.session_manager import Session
from rstatmon.general import Settings, Bulma
from rstatmon.application import app


@app.route("/")
def root():
    Settings().set_color_theme()
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form = LoginForm(meta={'csrf': False})
        if not form.check_validate():
            MyLogger().write_log(f"{request.remote_addr} : login failed", "error")
            return render_template('login.html', title='Login', form=form, address=request.remote_addr)
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash("The user doesn't exist.", "danger")
            MyLogger().write_log(f"{request.remote_addr} : login failed", "error")
            return render_template('login.html', title='Login', form=form, address=request.remote_addr)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            MyLogger().write_log(f"{request.remote_addr} : login success", "success")
            return redirect(url_for("home"))
        else:
            flash("The password is incorrect.", "danger")
            MyLogger().write_log(f"{request.remote_addr} : login failed", "error")
            return render_template('login.html', title='Login', form=form, address=request.remote_addr)
    return render_template('login.html', title='Login', address=request.remote_addr)


@app.route('/register', methods=["GET", 'POST'])
def register():
    if request.remote_addr != "127.0.0.1":
        abort()

    if request.method == "POST":
        form = RegistrationForm(meta={'csrf': False})
        if form.check_validate():
            username = request.form.get("username")
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Input user already exists.', "danger")
                return redirect(url_for('register'))
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                password=hashed_password)
            user_id = 1
            while user_id < 1000:
                if not User.query.filter_by(user_id=user_id).first():
                    break
                user_id += 1
            user.user_id = "{:03}".format(user_id)
            db.session.add(user)
            db.session.commit()
            flash("The account has been created!", "success")
            MyLogger().write_log("{} : created account".format(request.remote_addr), "success")
            return redirect(url_for("login"))
        else:
            return render_template('register.html', title='Register', form=form)
    else:
        return render_template('register.html', title='Register')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    MyLogger().write_log("{} : logout success".format(request.remote_addr), "success")
    return render_template("logout.html", title="Logout")


@app.route("/home")
@login_required
def home():
    hard = Hardware()
    info = hard.get_hard_info()
    settings = Path(__file__).resolve().parent / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
        Session.set_session("graph", json_data)
    return render_template("home.html", title="Home", data=info, graph=json_data)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='profile')


@app.route('/user_model')
@login_required
def user_model():
    settings = Path(__file__).resolve().parent / "config/user_model/model_prop.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    return render_template('user_model.html', title='user_model', graph=json_data)


@app.route('/model_value', methods=["POST", "GET"])
@login_required
def model_value():
    model = UserModel()
    data = {"data": model.get_value()}
    return jsonify(ResultSet=json.dumps(data))


@app.route('/add')
@login_required
def add():
    model = UserModel()
    model_name = model.models
    return render_template(
        'add_pyfile.html',
        title='add_pyfile',
        model_list=model_name)


@app.route("/add_graph", methods=["GET", "POST"])
@login_required
def add_graph():
    if request.method == "POST":
        j = JinjaTemplate(request.form)
        j.make_template()
        msg = "The new model has been added."
        return render_template('result.html', title='result', msg=msg)
    return render_template('add_pyfile.html', title='add_pyfile')


@app.route("/remove_model", methods=["GET", "POST"])
@login_required
def remove_model():
    j = JinjaTemplate(request.form)
    j.remove_model()
    UserModel().remove_current_model()
    msg = "The current model has been removed."
    return render_template('result.html', title='result', msg=msg)


@app.route('/setting')
@login_required
def setting():
    settings = Path(__file__).resolve().parent / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    return render_template('settings.html', title='Settings', data=json_data)


@app.route("/change_settings", methods=["POST"])
@login_required
def change_settings():
    p = Path(__file__).resolve().parent
    settings = p / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)

    params = request.form
    chart_type = params["chartType"]
    ret, msg = StatData().check_input_params(params, chart_type)
    if not ret:
        error = {chart_type: msg}
        return render_template(
            'settings.html',
            title='Settings',
            data=json_data,
            msg=error)
    for key, val in params.items():
        if "_" in key:
            k1, k2 = key.split("_")
            json_data["chart"][chart_type][k1][k2] = int(val)

    with open(settings, "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    # update settings
    with open(settings, "r") as f:
        json_data = json.load(f)
        Session.set_session("graph", json_data)
    msg = {chart_type: "Successsfully changed."}
    MyLogger().write_log("{} : changed settings".format(request.remote_addr), "success")
    return render_template(
        'settings.html',
        title='Settings',
        data=json_data,
        msg=msg)


@app.route("/chart-data", methods=["POST", "GET"])
def chart_data():
    if app.config["TEST"]:
        json_data = StatData().get_dummydata()
    else:
        json_data = StatData().get_alldata()
    return jsonify(ResultSet=json.dumps(json_data))


@app.route("/read_json", methods=["POST", "GET"])
@login_required
def read_json():
    settings = Path(__file__).resolve().parent / "config/settings/settings.json"
    with open(settings, "r") as f:
        json_data = json.load(f)
    return jsonify(ResultSet=json.dumps(json_data))


@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    try:
        username = request.form["user"]
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.username == current_user.username:
                    flash(f"The user '{username}' is currently logged in", 'danger')
                else:
                    db.session.delete(user)
                    db.session.commit()
                    flash(f"The user '{username}' has been deleted",'success')
                    MyLogger().write_log(f"{request.remote_addr} : deleted account", "success")
            else:
                flash(f"The user '{username}' doesn't exist.")
                MyLogger().write_log(f"{request.remote_addr} : failed to delete account", "error")
            users = User.query.all()
            return render_template("delete.html", title="Delete account", form=users)
    except:
        users = User.query.all()
        return render_template("delete.html", title="Delete account", form=users)


@app.route("/theme", methods=["POST", "GET"])
@login_required
def theme():
    if request.method == "POST":
        print(request.form)
        color = request.form.get("color")
        emp = request.form.get("emp")
        theme = request.form.get("theme")
        label = request.form.get("label")
        b = Bulma()
        b.set_color(color)
        color_name = b.get_bulma_color(color)
        setting = Settings()
        setting.write_color_theme(color_name, emp, label, theme)
        setting.set_color_theme()

    colors, themes = Bulma().get_colors()
    return render_template("setting_theme.html", colors=colors, themes=themes)


@app.route("/plot", methods=["POST", "GET"])
@login_required
def plot():
    days = StatData().exist_logs()
    return render_template("calendar.html", date_list=days, result={})


@app.route("/plot_data", methods=["POST"])
@login_required
def plot_data():
    if request.method == "POST":
        date = request.form.get("date")
        rate = request.form.get("rate")
        unit = request.form.get("unit")
        start = request.form.get("start")
        end = request.form.get("end")

        stat = StatData()
        if not stat.time_validate(start, end):
            flash(
                "The format of Start or End is invalid.",
                "danger")
            days = StatData().exist_logs()
            return render_template("calendar.html", date_list=days)

        start_hour = int(start[0])
        start_min = int(start[1])
        end_hour = int(end[0])
        end_min = int(end[1])
        sampling_rate = stat.get_sampling_rate(rate, unit)
        json_data = stat.read_log(stat.get_date(date), sampling_rate)
        year, month, day = stat.get_date(date, True)
        json_data["year"] = int(year)
        json_data["month"] = int(month)
        json_data["day"] = int(day)
        json_data["start"] = f"{year}-{month}-{day} {start_hour}:{start_min}"
        json_data["end"] = f"{year}-{month}-{day} {end_hour}:{end_min}"
        days = StatData().exist_logs()
        return render_template("calendar.html", date_list=days, result=json_data)
    return render_template("calendar.html", date_list=days)
