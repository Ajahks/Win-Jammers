import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def disconnect(self,ctx):
    try:
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
      ctx.voice_client.stop()
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format': 'bestaudio'}
      vc = ctx.voice_client

      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2,
        **FFMPEG_OPTIONS)
        vc.play(source)
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

def setup(client):
  client.add_cog(music(client))