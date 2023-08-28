import argparse
from svmmetider import fetch_and_dump_ics
from update_g_calandars import sync_cal_to_ics
import json
import os
from datetime import datetime, timedelta


# def fetch_handler(args):
#     fetch_and_dump_ics()
def push_handler(args):
    def is_in_sync_date_time_range(d):
        return datetime.today() - timedelta(
            days=31 * args.from_month) < d < datetime.today() + timedelta(days=31 * args.to_month)

    if args.fetch:
        fetch_and_dump_ics(entry_filter=is_in_sync_date_time_range)

    from google.oauth2 import service_account
    info = None
    if args.token_file:
        with open(args.token_file) as source:
            info = json.load(source)
    elif args.token_env:
        info = json.loads(os.getenv(args.token_env))
    else:
        print("Token must be specified")
        exit(1)

    if info is not None:
        creds = service_account.Credentials.from_service_account_info(info)

        sync_cal_to_ics('cnc7r2d4qfhp0qhu5js17l91bc@group.calendar.google.com', 'swimming_meet_odder.ics', creds,
                        full_refresh=False, entry_filter=is_in_sync_date_time_range)
        sync_cal_to_ics('jhpu1liovjefu5mbj5ui4uj8j4@group.calendar.google.com', 'swimming_meet_jylland.ics', creds,
                        full_refresh=False, entry_filter=is_in_sync_date_time_range)
        sync_cal_to_ics('ui9jr9vao6nacsckiss2ri1g50@group.calendar.google.com', 'swimming_meet.ics', creds,
                        full_refresh=False, entry_filter=is_in_sync_date_time_range)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG')

    subparsers = parser.add_subparsers(help='sub-command help')

    # a_parser = subparsers.add_parser("fetch")
    # a_parser.set_defaults(func=fetch_handler)
    b_parser = subparsers.add_parser("push")
    b_parser.add_argument("--fetch", action='store_true')
    b_parser.add_argument("--token-env", dest='token_env', type=str, default=None)
    b_parser.add_argument("--token-file", dest='token_file', type=str, default=None)
    b_parser.add_argument('--from-months', dest='from_month', type=int, default=3)
    b_parser.add_argument('--to-months', dest='to_month', type=int, default=12)
    b_parser.set_defaults(func=push_handler)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
