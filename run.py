import sys
sys.path.insert(1, 'settings/')
import config
import disnake
from disnake.ext import commands
from os import listdir
from asyncio import create_task, run
from enum import Enum

class Cogss(str, Enum):
    Basic = 'basic'
    Music = 'music'
    Support = 'support'
    Moder = 'moder'


bot = commands.InteractionBot(activity=disnake.Game(name="нарды"))
intents = disnake.Intents.all()
client = disnake.Client()

@bot.slash_command(name="load", description="FOR ADMINS")
@commands.is_owner()
async def load(inter, extension: Cogss):
    bot.load_extension(f"commands.{extension}")
    await inter.response.send_message("Cogs loaded")

@bot.slash_command(name="unload", description="FOR ADMINS")
@commands.is_owner()
async def unload(inter, extension: Cogss):
    bot.unload_extension(f"commands.{extension}")
    await inter.response.send_message("Cogs unloaded")

@bot.slash_command(name="reload", description="FOR ADMINS")
@commands.is_owner()
async def reload(inter, extension: Cogss):
    bot.reload_extension(f"commands.{extension}")
    await inter.response.send_message("Cogs reloaded")


def load_cogs():
    for filename in listdir('./commands'):
        if filename.endswith('.py'):
            bot.load_extension(f'commands.{filename[:-3]}')

if __name__ == "__main__":
    load_cogs()
    activity = disnake.Activity(
    name="нарды",
    type=disnake.ActivityType.watching,
    )
    bot.run(config.token)