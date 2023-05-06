import disnake
from disnake.ext import commands
import sys
sys.path.insert(1, '../')
from run import client
sys.path.insert(2, 'settings/')
import config


from bs4 import BeautifulSoup
from disnake import FFmpegPCMAudio
from disnake import TextChannel
from disnake import VoiceClient
from disnake import utils
from disnake.ext import commands
from disnake.ext.commands import Bot
from disnake.utils import get
from disnake.voice_client import VoiceClient
from dotenv import load_dotenv
from tabnanny import check
from time import sleep
from typing import List, Tuple, Optional
from yt_dlp import YoutubeDL
import asyncio
import datetime
import discord
import dpath.util
import ffmpeg
import json
import os
import random
import re
import requests
import time



class Music(commands.Cog):
    def __init__(self, bot):
            self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print("\033[35m\n MUSIC COMMANDS LOADED\033")

    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    PATTERNS = [
        re.compile(r'window\["ytInitialData"\] = (\{.+?\});'),
        re.compile(r'var ytInitialData = (\{.+?\});'),
    ]

    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    load_dotenv()
    
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'cookiefile': 'cookies.txt'}
    FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -af volume=0.06'}
            
    queue = {}
    track_c = 0
    track_p = 0


    async def play_queue(self, inter, search):
            print("\n\n")
            print(Music.queue)
            print("\n")
            print(f"СЧЕТЧИК ОЧЕРЕДИ -- {Music.track_c}")
            print(f"ТРЕК КОТОРЫЙ БУДЕТ ИГРАТЬ -- {Music.track_p}")
            print("\n\n")

            voice = get(self.bot.voice_clients, guild=inter.guild)
            
            channel_text = await self.bot.fetch_channel(953731239112736818)
            await channel_text.send(f'_Скачиваю трек из очереди_')
            
            def get_ytInitialData(url: str) -> Optional[dict]:

                rs = Music.session.get(url)

                for pattern in Music.PATTERNS:
                    m = pattern.search(rs.text)

                if m:
                    data_str = m.group(1)
                    return json.loads(data_str)
                    

            def search_youtube(text_or_url: str) -> List[Tuple[str, str]]:

                if text_or_url.startswith('http'):
                    text = text_or_url

                else:
                    text = search
                    url = f'https://www.youtube.com/results?search_query={text}&ab_channel={None}'

                items = []
                data = get_ytInitialData(url)

                if not data:
                    return items

                videos = dpath.util.values(data, '**/videoRenderer')

                if not videos:
                    videos = dpath.util.values(data, '**/playlistVideoRenderer')


                for video in videos:

                    if 'videoId' not in video:
                        continue

                    url = 'https://www.youtube.com/watch?v=' + video['videoId']

                    try:
                        title = dpath.util.get(video, 'title/runs/0/text')

                    except KeyError:
                        title = dpath.util.get(video, 'title/simpleText')

                    items.append((url, title))

                return items

                
            items = search_youtube('')
            items_https = items[0]
            print(items_https[0])


            url = items_https[0]
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            quotes = soup.find_all('link', itemprop="name")
            name = quotes[0]
            name_str = str(name)
            name_str = name_str.replace("<link content=\"", "")
            name_str = name_str.replace("\" itemprop=\"name\"/>", "")
            name_str = name_str.replace(" ", "")
            URL = f'{items_https[0]}&ab_channel={name_str}'

            OUT_URL = URL

            with YoutubeDL(Music.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(URL, download=False)

            URL = info['url']
            DURATION = info['duration']
            voice.play(disnake.FFmpegPCMAudio(executable="C:/Users/m1lle/Desktop/StrawberryBot-main/commands/ffmpeg.exe", source = URL, **Music.FFMPEG_OPTIONS))
            voice.is_playing()
            title = items[0]
            await channel_text.send(f'_Bot is playing:_ **{title[1]}**')
            await asyncio.sleep(DURATION)
            if Music.track_c == Music.track_p:
                Music.queue.clear()
                Music.track_c = 0
                Music.track_p = 0


            if len(Music.queue) != 0:

                voice.stop()
                Music.track_p += 1
                await Music.play_queue(self, inter, Music.queue[Music.track_p])





    @commands.slash_command(name="play", description="Включить трек")
    async def play(self, inter, search: str = commands.Param(description = "Название песни или ссылка(Youtube)")):
            
            
            channel_text = await self.bot.fetch_channel(953731239112736818)

            voice = get(self.bot.voice_clients, guild=inter.guild)

            if not inter.author.voice:
                await inter.response.send_message("Зайди в войс чтобы включить трек")
            
            channel = inter.author.voice.channel

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()


            if voice.is_playing():
                await inter.response.send_message(f"Добавил в очередь **{search}**")
                Music.track_c += 1
                Music.queue[Music.track_c] = search
                # voice.stop()


            if not voice.is_playing():
                await inter.response.defer()

                def get_ytInitialData(url: str) -> Optional[dict]:

                    rs = Music.session.get(url)

                    for pattern in Music.PATTERNS:
                        m = pattern.search(rs.text)

                    if m:
                        data_str = m.group(1)
                        return json.loads(data_str)
                    

                def search_youtube(text_or_url: str) -> List[Tuple[str, str]]:

                    if text_or_url.startswith('http'):
                        text = text_or_url

                    else:
                        text = search
                        url = f'https://www.youtube.com/results?search_query={text}&ab_channel={None}'

                    items = []
                    data = get_ytInitialData(url)

                    if not data:
                        return items

                    videos = dpath.util.values(data, '**/videoRenderer')

                    if not videos:
                        videos = dpath.util.values(data, '**/playlistVideoRenderer')


                    for video in videos:

                        if 'videoId' not in video:
                            continue

                        url = 'https://www.youtube.com/watch?v=' + video['videoId']

                        try:
                            title = dpath.util.get(video, 'title/runs/0/text')

                        except KeyError:
                            title = dpath.util.get(video, 'title/simpleText')

                        items.append((url, title))

                    return items

                
                items = search_youtube('')
                items_https = items[0]
                print(items_https[0])


                url = items_https[0]
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                quotes = soup.find_all('link', itemprop="name")
                name = quotes[0]
                name_str = str(name)
                name_str = name_str.replace("<link content=\"", "")
                name_str = name_str.replace("\" itemprop=\"name\"/>", "")
                name_str = name_str.replace(" ", "")
                URL = f'{items_https[0]}&ab_channel={name_str}'

                OUT_URL = URL

                with YoutubeDL(Music.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(URL, download=False)

                URL = info['url']
                DURATION = info['duration']
                voice.play(disnake.FFmpegPCMAudio(executable="C:/Users/m1lle/Desktop/StrawberryBot-main/commands/ffmpeg.exe", source = URL, **Music.FFMPEG_OPTIONS))
                voice.is_playing()
                title = items[0]
                await inter.edit_original_message(content = f'_Bot is playing:_ **{title[1]}**')
                await asyncio.sleep(DURATION)

                if len(Music.queue) != 0:
                    voice.stop()
                    Music.track_p += 1
                    await Music.play_queue(self, inter, Music.queue[Music.track_p])


    
    
    @commands.slash_command(name="resume", description="Продолжить трек")
    async def resume(self, inter):
        voice = get(self.bot.voice_clients, guild=inter.guild)
        if not inter.author.voice:
                await inter.response.send_message("Зайди в войс чтобы продолжить играть трек")
            
        elif not voice.is_playing():
            voice.resume()
            await inter.response.send_message("Продолжаю играть...")
        

    @commands.slash_command(name="pause", description="Приостановить трек")
    async def pause(self, inter):
        voice = get(self.bot.voice_clients, guild=inter.guild)

        if not inter.author.voice:
                await inter.response.send_message("Зайди в войс чтобы приостановить трек")
            

        elif voice.is_playing():
            voice.pause()
            await inter.response.send_message("Опа, моя остоновочка")
            #await inter.send('_Bot has been paused_')


    # command to pause voice if it is playing
    @commands.slash_command(name="leave", description="Выгнать бота")
    async def leave(self, inter):
        await inter.response.defer()
        voice = get(self.bot.voice_clients, guild=inter.guild)
        if not inter.author.voice:
                await inter.edit_original_message(content = "Зайди в войс чтобы выгнать бота")
            
        elif voice.is_playing():
            voice.stop()
            Music.queue.clear()
            Music.track_c = 0
            Music.track_p = 0
        else:
            Music.queue.clear()
            Music.track_c = 0
            Music.track_p = 0
            await voice.disconnect()
            await inter.edit_original_message(content = "GG, я ливаю")


    # command to stop voice
    @commands.slash_command(name="skip", description="Пропустить трек")
    async def skip(self, inter):
        await inter.response.defer()
        voice = get(self.bot.voice_clients, guild=inter.guild)
        if not inter.author.voice:
                await inter.edit_original_message(content = "Зайди в войс чтобы пропустить трек")
        else:    
            if voice.is_playing():
                if len(Music.queue) != 0:
                    Music.track_p += 1
                    if Music.track_p <= len(Music.queue):
                        voice.stop()
                        await inter.edit_original_message(content = "Пропускаю трек...")
                        await Music.play_queue(self, inter, Music.queue[Music.track_p])

                    else:
                        voice.stop()
                        Music.queue.clear()
                        Music.track_c = 0
                        Music.track_p = 0
                        await inter.edit_original_message(content = "Треки в очереди закончились, пропускаю данный трек")
                else:
                    await inter.edit_original_message(content = "Пропускаю трек...")
                    voice.stop()
            else:
                await inter.edit_original_message(content = "Я и так ничего не играю =(")

    @commands.slash_command(name="volume", description="Изменить громкость")
    async def volume(self, inter, vol: int = commands.Param(description = "Громкость в % (от 0% до 100%)")):
        voice = get(self.bot.voice_clients, guild=inter.guild)
        if vol > 100 or vol < 0:
            await inter.response.send_message("0 < Volume < 100")
        vol2 = vol/1000

        Music.FFMPEG_OPTIONS['options'] = f'-vn -af volume={vol2}'
        await inter.response.send_message(f"Volume = {vol}%")
    @commands.slash_command(name="очередь", description="Показать треки в очереди")
    async def очередь(self, inter):
        await inter.response.defer()
        print(len(Music.queue))
        if len(Music.queue) > 1:
            embed = disnake.Embed(title="Треки в очереди",
                        colour=0xe400f5)
            for i in range(1, len(Music.queue)+1):
                embed.add_field(name=f"_{i} - {Music.queue[i]}_",
                            value="",
                            inline=False)
            await inter.edit_original_message(embed = embed)
        if len(Music.queue) == 1:
            embed = disnake.Embed(title="Треки в очереди",
                        colour=0xe400f5)
            embed.add_field(name=f"_1 - {Music.queue[1]}_",
                            value="",
                            inline=False)
            await inter.edit_original_message(embed = embed)
        if len(Music.queue) == 0:
            await inter.edit_original_message(content = "**Нет треков в очереди**")


def setup(bot):
    bot.add_cog(Music(bot)) 