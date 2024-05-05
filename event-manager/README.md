# Automation to create events across Google Calendar & Discord


## Description

This script creates events across [Google Calendar](https://developersindia.in/events-calendar/) & [Discord](https://discord.com/channels/669880381649977354/)

### First Time Setup

1. Get Python3

   ```bash
   sudo apt-get install python3 && python3 --version
   ```

2. Install required packages

   ```bash
   pip install -r requirements.txt
   ```

3. Add respective tokens in the `.env` file

   ```bash
   cp .sample.env .env
   ```

   1. `DISCORD_BOT_TOKEN`
      - Get it from [Discord Developers portal](https://discord.com/developers/applications/)) (bot must have MANAGE_EVENT & CREATE_EVENT permission)

   2. `DISCORD_GUILD_ID`
      - developersIndia's GUID is `1229786646468362260`

   3. `GOOGLE_CALENDAR_ID`
      - developersIndia calendar is public, `9f1337e4154910eb1bdb3bfac32b88f69546468b1281a6db58f50a909df5049f@group.calendar.google.com`

4. Connect Google calendar through [Google cloud Console](https://console.cloud.google.com/)
   1. 4.1 Create a Project on Google Cloud Console
   2. Search for calendar API and enable it
   3. Create Credentials ->  OAuth Client ID -> Application type as Desktop
   4. Download the JSON file
   5. Rename that JSON file as `credentials.json` and save it to the project directory.

5. `python3 main.py`

---

### NOTES-

> - Google authenication is required for the first time.
> 
> - A file `token.json` will be downloaded automatically, and no web login will be needed afterwards.
