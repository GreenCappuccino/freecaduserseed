import csv
import random

from generate_seed_common import generate_password, generate_email


# Define a function to generate random names
def generate_name():
    first_names = ["John", "Jane", "Jonnie", "Alice", "Bob", "Charlie", "David", "Eve"]
    last_names = ["Doe", "Smith", "Jones", "Johnson", "Brown", "Davis", "Miller", "Wilson"]
    return random.choice(first_names) + " " + random.choice(last_names)


# Define a function to generate random role combinations
def generate_roles():
    roles = ["editor", "staff", "admin", "bureaucrat"]
    return random.sample(roles, random.randint(1, len(roles)))


# Open the TSV file and create a CSV file
with open("wiki_users.tsv", newline="") as wiki_users, open("wiki_export.csv", mode="w", newline="") as export:
    reader = csv.DictReader(wiki_users, delimiter="\t")
    writer = csv.writer(export)

    # Write the header row
    writer.writerow(["username", "password", "email", "name", "roles"])

    # Loop through each row in the TSV file and write a corresponding row to the CSV file
    for i, row in enumerate(reader):
        username = row["name"]
        password = generate_password()
        email = generate_email(username)
        name = generate_name()
        roles = generate_roles()
        writer.writerow([username, password, email, name] + roles)
