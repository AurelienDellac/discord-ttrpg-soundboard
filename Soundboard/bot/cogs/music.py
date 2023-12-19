import typing as t
from enum import Enum
from time import sleep

import discord
import wavelink
from discord.ext import commands

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class VolumeTooLow(commands.CommandError):
    pass


class VolumeTooHigh(commands.CommandError):
    pass


class MaxVolume(commands.CommandError):
    pass


class MinVolume(commands.CommandError):
    pass


class NoLyricsFound(commands.CommandError):
    pass


class InvalidEQPreset(commands.CommandError):
    pass


class NonExistentEQBand(commands.CommandError):
    pass


class EQGainOutOfBounds(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eq_levels = [0.] * 15
        self.current_track = None
        self.preferred_volume = 1.0
        self.repeat_mode = RepeatMode.NONE

    async def play_current_track(self):
        if self.current_track:
            await self.play(self.current_track)
        
    async def set_volume_to_preferred(self):
        await self.set_volume(self.preferred_volume)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.context = None
        
    async def start_nodes(self):
        await self.bot.wait_until_ready()
        
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='127.0.0.1',
            port=2333,
            password='youshallnotpass',
            identifier=self.bot.identifier + " NODE",
            region="europe")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild.id).disconnect()

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player, track, reason):
        await self.repeat_on_wavelink_event(player)
    
    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, player, track, error):
        await self.repeat_on_wavelink_event(player)
    
    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self, player, track, treshold):
        await self.repeat_on_wavelink_event(player)
        
    async def repeat_on_wavelink_event(self, player):
        if player.repeat_mode == RepeatMode.ONE:
            await player.play_current_track()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    def get_player(self):
        if self.context != None:
            return self.context.voice_client
        else:
            return None
        
    '''
    Play a song from a file path.
    '''
    async def play_async(self, song_path):
        player = self.get_player()
        
        if player != None and player.is_connected:
            tracks = await wavelink.NodePool.get_node().get_tracks(cls=wavelink.abc.Playable, query=song_path)
        
            if not tracks:
                return await self.context.send('Could not find any songs with that query.')
            else:
                player.current_track = tracks[0]
                
            if player.is_playing() and player.repeat_mode != RepeatMode.NONE:
                    await self.mute_player(player)
                    await player.stop()
            else:                    
                await player.play(player.current_track)
            
            await player.set_volume_to_preferred()
            
    async def stop_player_async(self):
        player = self.get_player()
        player.current_track = None
        
        await self.mute_player(player)
        await player.stop()
        await self.context.send('stops playing ' + self.bot.display_name)
        
    async def pause_player_async(self):
        player = self.get_player()
        
        await self.mute_player(player)
        await player.set_pause(True)
        await self.context.send('interrupts playing ' + self.bot.display_name)
        
    async def resume_player_async(self):
        player = self.get_player()
        
        await player.set_volume_to_preferred()
        await player.set_pause(False)
        await self.context.send('resumes playing ' + self.bot.display_name)
        
    async def set_player_volume_async(self, volume):
        if volume <= 100:
            volume = volume / 100 * 5
        
        if volume > 0 and volume < 5:
            player = self.get_player()
            player.preferred_volume = volume
            await player.set_volume_to_preferred()
            await self.context.send('Volume set to ' + str(round(player.volume * 100 / 5)) + "%")
        
    async def modulate_player_volume_async(self, modulation):
        player = self.get_player()
        if player.volume + modulation > 0 and player.volume + modulation < 5:
            player.preferred_volume = player.volume + modulation
            await player.set_volume_to_preferred()
            await self.context.send('Volume set to ' +str(round(player.volume * 100 / 5)) + "%")
    
    async def mute_player(self, player):
        await player.set_volume(0)
        
    async def repeat_player(self, repeat_mode):
        player = self.get_player()
        player.repeat_mode = RepeatMode(repeat_mode)
        await self.context.send('Repeat mode set to ' + RepeatMode(repeat_mode).name)        
        
    @commands.command(name="connect", aliases=["join"])
    async def connect_command(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        player = self.get_player()
        if(player == None):
                
            try:
                channel = channel or ctx.author.voice.channel
            except AttributeError:
                return await ctx.send('No voice channel to connect to. Please either provide one or join one.')

            # vc is short for voice client...
            # Our "vc" will be our wavelink.Player as typehinted below...
            # wavelink.Player is also a VoiceProtocol...
            player = Player()
            vc: Player = await channel.connect(cls=player)
            
            self.context = ctx

            await ctx.send(f"Connected to {channel.name}.")
            await self.repeat_player(self.bot.repeat_mode)
        else:
            await ctx.send(f"Already connected to {player.channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        player = self.get_player()
        if player != None:
            await player.disconnect()
            await ctx.send("Disconnected.")
    
    @commands.command(name="eq")
    async def eq_command(self, ctx, preset: str):
        player = self.get_player()

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            raise InvalidEQPreset

        await player.set_eq(eq())
        await ctx.send(f"Equaliser adjusted to the {preset} preset.")


async def setup(bot):
    await bot.add_cog(Music(bot))
