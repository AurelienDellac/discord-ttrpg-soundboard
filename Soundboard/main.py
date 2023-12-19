import asyncio
import logging
import os
import threading

import eel
from dotenv import load_dotenv

from bot import MusicBot
from soundboard import Soundboard


def run_bots_async(bot1, bot2):
    TOKEN_MUSIC = os.getenv("DISCORD_BOT_MUSIC_TOKEN")
    TOKEN_SE = os.getenv("DISCORD_BOT_SE_TOKEN")
    
    loop = asyncio.get_event_loop()
    loop.create_task(bot1.start(TOKEN_MUSIC))
    loop.create_task(bot2.start(TOKEN_SE))
    loop.run_forever()  
       
def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    load_dotenv()
    PREFIX_MUSIC = str(os.getenv("DISCORD_BOT_MUSIC_PREFIX"))
    PREFIX_SE = str(os.getenv("DISCORD_BOT_SE_PREFIX"))
    
    bot_music = MusicBot(prefix=PREFIX_MUSIC, identifier="music", display_name="music", repeat_mode=1)
    bot_sound_effects = MusicBot(prefix=PREFIX_SE, identifier="sound_effects", display_name="sound effects", repeat_mode=0)
    
    # Create the soundboard and expose the function to the Javascript part.
    soundboard = Soundboard([bot_music, bot_sound_effects], os.getenv("LOCAL_STORAGE_FOLDER"))
    eel.expose(soundboard.play_song)
    eel.expose(soundboard.control_music)
    
    # Create a thread to run the web interface.
    soundboard_thread = threading.Thread(target=soundboard.start_ui)
    soundboard_thread.daemon = True
    soundboard_thread.start()     
    
    run_bots_async(bot_music, bot_sound_effects)
    
if __name__ == "__main__":
    main()
