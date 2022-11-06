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
    app_commands.Choice(name="PST", value="Etc/GMT+8"),
    app_commands.Choice(name="EST", value="Etc/GMT+4"),
]

tzs = {
    "Etc/GMT+5": "EST",
    "Etc/GMT+8": "PST"
}


class Alarms(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.generator = GenerateTimeString()
        self.check_times.start()
        self.count = 0

    def cog_unload(self):
        self.check_times.cancel()

    @app_commands.command(name="create_alarm", description="Creates an alarm!")
    @app_commands.describe(alarm_time="Format as \"MM/DD hh:mm\"")
    @app_commands.describe(timezone="Timezone the alarm is set to")
    @app_commands.describe(description="Alarm title")
    @app_commands.choices(timezone=time_zone_choices)
    async def create_alarm(self, interaction: discord.Interaction, alarm_time: str, timezone: str, description: str):
        await interaction.response.defer()
        month_day, hour_minutes = alarm_time.split()
        month, day = month_day.split("/")
        hour, minute = hour_minutes.split(":")
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        message1 = await interaction.followup.send(f"Creating alarm!")
        end_date_time = datetime(datetime.now().year, month, day, hour, minute)
        end_time = end_date_time.replace(
            microsecond=0).strftime("%m/%d, %H:%M")
        time_difference = self.get_time_difference(
            end_date_time, datetime.now())
        msg_1_content = f"Alarm set for: {end_time}, {tzs[timezone]}\n"
        msg_2_content = ""
        message2 = None
        if time_difference[0] > 0:
            msg_1_content += self.generator.generate_day_string(
                time_difference[0])
            msg_2_content = self.generator.generate_string(time_difference[1])
        else:
            msg_1_content += self.generator.generate_string(time_difference[1])
        await message1.edit(content=(msg_1_content))
        if time_difference[0] > 0:
            message2 = await self.bot.get_channel(interaction.channel).send(msg_2_content)
        # self.generator.generate_string(time_difference[1])
        await self.bot.get_channel(self.bot.instances_channel).send(f"s {interaction.channel_id} {message1.id} {end_time} {timezone} {description}")
        self.bot.instances["alarms"].append(
            [interaction.channel_id, message1.id, end_time, timezone, description, message2])

    @staticmethod
    def check_time_difference(t1: datetime, t2: datetime) -> bool:
        if t1.month == t2. month and t1.day == t2.day:
            hour_difference = (t1.hour - t2.hour) * 60 * 60
            minute_difference = (t1.minute - t2.minute) * 60
            second_difference = t1.second - t2.second

            total_second_difference = hour_difference + \
                minute_difference + second_difference
            return total_second_difference < 0

        day_difference = t1.day - t2.day
        month_difference = (t1.month - t2.month) * 30
        return day_difference + month_difference < 0

    @staticmethod
    def get_time_difference(t1: datetime, t2: datetime) -> tuple:
        hour_difference = t1.hour - t2.hour
        minute_difference = t1.minute - t2.minute
        second_difference = t1.second - t2.second
        day_difference = t1.day - t2.day
        if second_difference < 0:
            minute_difference -= 1
            second_difference += 60
        if minute_difference < 0:
            hour_difference -= 1
            minute_difference += 60
        if hour_difference < 0:
            day_difference -= 1
            hour_difference += 24
        return day_difference, (hour_difference, minute_difference, second_difference)

    @tasks.loop(seconds=1)  # checks if alarm time is reaching actual time
    async def check_times(self):
        self.count += 1
        alarms_to_be_deleted = []
        for i in range(len(self.bot.instances["alarms"])):
            channel_id, message1_id, end_time, tz, description, message2_id = self.bot.instances[
                "alarms"][i]
            timezone = pytz.timezone(tz)
            current_time = datetime.now(timezone)
            alarm_time = datetime.strptime(
                end_time, "%m/%d, %H:%M").replace(year=current_time.year, tzinfo=timezone)
            if self.check_time_difference(alarm_time, current_time):
                message1 = await self.bot.get_channel(channel_id).fetch_message(message1_id)
                await message1.edit(content=message1.content[:32] + "\n" + self.generator.generate_string((0, 0, 0)))
                await self.bot.get_channel(channel_id).send(f"@everyone **{description}**")
                alarms_to_be_deleted.append(i)
            else:
                if self.count % 3 == 0:
                    got_rid_of_days = await self.count_down_alarm(channel_id, message1_id, alarm_time, 32, current_time, message2_id)
                    if got_rid_of_days:
                        self.bot.instances["alarms"][i] = (
                            channel_id, message1, end_time, tz, description, None)
        for i in range(len(alarms_to_be_deleted)):
            for j in range(i, len(alarms_to_be_deleted)):
                alarms_to_be_deleted[j] -= 1
            self.bot.instances["alarms"].pop(i)

    async def count_down_alarm(self, channel_id: int, message1_id: int, alarm_time: datetime, first_msg_len: int, current_time: datetime, message2_id) -> bool:
        if message2_id is None:
            message = await self.bot.get_channel(channel_id).fetch_message(message1_id)
            first = message.content[:first_msg_len]
            time_difference = self.get_time_difference(
                alarm_time, current_time)
            await message.edit(content=first + "\n" + self.generator.generate_string(time_difference[1]))
        else:
            message1 = await self.bot.get_channel(channel_id).fetch_message(message1_id)
            message2 = await self.bot.get_channel(channel_id).fetch_message(message2_id)
            first = message.content[:first_msg_len]
            time_difference = self.get_time_difference(
                alarm_time, current_time)
            if time_difference[0] > 0:
                await message1.edit(content=first+"\n" + self.generator.generate_day_string(time_difference[0]))
                await message2.edit(content=self.generator.generate_string(time_difference[1]))
            else:
                await message1.edit(content=first+"\n" + self.generator.generate_string(time_difference[1]))
                await message2.delete()
                return True
        return False

    @check_times.before_loop
    async def before_check_times(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Alarms(bot), guilds=[discord.Object(id=1038187258165067836)])
