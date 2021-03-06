import asyncio
import os
import wikipedia
import yfinance
from dotenv import load_dotenv
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
discordtoken = os.getenv('DISCORD_TOKEN')
spotifyClient = os.getenv('SPOTIFY_CLIENT_ID')
spotifySecretClient = os.getenv('SPOTIFY_CLIENT_SECRET')

# use this line to change the bot prefix to whatever you want
# by changing the sign inside the quotations in command_prefix="~"
bot = commands.Bot(command_prefix="~")


@bot.event
# Console response logging that the bot is active
async def on_ready():
    print('logged in as {0.user}'.format(bot))


# User inputs ~ping and returns pong
@bot.command(
    name="ping",
    help="~~ Uses come crazy logic to determine if pong is actually the correct value or not.",
    brief="~~ Prints pong back to the channel."
)
async def pingpong(message):
    await message.channel.send("```fix\npong```")


#
@bot.command(
    name="tired",
    help="~~ its all so tiresome",
    brief="~~ its all so tiresome"
)
async def tiresome(message):
    await message.channel.send("https://i.imgur.com/yxqwFFG.jpg")


# search wikipedia for a link based on the users arguement
@bot.command(
    name="wiki",
    help="~~ Searches Wikipedia for a page based on the users arguement",
    brief="~~ Wikipedia Search Function"
)
async def wikipediaSearch(message, arg):
    print("User searched wikipedia for: " + arg)

    results = wikipedia.search(arg, results=5)
    finalmessage = "```fix\nHere are your results:\n\n"

    for x in range(len(results)):
        finalmessage += "   " + str(x + 1) + ". " + results[x] + "\n"

    finalmessage += "\nPlease choose 1-5 for your desired search```"

    if 0 < len(results):
        wikimsg = await message.channel.send(finalmessage)

        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for x in emojis:
            await wikimsg.add_reaction(emoji=x)

        def check(reaction, user):
            return reaction.message.id == wikimsg.id and user == message.author

        while True:
            try:
                reaction, _ = await bot.wait_for('reaction_add', timeout=20.0, check=check)

                if reaction.emoji == "1️⃣":
                    await message.channel.send(wikipedia.page(results[0], auto_suggest=False).url, )
                elif reaction.emoji == "2️⃣":
                    await message.channel.send(wikipedia.page(results[1], auto_suggest=False).url)
                elif reaction.emoji == "3️⃣":
                    await message.channel.send(wikipedia.page(results[2], auto_suggest=False).url)
                elif reaction.emoji == "4️⃣":
                    await message.channel.send(wikipedia.page(results[3], auto_suggest=False).url)
                elif reaction.emoji == "5️⃣":
                    await message.channel.send(wikipedia.page(results[4], auto_suggest=False).url)

            except asyncio.TimeoutError:
                break
    else:
        await message.channel.send("```fix\nI could not find anything for that page, Sorry.```")


@bot.command(
    name="stock",
    help="~~ Searches for a stock tags price (Powered by yfinance API)",
    brief="~~ Searches for a stock tags price"
)
async def stockp(message, arg):
    # create Ticker module
    arg = arg.upper()
    stk = yfinance.Ticker(arg)

    # source data on stocks into variables
    # Note: Change period ="1d" to change timeframe of data provided
    current_data = stk.history(period="1d")
    current_descriptors = stk.info

    # Gets asset type, asset name, and asset exchange timezones
    stkType = current_descriptors["quoteType"]
    stkname = current_descriptors["shortName"]
    stkexchange = current_descriptors["exchangeTimezoneName"]

    # Gets and rounds that opening, closing,
    # and volume of stock based on the past 24 hours
    open = round(current_data['Open'][0], 2)
    close = round(current_data['Close'][0], 2)
    volume = current_data['Volume'][0]

    # Prints data to a discord message
    await message.channel.send(
        "```fix\nAsset Data Available for " + arg.upper()
        + "\n\nName:                          " + stkname
        + "\nAsset Type:                    " + stkType
        + "\nTraded Exchange:               " + stkexchange
        + "\n\nOpen price:                    " + str(open)
        + "\nLast Close Price:              " + str(close)
        + "\nVolume Sold in last 24hrs:     " + str(volume)
        + "```")


@bot.command(
    name="spotifysong",
    help="~~ Searches spotify for a track",
    brief="~~ Searches spotify for a track"
)
async def spotifysearch(message, arg):
    print("User searched Spotify for " + arg)

    client_credentials_manager = SpotifyClientCredentials(client_id=spotifyClient,
                                                          client_secret=spotifySecretClient)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    try:
        searchresults = sp.search(q=arg, type='track', limit=1)
        returnid = searchresults['tracks']['items'][0]["id"]
        await message.channel.send('https://open.spotify.com/track/' + returnid)
    except:
        await message.channel.send('Sorry, Spotify could not find that track.')


bot.run(discordtoken)
