#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import signal
import sys
from multiprocessing import Process
from flask_login import LoginManager
from pathlib import Path

from rstatmon.general import Settings
from rstatmon.database import User, db, DBInit
from rstatmon.statdata import routine
from rstatmon.usermodel import UserModel
from rstatmon.application import app
import rstatmon.routes

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        help="debug",
        action='store_true'
    )
    parser.add_argument(
        '-c',
        '--create',
        help="Create a new database, table and admin user.",
        action='store_true'
    )
    parser.add_argument(
        '-n',
        '--new',
        type=str,
        help='Register a new user-defined model.'
    )
    parser.add_argument(
        '--remove',
        help="Remove the data",
        action='store_true'
    )
    args = parser.parse_args()
    if args.new:
        model = UserModel()
        model.register_model(args.new)
        print("register :", args.new)
        parser.exit()

    if args.create:
        try:
            js = Path(__file__).resolve().parent / "config/database.json"
            d = DBInit()
            d.read_json(js)
            d.db_setup()
        except FileNotFoundError:
            print(
                "\033[31mThere is no database file.\n" +
                "Execute rstatmon-setup before this step.\033[0m",
                file=sys.stderr)
        except:
            print(
                "\033[31mFailed to create the database.\033[0m",
                file=sys.stderr)
        finally:
            parser.exit()

    if args.remove:
        print("Do you really remove the all data? (yes/[no]):", end="")
        ans = input().strip()
        if ans == "yes":
            DBInit().delete_database()
            Settings.delete_metadata()
        else:
            print("quit")
        parser.exit()

    #signal.signal(signal.SIGINT, signal_handler)
    p = Process(target=routine, args=(args.debug,))
    p.start()
    #parent_pid = os.getpid()
    #child_id = p.pid


    if args.debug:
        app.config["TEST"] = True
        app.run(debug=True, threaded=True)
    else:
        app.run(debug=False, threaded=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
