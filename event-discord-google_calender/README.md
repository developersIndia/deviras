# Automation to create events across channels (google calendar & discord)
#### by [Rancho-rachit](https://github.com/Rancho-rachit)

---

## Description:

This script creates events across -
1. [Google Calendar](https://developersindia.in/events-calendar/)  
2. [Discord](https://discord.com/channels/669880381649977354/)

---

### FIRST TIME SETUP

1. Get Python3 `sudo apt-get install python3 && python3 --version`

2. Install required packages `pip install -r packages.txt`

3. Add respective tokens in the `.env` file
    2.1 Discord Bot token (Get it from [Discord Developers portal](https://discord.com/developers/applications/)) (bot must have MANAGE_EVENT & CREATE_EVENT permission)
    2.2 Guild ID (developersIndia => 1229786646468362260)

3. Connect Google Calender through [Google cloud Console](https://console.cloud.google.com/)
    3.1 Create a Project on Google Cloud Console
    3.2 Search for Calender API and enable it
    3.3 Create Credentials ->  OAuth Client ID -> Application type as Desktop
    3.4 Download the Json file 
    3.5 Rename that JSON file as `credentials.json` and save it to the project directory.

4. `python3 main.py` 

---

### NOTES-

> - Google authenication is required for the first time.
> 
> - A file `token.json` will be downloaded automatically, and no web login will be needed afterwards.

<!-- END -->