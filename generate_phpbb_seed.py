import csv
import datetime

from generate_seed_common import generate_email, generate_password


def convert_time_to_int(date_str):
    date_obj = datetime.datetime.strptime(date_str, '%a %b %d, %Y %I:%M %p')
    unix_timestamp = int(date_obj.timestamp())
    return unix_timestamp


with open('phpbb_users.tsv', 'r') as phpbb_users, open('phpbb_export.csv', 'w', newline='') as export:
    tsv_reader = csv.DictReader(phpbb_users, delimiter='\t')
    csv_writer = csv.writer(export)
    # Too lazy to remove headers in PHP import script
    # csv_writer.writerow(['username', 'email', 'password', 'timestamp'])
    for row_i, row in enumerate(tsv_reader):
        username = row['username']
        email = generate_email(username)
        password = generate_password()
        timestamp = convert_time_to_int(row['joined'])
        csv_writer.writerow([username, email, password, timestamp])
