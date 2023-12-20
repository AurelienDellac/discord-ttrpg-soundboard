import asyncio
import tkinter as tk
from functools import partial

import eel
from configobj import ConfigObj


class Soundboard():
    def __init__(self, bots, sound_folder):
        self.sound_folder = sound_folder
        self.bots = {}
        for bot in bots:
            self.bots[bot.identifier] = bot
        
        self.eel = eel
        eel.init('soundboard_web')
        
    def start_ui(self):
        self.eel.start("index.html")
    
    def play_sound(self, sound_path, bot_identifier):
        bot = self.bots[bot_identifier]
        sound_path = sound_path.replace("{sound_folder}", self.sound_folder)
        sound_path = sound_path.replace("{youtube}", "ytsearch: ")
        asyncio.run_coroutine_threadsafe(bot.play_sound_async(sound_path), bot.loop).result()
     
    def control_music(self, control, bot_identifier):
        bot = self.bots[bot_identifier]
        asyncio.run_coroutine_threadsafe(bot.control_music_async(control), bot.loop).result()
