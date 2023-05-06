from disnake.ext import commands
import disnake
import sys
sys.path.insert(1, '../')
import run

class Support(commands.Cog):

    def __init__(self, bot):
            self.bot = bot  

    @commands.Cog.listener()
    async def on_ready(self):
        print("\033[35m\n SUPPORT COMMANDS LOADED\033")
    @commands.slash_command(name="report", description="Жалоба на человека")
    async def report(self, inter, человек: disnake.User  = commands.Param(description = " Человек, который нарушил правила"), report: str = commands.Param(description = "Причина")):
        await inter.response.defer(ephemeral=True)
        channel = await self.bot.fetch_channel(987268067841179660)
        user = await self.bot.fetch_user(450329247924355096)
        palka = await self.bot.fetch_user(791592421460541450)
        await channel.send(f"\n**Жалоба** от <@{inter.author.id}> на <@{человек.id}>, причина - **{report}**\n")
        await user.send(f"\n**Жалоба** от <@{inter.author.id}> на <@{человек.id}>, причина - **{report}**\n")
        await palka.send(f"\n**Жалоба** от <@{inter.author.id}> на <@{человек.id}>, причина - **{report}**\n")
        await inter.edit_original_message(content = f"\n**Жалоба** на <@{человек.id}> отправлена, причина - **{report}**\n")
def setup(bot):
    bot.add_cog(Support(bot)) 