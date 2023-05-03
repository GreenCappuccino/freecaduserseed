# Define a function to generate random email addresses
import random
import string


def generate_email(username):
    domains = ["example.com", "example.org", "example.net"]
    return username + "@" + random.choice(domains)

# Define a function to generate random passwords
def generate_password(length=12):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

