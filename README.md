# Winter Bot

Discord bot managing the [Project Winter server](https://discord.gg/projectwinter),
containing multiple ticket systems, reaction roles, tags and other server specific features.
This is not developed or maintained by Other Ocean officially,
but voluntarily by the Community Moderator Bluenix.

## Requirements

* Python 3.7.9 or newer
* PostgreSQL 13

## Installation

### Bot Installation

1. **Install requirements**

    Install Python 3.7.9 or newer and PostgreSQL 13.

2. **Set up venv**

    This is easily done using `python -m venv venv`.

3. **Install dependencies**

    Use the requirements.txt file, `pip install -U -r requirements.txt`.

4. **Create the PostgreSQL database**

    Using the `psql` tool, execute the following queries:

    ```sql
    CREATE ROLE winterbot WITH LOGIN PASSWORD 'yourpw';
    CREATE DATABASE winterdb OWNER winterbot;
    ```

5. **Set up configuration**

    The bot uses a `config.py` file for configuration of credentials.
