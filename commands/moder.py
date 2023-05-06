from disnake.ext import commands
import disnake

class Moder(commands.Cog):

    def __init__(self, bot):
            self.bot = bot  

    @commands.Cog.listener()
    async def on_ready(self):
        print("\033[35m\n MODER COMMANDS LOADED\033")

    
def setup(bot):
    bot.add_cog(Moder(bot)) 