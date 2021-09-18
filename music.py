import discord
from discord.ext import commands
import youtube_dl
import asyncio
import urllib
import simplejson
from song import Song

class music(commands.Cog):
  # Input queue
  song_queue = []

  FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
  }
  YDL_OPTIONS = {
    'format': 'bestaudio'
  }

  ytdl = youtube_dl.YoutubeDL(YDL_OPTIONS)

  loop: asyncio.AbstractEventLoop

  def __init__(self, client):
    self.client = client
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    self.loop = loop

  @commands.command()
  async def disconnect(self,ctx):
    try:
      self.song_queue = []
      await ctx.voice_client.disconnect()
    except Exception as exception:
      await self.handle_exception(ctx, exception)
      raise exception

  @commands.command()
  async def play(self, ctx, url):
    try:
      # Join the voice channel 
      await self.join(ctx)

      # If we fail to join the voice channel, then do nothing
      if ctx.voice_client is None: 
        print('Failed to join voice channel')
        return

      vc = ctx.voice_client

      # Get song data from youtube
      source = await self.getSourceFromUrl(url)

      # Store the song data into a song object and store that into queue
      song = Song(url, '', '', source)
      self.song_queue.append(song)

      # Add play if not already playing a song
      if not vc.is_playing():
        self.play_next(ctx, vc)

      else:
        await ctx.send('Song queued')
    except Exception as exception:
      await self.handle_exception(ctx, exception)
      raise exception

  @commands.command()
  async def pause(self,ctx):
    try:
      ctx.voice_client.pause()
      await ctx.send('paused')
    except Exception as exception:
      await self.handle_exception(ctx, exception)
      raise exception

  @commands.command()
  async def resume(self,ctx):
    try:
      ctx.voice_client.resume()
      await ctx.send('resume')
    except Exception as exception:
      await self.handle_exception(ctx, exception)
      raise exception

  @commands.command() 
  async def clear(self,ctx):
    try:
      self.song_queue = []
      await ctx.send("Queue has been cleared")
    except Exception as exception:
      await self.handle_exception(ctx, exception)
      raise exception

  @commands.command()
  async def queue(self, ctx):
    await ctx.send("Current urls in the queue:")
    for i in range(len(self.song_queue)):
      await ctx.send(str(i+1) + ": " + self.song_queue[i].getUrl())

  @commands.command()
  async def skip(self, ctx):
    vc = ctx.voice_client
    if not vc is None:
      self.play_next(ctx, vc)

  async def handle_exception(self,ctx, exception):
    await ctx.send("RIP, something broke")
    user = await self.client.fetch_user("90457491711754240")
    await ctx.send(user.mention + ' please fix me!')

  async def join(self,ctx):
    # If the user is not in the voice channel, then do nothing
    if ctx.author.voice is None:
      await ctx.send("Hey you arent in a voice channel")
      return

    # If voice channel is found, join it
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  async def getSourceFromUrl(self, url):
    info = self.ytdl.extract_info(url, download=False)
    url2 = info['formats'][0]['url']
    return await discord.FFmpegOpusAudio.from_probe(
      url2,
      **self.FFMPEG_OPTIONS
    )

  def play_next(self, ctx, vc):
    if len(self.song_queue) >= 1:
      source = self.song_queue.pop(0).getSource()
      vc.stop()
      vc.play(source=source, after=lambda e: {
        self.play_next(ctx, vc)
      })
    else:
      fut = asyncio.run_coroutine_threadsafe(self.waitThenDisconnect(ctx, vc), vc.loop)
      try:
        fut.result()
      except:
        print("ERROR getting thread result")
        pass


  async def waitThenDisconnect(self, ctx, vc):
      await asyncio.sleep(90) #wait 1 minute and 30 seconds
      if not vc.is_playing():
        await ctx.send("No more songs in queue.")
        await self.disconnect(ctx)

def setup(client):
  client.add_cog(music(client))