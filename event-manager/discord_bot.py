from datetime import datetime, timedelta
import discord
from discord.ext import commands


def create_discord_event(
    bot_token,
    guild_id,
    EVENT_NAME,
    EVENT_DESCRIPTION,
    EVENT_LOCATION,
    EVENT_DATE,
    EVENT_START_TIME,
    EVENT_END_TIME,
):

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

    @bot.event
    async def on_ready():

        # Convert the date string to a datetime object
        date_object = datetime.strptime(EVENT_DATE, "%Y-%m-%d")

        # Convert the time string to a datetime object
        start_time_object = datetime.strptime(EVENT_START_TIME, "%H:%M")
        end_time_object = datetime.strptime(EVENT_END_TIME, "%H:%M")

        # Combine the date and time objects
        st = date_object.replace(
            hour=start_time_object.hour, minute=start_time_object.minute
        ).astimezone()
        et = date_object.replace(
            hour=end_time_object.hour, minute=end_time_object.minute
        ).astimezone()

        gg = bot.get_guild(guild_id)

        try:
            event = await gg.create_scheduled_event(
                name=EVENT_NAME,
                entity_type=discord.EntityType.external,
                description=EVENT_DESCRIPTION,
                start_time=st,
                end_time=et,
                location=EVENT_LOCATION,
                privacy_level=discord.PrivacyLevel.guild_only,
            )
            print("Discord Event created: ", event.url)

        except Exception as e:
            print(e)

        await bot.close()

    # Run the bot
    bot.run(bot_token)
