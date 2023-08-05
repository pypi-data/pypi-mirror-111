# [Tawpy](https://tenor.com/gifapi/documentation)

An `non-asynchronous` api wrapper writen in python originally made to be used for [discord.py](https://discordpy.readthedocs.io/en/stable/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)



## Features 
-   Almost full coverage of the `Tenor` api

-   The ability to request gifs from the `Tenor`  website


## Up-Coming Changes
-   The ability to use `Asynchronous Programming`

-   `Reduced` GIF wait time 

-   The fix of `tenor_random_request` and `custom_random_request` functions 

## Installing 
### Requires Python Version's 3+

```sh
# Linux/macOS
python3 -m pip install -U tawpy

# Windows
py -3 -m pip install -U tawpy
```
To install the development version and contribute do: 
```sh
$ git clone https://github.com/devKeef/tawpy
$ cd tawpy
```


## Quick Example
```py
from tawpy import Tapi 
from tawpy import Enum 

tenor_client = Tapi() # Creating the client

print(tenor_client.tenor_search_request(query="sad")) # Returns a tuple of gif urls

""" 
OUTPUT 

('https://media.tenor.com/images/8a9c48bd8de465b549dc8684bf6404a4/tenor.gif', 
'https://media.tenor.com/images/b19863ff5624c88e81d0570c5d85e430/tenor.gif', 
'https://media.tenor.com/images/b69ac21acadfd8c3ece06e29f26d9fdf/tenor.gif', 
'https://media.tenor.com/images/1f42c4f00f1ae7c560bfbf329b767976/tenor.gif', 
'https://media.tenor.com/images/3e35e47384653347a72b0626ed90cfe6/tenor.gif')
"""
```
## Documentation 
This section of the markdown file contains the duties of specific functions and their parameters and how they affect the set `tuple` of gifs you reviece from `Tenor`
## Paremters
```
Keep in mind that these are all keyword-arguments 
there are no positional arguments all functions 
are keyword-argument based.


query: str
The tag to be used to find an array or specific gif from 
the tenor website.

limt: int = 5 
The number of gifs that you would like to request from the 
tenor website with each call.

contentfilter: Enum = Enum.ContentFilter.LOW 
The the content safety of gifs requested from
the tenor website with each call.

mediafilter: Enum = Enum.MediaFilter.GIF 
The format in which the gifs are returned in.

pos: int = 5
The position you want to start collection gif's from.

locale: Enum = Enum.LocaleMedida.EN_US 
The default language to interpret search string.
```
## Methods
```
All methods in this section returns a tuple of gif urls 
from tenor. 

def tenor_search_request(
    self , *,
    query: str ,
    limit: int = 5 , 
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    pos: int = 0 , 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:


This function request gif's from the tenor 
website starting listed most popular gif's to least.

def tenor_trending_request(
    self , *,
    limit: int = 5 , 
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:

This function request trending gif's 
from the tenor website listed most popular gif's to least.


def custom_random_request(
    self , *,
    query: str ,
    limit: int = 5 , 
    pos: int = 5 ,
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:

This function request random gif's from the tenor website with each call
When i say random i mean random the listing order is not most popular to least 
it is random completey random. 


def tenor_random_request(
    self , *,
    query: str ,
    limit: int = 5 , 
    pos: int = 0 ,
    contentfilter: Enum = Enum.ContentFilter.OFF , 
    mediafilter: Enum = Enum.MediaFilter.GIF, 
    locale: Enum = Enum.LocaleMedia.EN_US
) -> tuple[str]:

This function request random gif's from the tenor website
would use tenor_gif_search if i were you.
```
## Enums 
```
Content Filters

OFF: MAY INCLUDED NSFW GIFS
LOW: A LOWER RISK OF NSFW GIFS 
MEDIUM: AN EVEN LOWER RISK OF NSFW GIFS 
HIGH: THE LOWEST RISK OF NSFW GIFS


Media Filters

Gifs
----
GIF: HIGH QUALITY GIF FORMAT , LARGEST FORMAT OF GIF
MEDIUMGIF: SMALL REDUCTION OF GIF FORMAT
TINYGIF: REDUCED SIZE OF THE GIF FORMAT
NANOGIF: SMALLEST SIZE OF GIF FORMAT

Mp4
---
MP4: HIGH QUALITY MP4 FORMAT , LARGEST FORMAT OF MP4
LOOPEDMP4: SAME AS MP4
TINYMP4: REDUCED SIZE OF THE MP4 FORMAT
NANOMP4: SMALLEST SIZE OF MP4 FORM
WEBM
----
WEBM: LOWER QUALITY VIDEO FORMAT
TINYWEBM: REDUCED SIZE OF WEBM FORMAT 
NANOWEBM: SMALLEST SIZE OF WEBM FORMAT


Language Codes 

ZH_CN: CHINESE
ZH_TW: TAIWAN
EN_US: ENGLISH 
FR_FR: FRENCH
DE_DE: GERMAN
IT_IT: ITALIAN 
JA_JP: JAPANESE
KO_KR: KOREAN
PT_BR: PORTUGUESE
ES_ES: SPANISH
```
## Implementing In Discord Bot Example
### Before we begin If you don't know what `discord.py` is. Visit [discord.py](https://discordpy.readthedocs.io/en/stable/)
In this example which is placed below shows how the api wrapper is to be 
used when making a `discord bot`
```py
import discord 
from discord.ext import commands
from tawpy import Tapi # Import the "Tapi" Class from the "tawpy" module
from tawpy import Enum # Import the Enums Class from the "tawpy" module

token = "YOUR_API_KEY"

tenor_client = Tapi() # Create a Tapi Object ( Object used to get information from tenor )
discord_client = commands.Bot(command_prefix="!") # Create a Discord Client Object

@discord_client.event
async def on_ready(): 
    return print("running...")

@discord_client.command() 
async def gif(ctx , *,q: str): 
    # Use the tenor_search_request function 
    # To get a tuple of gifs ranging from the 
    # Most popular to the least
    gif_urls = tenor_client.tenor_search_request(
        query = q , 
        limit = 1 , 
        mediafilter = Enum.MediaFilter.GIF
    )

    await ctx.send(gif_urls[0]) # Since it returns a tuple select index [0] Or any suitable index

    
discord_client.run(token) # Start the discord client
```

## Implementing In Discord Bot Example With Cogs
```py
import discord 
from discord.ext import commands
from tawpy import Tapi # Import the "Tapi" Class from the "tawpy" module
from tawpy import Enum # Import the Enums Class from the "tawpy" module
import os

token = "YOUR_API_KEY"

class MyDiscordClient(commands.Bot): 
    def __init__(self , **kwargs): 
        super(**kwargs)
        self.tenor_client = Tapi() # Create the tenor client to be used anywhere
        self.tenor_enums = Enum()
    
    async def on_ready(self): 
        return print("running")
    
discord_client = MyDicordClient(command_prefix="!")

for file in os.listdir("./cogs"):
    if file.endswith(".py"): 
        discord_client.load_extension("cogs.%s" % (file[:-3]))

discord_client.run(token)
```

Create a cog folder and a new file called `tenor.py` 
and do as followed , if you're already furmiliar with `discord.py` feel 
free to skip ahead

```py
import discord 
from discord.ext import commands

class GifCommands(commands.Cog): 
    def __init__(self , client): 
        self.client = client 

        @commands.command() 
        async def gif(self , ctx , *, query: str): 
            return await ctx.send("GIF:\n%s" % (self.tenor_client.tenor_search_request(
                query = query , 
                limit = 1
            )))

def setup(client): 
    client.add_cog(GifCommands(client))
```