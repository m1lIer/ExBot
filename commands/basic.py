from disnake.ext import commands
import disnake
import sys
class BasicCommands(commands.Cog):
    def __init__(self, bot):
            self.bot = bot  
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("\033[35m\n BASIC COMMANDS LOADED\033")


    @commands.slash_command(name='help', description="Помощь умственно отсталым")
    async def help(self, inter):
        embedguild = disnake.Embed()
        embed = disnake.Embed(title="🍓 Помощь умственно отсталым  🍓",
                      description="»»                                           »»——⍟——««                                          ««",
                      colour=0xe400f5)

        embed.add_field(name="╔=====================================╗",
                        value="",
                        inline=False)
        embed.add_field(name="║                    ↘️ ***Основные команды*** ↙️           ║",
                        value="",
                        inline=False)
        embed.add_field(name="╚=====================================╝",
                        value="",
                        inline=False)
        embed.add_field(name="/report",
                        value="Жалоба на человека",
                        inline=False)
        embed.add_field(name="/help",
                        value="*Помощь умственно отсталым*",
                        inline=False)
        embed.add_field(name="/server",
                        value="Информация о сервере",
                        inline=False)
        embed.add_field(name="╔=====================================╗",
                        value="",
                        inline=False)
        embed.add_field(name="║                       ↘️***Чат команды***↙️                     ║",
                        value="",
                        inline=False)
        embed.add_field(name="╚=====================================╝",
                        value="",
                        inline=False)
        embed.add_field(name="/ударить",
                        value="Ударить человека",
                        inline=False)
        embed.add_field(name="/обнять",
                        value="Обнять человека",
                        inline=False)
        embed.add_field(name="/поцеловать",
                        value="Поцеловать человека",
                        inline=False)
        embed.add_field(name="╔=====================================╗",
                        value="",
                        inline=False)
        embed.add_field(name="║            ↘️***Музыкальные команды***↙️             ║",
                        value="",
                        inline=False)
        embed.add_field(name="╚=====================================╝",
                        value="Доступны только в <#953731239112736818>",
                        inline=False)
        embed.add_field(name="/play",
                        value="Воспроизвести трек",
                        inline=False)
        embed.add_field(name="/skip",
                        value="Остановить проигрывание трека",
                        inline=False)
        embed.add_field(name="/volume",
                        value="Изменить громкость бота(Доступ от Модератора и выше)",
                        inline=False)
        embed.add_field(name="/leave",
                        value="Выгнать бота из голосового канала",inline=False)
        embed.add_field(name="/pause",value="Поставить бота на паузу",inline=False)
        embed.add_field(name="/resume",value="Продолжить проигрывание трека",inline=False)
        '''
        embed.add_field(name="╔=====================================╗",
                        value="",
                        inline=False)
        embed.add_field(name="║            ↘️***Команды модераторов***↙️             ║",
                        value="",
                        inline=False)
        embed.add_field(name="╚=====================================╝",
                        value="",
                        inline=False)
        embed.add_field(name="/load",value="Загрузить cog (music, basic, moder, support)",inline=False)
        embed.add_field(name="/unload",value="Выгрузить cog (music, basic, moder, support)",inline=False)
        embed.add_field(name="/reload",value="Перезагрузить cog (music, basic, moder, support)",inline=False)
        embed.add_field(name="/volume",value="Изменить громкость бота(Доступ от Модератора и выше)",inline=False)
'''
        embed.set_image(url="https://media.discordapp.net/attachments/1087471217939857470/1099061426171154572/2543ff1b8e9f95b7f18d38041fa31d45.gif")

        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/784421051828142080/4003c7e00a1cd0085b241f1f5d5f010e.webp?size=2048")

        embed.set_footer(text="Помощь умственно отсталым")
        user = await self.bot.fetch_user(inter.author.id)
        await user.send(embed = embed)
        await inter.response.send_message("Посмотри в лс!)", ephemeral = True)


    @commands.slash_command(name="server", description="server information")
    async def server(inter):
        await inter.response.send_message(f"Server name: {inter.guild.name}\nTotal members: {inter.guild.member_count}")


    @commands.slash_command(name="обнять", description="обнять человека")
    async def обнять(inter, человек: disnake.User  = commands.Param(description = "Человек которого вы хотите обнять")):
        await inter.response.send_message(f"<@{inter.author.id}> обнял(а) <@{человек.id}>")


    @commands.slash_command(name="поцеловать", description="поцеловать человека")
    async def поцеловать(inter, человек: disnake.User= commands.Param(description = "Человек которого вы хотите поцеловать")):
        await inter.response.send_message(f"<@{inter.author.id}> поцеловал(а) <@{человек.id}>")


    @commands.slash_command(name="ударить", description="ударить человека")
    async def ударить(inter, человек: disnake.User= commands.Param(description = "Человек которого вы хотите ударить")):
        await inter.response.send_message(f"<@{inter.author.id}> ударил(а) <@{человек.id}>")


def setup(bot):
    bot.add_cog(BasicCommands(bot))  