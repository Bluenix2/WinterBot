# Winter Bot

Discord bot managing the [Project Winter server](https://discord.gg/projectwinter),
containing multiple ticket systems, reaction roles, tags and other server specific features.
This is not developed or maintained by Other Ocean officially,
but voluntarily by the Community Moderator Bluenix.

## Requirements

* Python 3.7.9 or newer
* PostgreSQL 13

## Installation

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

    Then use the `psql` to also execute `init.sql`.

5. **Set up main file**

    Use the following template to set up your own main file:

    ```python
    from fastapi import FastAPI

    from bot import Config, WinterBot

    # Your IDE should show other options you may have available.
    config = Config(client_id=123, token='123')

    app = FastAPI()
    bot = WinterBot(app, config)
    app.bot = bot

    bot.run()
    ```
