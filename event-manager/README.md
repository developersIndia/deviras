# Automation to create events across channels (google calendar & discord)
#### by [Rancho-rachit](https://github.com/Rancho-rachit)

---

### Description:

This script creates events across -
1. [Google Calendar](https://developersindia.in/events-calendar/)  
2. [Discord](https://discord.com/channels/669880381649977354/)

---

### FIRST TIME SETUP

1. Get Python3 `sudo apt-get install python3 && python3 --version`

2. Install required packages `pip install -r requirements.txt`

3. Add respective tokens in the `.env` file

   3.1 Discord Bot token [`DISCORD_BOT_TOKEN`] (Get it from [Discord Developers portal](https://discord.com/developers/applications/)) (bot must have MANAGE_EVENT & CREATE_EVENT permission)

   3.2 Guild ID [`DISCORD_GUILD_ID`] (developersIndia => `1229786646468362260`)

   3.3 calendar Id [`GOOGLE_calendar_ID`] (developerIndia => `9f1337e4154910eb1bdb3bfac32b88f69546468b1281a6db58f50a909df5049f@group.calendar.google.com`)

4. Connect Google calendar through [Google cloud Console](https://console.cloud.google.com/)

    4.1 Create a Project on Google Cloud Console
   
    4.2 Search for calendar API and enable it

    4.3 Create Credentials ->  OAuth Client ID -> Application type as Desktop

    4.4 Download the Json file 

    4.5 Rename that JSON file as `credentials.json` and save it to the project directory.

5. `python3 main.py` 

---

### NOTES-

> - Google authenication is required for the first time.
> 
> - A file `token.json` will be downloaded automatically, and no web login will be needed afterwards.

<!-- END -->
