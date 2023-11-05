"""
MelonBot
"""
import discord #pycord
import json
import pytube
import os
import asyncio

botdata = json.load(open("config.json"))
bot = discord.Bot()

######################################################## COMMANDS ########################################################
@bot.command(description="The coup de grace")
async def intent(ctx): 
    await ctx.respond("I SHALL CLEANSE THE SERVER OF NON-MELONKIND")

############## ARCHIVE ##############
@bot.command(description="Archives the channel's messages and pictures, and optionally stores all files in it")
async def archive(ctx): 
    await ctx.respond("NOT IMPLEMENTED YET L")

############## PLAY #################

#add_item
class QueryResults(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View

    async def __init__(self, searchResults):

        super().__init__()
            
            #create button, needs youtube object
            #button should contain link, name of video, author

    @discord.ui.button(label="**{self.searchResults[0].title}** by **{self.searchResults[0].author}**:\n**https://www.youtube.com/watch?v={self.searchResults[0].video_id}**", row=0, style=discord.ButtonStyle.primary)
    async def callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="**{self.searchResults[1].title}** by **{self.searchResults[1].author}**:\n**https://www.youtube.com/watch?v={self.searchResults[1].video_id}**", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="**{self.searchResults[2].title}** by **{self.searchResults[2].author}**:\n**https://www.youtube.com/watch?v={self.searchResults[2].video_id}**", row=1, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="**{self.searchResults[3].title}** by **{self.searchResults[3].author}**:\n**https://www.youtube.com/watch?v={self.searchResults[0].video_id}**", row=1, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="**{self.searchResults[4].title}** by **{self.searchResults[4].author}**:\n**https://www.youtube.com/watch?v={self.searchResults[0].video_id}**", row=2, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="**{self.searchResults[5].title}** by **{self.searchResults[5].author}**:\n**https://www.youtube.com/watch?v={self.searchResults[5].video_id}**", row=2, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message("You pressed me!")

    #filename=(video.video_id+".mp4"))

async def playVideo(response, vc, video):
#Attempt to download and play video
    try:
        url = f"https://www.youtube.com/watch?v={video.video_id}"
        await response.edit_original_response(content=f"Loading: **{video.title}** by **{video.author}\n{url}**")
        stream = video.streams.filter(only_audio=True).filter(file_extension='mp4').order_by(attribute_name="abr").last()
        videopath = stream.download(output_path=(f"{os.getcwd()}\\videocache"), filename="music.mp4") 
        #File downloaded, now play

        await response.edit_original_response(content=f"Playing: **{video.title}** by **{video.author}\n{url}**")
        vc.play(discord.FFmpegPCMAudio(videopath))
        while vc.is_playing(): await asyncio.sleep(1)

        #Wait until music is done playing
        await response.edit_original_response(content=f"Finished playing: **{video.title}** by **{video.author}\n{url}**")
        await vc.disconnect()

    except Exception as e:
        await response.edit_original_response(content=f"Error has occurred: {e}")

@bot.command(description="Plays youtube video with specified URL, otherwise searches for the video")
async def play(ctx, query): 
    #Check if user is in a voice channel
    if not ctx.author.voice:
        await ctx.respond("You must be in a voice channel to play audio!")
    #Conditions all set, play audio
    else: 
        #Connect bot to the channel
        vc = ctx.voice_client
        if not vc or ctx.author.voice.channel.id != vc.channel.id:
            vc = await ctx.author.voice.channel.connect()  

        #Direct URL
        if "https://www.youtube.com/watch" in query:
            response = await ctx.respond(f"Querying link: **{query}**")
            try:
                video = pytube.YouTube(query)
            except pytube.exceptions.VideoUnavailable:
                await response.edit_original_response(content=f"Link unavailable or incorrect: **{query}**")
                return
            playVideo(response, vc, video)
        #Keyword search
        else: 
            response = await ctx.respond(f"Querying search: **\"{query}\"**")
            search = pytube.Search(query)
            if len(search.results) == 0:
                await response.edit_original_response(content=f"No results found for: **{query}**")
                return
            elif len(search.results) == 1:
                playVideo(response, vc, search.results[0])
            else:
                await response.edit_original_response(content=f"Results for: **{query}**:", view=QueryResults(search.results[:6]))

        

######################################################## RUN BOT ########################################################
print("Running bot...")
bot.run(botdata["client_secret"])
print("Bot shutdown!")

#https://discord.com/api/oauth2/authorize?client_id=1167948719006679171&permissions=277045423616&scope=bot