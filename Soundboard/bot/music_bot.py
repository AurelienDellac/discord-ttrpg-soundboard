from pathlib import Path

import discord
from discord.ext import commands


class MusicBot(commands.Bot):
    def __init__(self, prefix, identifier, display_name, repeat_mode):
        self.identifier = identifier
        self.display_name = display_name
        self.repeat_mode = repeat_mode
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=prefix, case_insensitive=True, intents=discord.Intents.all())

    def bprint(self, txt):
        print(self.display_name + ": " + self.identifier + " >> " + txt)
    
    async def setup(self):
        self.bprint("Running setup...")

        for cog in self._cogs:
            await self.load_extension(f"bot.cogs.{cog}")
            self.bprint(f" Loaded `{cog}` cog.")

        self.bprint("Setup complete.")
    
    async def setup_hook(self):
        music = self.get_cog("Music")
        self.loop.create_task(music.start_nodes())

    async def start(self, token):
        await self.setup()

        self.bprint("Starting bot...")
        await super().start(token, reconnect=True)

    async def shutdown(self):
        self.bprint("Closing connection to Discord...")
        await super().close()

    async def close(self):
        self.bprint("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        self.bprint(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        self.bprint("Bot resumed.")

    async def on_disconnect(self):
        self.bprint("Bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        self.bprint("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or(";;")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
            
    async def play_song_async(self, song_path):
        await self.get_cog("Music").play_async(song_path)
        
    async def control_music_async(self, control):
        music = self.get_cog("Music")
        
        control = control.split(";")
        control_command = control[0]
        control_parameters = control[1:]
        
        if control_command == "pause":
            await music.pause_player_async()
            
        elif control_command == "resume":
            await music.resume_player_async()
            
        elif control_command == "stop":
            await music.stop_player_async()
            
        elif control_command == "volume":
            await music.set_player_volume_async(int(control_parameters[0]))
            
        elif control_command == "volume_up":
            await music.modulate_player_volume_async(0.2)
            
        elif control_command == "volume_down":
            await music.modulate_player_volume_async(-0.2)
        
        elif control_command == "repeat":
            await music.repeat_player(int(control_parameters[0]))
