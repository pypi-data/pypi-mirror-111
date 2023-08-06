#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--password',
        type=str,
        help='password'
    )
    parser.add_argument(
        '--port',
        type=str,
        default="3306",
        help='port'
    )
    parser.add_argument(
        "-s",
        '--server',
        type=str,
        default="localhost",
        help='server name'
    )
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        default="root",
        help='user name'
    )
    args = parser.parse_args()
    if args.user and args.password:
        data = {
            "username": args.user,
            "password": args.password,
            "server": args.server,
            "port": args.port,
            "db_name": "raspi"
        }
        j = Path(__file__).resolve().parent / "config/database.json"
        with open(str(j), mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("-" * 60)
        for key, val in data.items():
            print(f"{key:<10}: {val}")
        print("-" * 60)
        print("register success")
        print("The information about database is written in the following file.")
        print(j)
    else:
        print(
            "\033[31mUsername or password is empty.\033[0m",
            file=sys.stderr)
        parser.print_help()
    parser.exit()


if __name__ == '__main__':
    main()