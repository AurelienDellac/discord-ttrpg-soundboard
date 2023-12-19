import asyncio
import tkinter as tk
from functools import partial

import eel
from configobj import ConfigObj


class Soundboard():
    def __init__(self, bots, song_folder):
        self.song_folder = song_folder
        self.bots = {}
        for bot in bots:
            self.bots[bot.identifier] = bot
        
        self.eel = eel
        eel.init('soundboard_web')
        
    def start_ui(self):
        self.eel.start("index.html")
    
    def play_song(self, song_path, bot_identifier):
        bot = self.bots[bot_identifier]
        song_path = song_path.replace("{song_folder}", self.song_folder)
        song_path = song_path.replace("{youtube}", "ytsearch: ")
        asyncio.run_coroutine_threadsafe(bot.play_song_async(song_path), bot.loop).result()
     
    def control_music(self, control, bot_identifier):
        bot = self.bots[bot_identifier]
        asyncio.run_coroutine_threadsafe(bot.control_music_async(control), bot.loop).result()
