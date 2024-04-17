from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import event_details
import discord
from discord.ext import commands

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')
guild_id = int(os.getenv('DISCORD_GUILD_ID'))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():

    # Convert the date string to a datetime object
    date_object = datetime.strptime(event_details.EVENT_DATE, "%Y-%m-%d")

    # Convert the time string to a datetime object
    start_time_object = datetime.strptime(event_details.EVENT_START_TIME, "%H:%M")
    end_time_object = datetime.strptime(event_details.EVENT_END_TIME, "%H:%M")

    # Combine the date and time objects
    st = date_object.replace(hour=start_time_object.hour, minute=start_time_object.minute).astimezone()
    et = date_object.replace(hour=end_time_object.hour, minute=end_time_object.minute).astimezone()

    gg = bot.get_guild(guild_id)

    try:
        event = await gg.create_scheduled_event(
            name=event_details.EVENT_NAME, 
            entity_type=discord.EntityType.external, 
            description=event_details.EVENT_DESCRIPTION,
            start_time=st,
            end_time=et, 
            location=event_details.EVENT_LOCATION, 
            privacy_level=discord.PrivacyLevel.guild_only,
            )      
        print("Discord Event: ", event.url)
        
    except Exception as e:
        print(e)
        
    await bot.close()
    
# Run the bot
bot.run(bot_token)

# END