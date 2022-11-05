# Currently doesn't save the data


import discord
from discord.ext import tasks
from discord import app_commands
from discord.ext import commands, tasks
import interactions
import pytz
from datetime import datetime, timedelta
import csv
from helpers.generate_time import GenerateTimeString

# change these var to yours
# token = 'MTAzODMxNDY0MzA1MzA5Mjk0NQ.GaGciB.ziX1NGcMHftg8Pg6iM-FgP2aaO8exEzH16Mi5E'
# guild_id = 1010397037424033942
# bot = interactions.Client(token)

# timezone = pytz.timezone("America/Vancouver")
time_zone_choices = [
    app_commands.Choice(
        name="Vancouver", value="America/Vancouver"),
    app_commands.Choice(name="UTC", value="UTC"),
    app_commands.Choice(name="EST", value="Canada/Eastern"),
]


class Alarms(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.check_times.start()

    def cog_unload(self):
        self.check_times.cancel()

    @app_commands.command(name="create_alarm", description="Creates an alarm!")
    @app_commands.describe(alarm_time="Format as \"MM/DD hh:mm\"")
    @app_commands.describe(timezone="Timezone the alarm is set to")
    @app_commands.choices(timezone=time_zone_choices)
    async def create_alarm(self, interaction: discord.Interaction, alarm_time: str, timezone: str):
        await interaction.response.defer()
        month_day, hour_minutes = alarm_time.split()
        month, day = month_day.split("/")
        hour, minute = hour_minutes.split(":")
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        message = await interaction.followup.send(f"Creating alarm!")
        end_time = datetime(datetime.now().year, month, day, hour, minute).replace(
            microsecond=0).strftime("%m/%d, %H:%M")
        await message.edit(content=("Alarm set for: " + end_time))
        await self.bot.get_channel(self.bot.instances_channel).send(f"s {interaction.channel_id} {message.id} {end_time} {timezone}")
        self.bot.instances["alarms"].append(
            [interaction.channel_id, message.id, end_time, timezone])

    @tasks.loop(seconds=5)  # checks if alarm time is reaching actual time
    async def check_times(self):
        alarms_to_be_deleted = []
        for i in range(len(self.bot.instances["alarms"])):
            channel_id, message_id, end_time, tz = self.bot.instances["alarms"][i]
            alarm_time = datetime.strptime(end_time, "%m/%d, %H:%M")
            timezone = pytz.timezone(tz)
            timediff = alarm_time.astimezone(
                timezone) - datetime.now().astimezone(timezone)
            if timediff.total_seconds() < 1:
                await self.bot.get_channel(channel_id).send("AHHHHHHHHHHH")
                alarms_to_be_deleted.append(i)
        for i in range(len(alarms_to_be_deleted)):
            for j in range(i, len(alarms_to_be_deleted)):
                alarms_to_be_deleted[j] -= 1
            self.bot.instances["alarms"].pop(i)

    @check_times.before_loop
    async def before_check_times(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Alarms(bot), guilds=[discord.Object(id=1038187258165067836)])


# @bot.event  # bot is online
# async def on_ready():
#     print(f"logged in")


# @bot.command(  # alarm slash command
#     name="alarm",
#     description="set an alarm",
#     scope=guild_id,
#     options=[
#         interactions.Option(
#             name="hour",
#             description="input hour in 24hr format",
#             type=4,  # interactions.OptionType.INTEGER
#             required=True,
#         ),
#         interactions.Option(
#             name="min",
#             description="input minutes",
#             type=4,  # interactions.OptionType.INTEGER
#             required=True,
#         ),
#         interactions.Option(
#             name="name",
#             description="what is this alarm for?",
#             type=3,  # interactions.OptionType.STRING
#             required=True,
#         ),
#     ]
# )
# Trying to save user input data below not working
# @bot.event
# async def on_alarm_create(alarmC):
#    name = alarmC.name
#    alarm_hour = alarmC.hour.astimezone(timezone).strftime('%m %d %H:%M')
#    alarm_min = alarmC.min.astimezone(timezone).strftime('%m %d %H:%M')
#    alarm_time = alarm_hour + ":" + alarm_min
#    with open("data.csv", "alarms") as f:
#        csv_writer = csv.writer(f, delimiter="~", lineterminator='\n')
#        csv_writer.writerow([name, alarm_time])
#    await print_scheduled_event(alarmC)
# ignore for now
