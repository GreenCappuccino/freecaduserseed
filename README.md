The intention of this project is to generate a test environment for the purposes of user account migration of certain
FreeCAD infrastructure.

# Setting up

- `poetry install`
- `poetry run pre-commit install`
- Enter venv: `poetry shell`

# Getting Original User Data

- MediaWiki: `python get_wiki_users.py` (Creates `wiki_users.tsv`)
    - Alternatively, download pre-generated files: https://s3.shamrock.systems/data-archive/wiki_users.tsv
- phpBB: `python get_phpbb_users.py` (Create `phpbb_users.tsv`)
    - Alternatively, download pre-generated files: https://s3.shamrock.systems/data-archive/phpbb_users.tsv

# Generating Seed Data

- MediaWiki: `python generate_wiki_seed.py` (Creates `wiki_export.csv`)
- phpBB: `python generate_phpbb_seed.py` (Creates `phpbb_export.csv`)

# Set up local test environment

- phpBB
    - `cd phpbb/`
    - `podman-compose up`
    - To bring down: `podman-compose down`
    - To bring down and delete volumes: `podman-compose down -v`
- MediaWiki (TBA)

# Seed data

- phpBB
    - Ensure phpBB server running
    - `cd phpbb/`
    - `./seedimport.sh`
- MediaWiki (TBA)
