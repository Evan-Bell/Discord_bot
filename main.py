import discord
import os
import random
from replit import db
import requests
import datetime
import asyncio
import datetime as dt
from discord.ext import commands, tasks

#keeps server alive
from keep_alive import keep_alive

from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='$')

lettuce_chat = 825616071531692065
testing_chat = 825944894106763295
bot_command_chat = 826080181075705867


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("------")
    bday_check.start()


if "shows" not in db.keys():
    db["shows"] = []
if "todo" not in db.keys():
    db["todo"] = []
if "bdays" not in db.keys():
    db["bdays"] = []

#list of all commands and their functions
help_commands = [
    [
        "General", "$hello - _ get insulted _",
        "$help - _ get list of all commands _",
        "$all - _ lists all shows and todo items _"
    ],
    [
        "Shows",
        "$shows - _ list all shows on file _",
        "$as [] - _ add a show to list (EX:  '$as Seinfield' ) _",
        #"$ss []  - _ search for if a show is on list _",
        "$rs [] - _ remove a show from list (EX:  '$rs Seinfield' )_"
    ],
    [
        "Todo",
        "$todo - _ list all todo tasks _",
        "$at [] - _ add a todo to list (EX:  '$at Have Fun' )_",
        #"$st []  - _ search for if a todo is on list _",
        "$rt [] - _ remove a todo from list (EX:  '$rt Have Fun' )_"
    ],
    [
        "Birthdays",
        "$bday - _ list all birthdays on file _",
        "$ab [] - _ add a bday to list (EX:  '$ab Billy - 02/29' ) _",
        #"$ss []  - _ search for if a show is on list _",
        "$rb [] - _ remove a bday from list (EX:  '$rb Billy - 02/29' )_"
    ]
]


#chooses a random insult for the $hello command
def get_insult():
    insults = [
        "Suck my dick, %s", "Eat shit %s", "%s is a BITCH",
        "I'd kill %s if I had hands",
        "Wow, %s makes me want to kill myself, and i'm not even alive",
        "Fuck you, %s", "Hey, %s", "Yo, what's up %s",
        "You look like you need to be bitch slapped %s", ":weary:  %s"
    ]

    insult = random.choice(insults)
    return insult


#HELLO responds to a $hello with a random insult with the person's name, either gen from online, or chooses from my written list
@bot.command(name='hello')
async def greet(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    response = requests.get(
        'https://evilinsult.com/generate_insult.php?lang=en&type=json')
    if response.status_code == 200:  #set this to 200 for this portion to run over the other
        temp = response.text
        temp = temp[temp.index("insult") + 9:temp.index("created") - 3]
        await ctx.reply(temp)

    elif response.status_code == 404:
        choice = get_insult() % str(ctx.author.display_name)
        await ctx.reply(choice)


#HELP sends list of all commands and their functions
@bot.remove_command("help")
@bot.command(name='help')
async def help(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "All Commands"
    desc = "This is a list of all bot commands and their functions"
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    for each in help_commands:
        nme = "**%s**" % each[0]
        desc = "\n".join(each[1:])
        embed.add_field(name=nme, value=desc, inline=False)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#ALL sends list of all shows and todo
@bot.command(name='all')
async def all(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Full list of both Shows and Todo list**"
    desc = ""
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.add_field(name="**Shows**", value=list_shows(), inline=True)
    embed.add_field(name="**Todo**", value=list_todo(), inline=True)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#SHOWS sends list of shows
@bot.command(name='shows')
async def shows(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Shows**"
    desc = list_shows()
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#ADDSHOW adds a show
@bot.command(name='as')
async def a_s(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Shows**"
    desc = add_show(ctx.message.content.split("$as ", 1)[1])
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#DELSHOW removes a show
@bot.command(name='rs')
async def rs(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Shows**"
    desc = remove_show(ctx.message.content.split("$rs ", 1)[1])
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#TODO gets list of todo tasks
@bot.command(name='todo')
async def todo(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Todo List**"
    desc = list_todo()
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#ADDTODO adds a todo item
@bot.command(name='at')
async def a_t(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Todo List**"
    desc = add_todo(ctx.message.content.split("$at ", 1)[1])
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#DELTODO removes a todo item
@bot.command(name='rt')
async def rt(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Todo List**"
    desc = remove_todo(ctx.message.content.split("$rt ", 1)[1])
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#BDAY gets list of bday
@bot.command(name='bday')
async def bday(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Birthday List**"
    desc = list_bday()
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#ADDBDAY adds a bday item
@bot.command(name='ab')
async def ab(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Birthday List**"
    desc = add_bday(ctx.message.content.split("$ab ", 1)[1].lower())
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#DELBDAY removes a Bday item
@bot.command(name='rb')
async def rb(ctx):
    if not (ctx.channel.id == testing_chat
            or ctx.channel.id == bot_command_chat):
        return
    title = "**Birthday List**"
    desc = remove_bday(ctx.message.content.split("$rb ", 1)[1].lower())
    color = 0xFF5733
    embed = discord.Embed(title=title, description=desc, color=color)

    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


#adds show to db
def add_show(show):
    if (show not in db["shows"]):
        temp = db["shows"]
        temp.append(show)
        db["shows"] = temp
        return "%s was added to shows list %s" % (show, list_shows())
    return "Sorry, %s is already in there :( %s" % (show, list_shows())


#grabs shows from db and formats
def list_shows():
    if (len(db["shows"]) == 0):
        return "**Nothing in the Shows List :(**"
    shws = db["shows"]
    res = "\n"
    for each in shws:
        ol = str(shws.index(each) + 1)
        res = "%s%s. %s\n" % (res, ol, each)
    return "\n%s" % str(res)


#removes show from db and formats for clarity
def remove_show(show):
    if (show in db["shows"]):
        shws = list_shows()
        x = shws.find(show)
        res = "%s~~%s~~%s" % (shws[:x], shws[x:x + len(show)],
                              shws[x + len(show):])
        temp = db["shows"]
        temp.remove(show)
        db["shows"] = temp
        return "%s was removed from Shows list %s" % (show, res)
    return "%s was not in list :(" % show


def search_show():
    return


#adds todo task to db
def add_todo(task):
    if (task not in db["todo"]):
        temp = db["todo"]
        temp.append(task)
        db["todo"] = temp
        return "%s was added to Todo list %s" % (task, list_todo())
    return "Sorry, %s is already in there :( %s" % (task, list_todo())


#grabs todo from db and formats
def list_todo():
    if (len(db["todo"]) == 0):
        return "**Nothing in the Todo List :(**"
    tsks = db["todo"]
    res = "\n"
    for each in tsks:
        ol = str(tsks.index(each) + 1)
        res = "%s%s. %s\n" % (res, ol, each)
    return "\n%s" % str(res)


#removes show from db and formats for clarity
def remove_todo(task):
    if (task in db["todo"]):
        tsks = list_todo()
        x = tsks.find(task)
        res = "%s~~%s~~%s" % (tsks[:x], tsks[x:x + len(task)],
                              tsks[x + len(task):])
        temp = db["todo"]
        temp.remove(task)
        db["todo"] = temp
        return "%s was removed from Todo list %s" % (task, res)
    return "%s was not in list :(" % task


def search_todo():
    return


def sort_bday():
    bdays = [each.split("-") for each in db["bdays"]]
    bdays.sort(key=lambda x: x[1])
    bdays = [each[0] + "-" + each[1] for each in bdays]
    db["bdays"] = bdays
    return None


#adds bday to db
def add_bday(bday):
    if ("-" not in bday or "/" not in bday):
        return "%s is invalid input, try again, and **get it right this time you bum**" % bday
    if (bday not in db["bdays"]):
        temp = db["bdays"]
        temp.append(bday)
        db["bdays"] = temp
        return "%s was added to Bday list %s" % (bday.capitalize(),
                                                 list_bday())
    return "Sorry, %s is already in there %s" % (bday.capitalize(),
                                                 list_bday())


#grabs bdays from db
def list_bday():
    sort_bday()
    if (len(db["bdays"]) == 0):
        return "**Nothing in the Bday List :(**"
    bdays = db["bdays"]
    res = "\n"
    for each in bdays:
        res = "%s %s\n" % (res, each.capitalize())
    return "\n%s" % str(res)


#removes bday from db and formats for clarity
def remove_bday(bday):
    if (bday in db["bdays"]):
        bdays = list_bday()
        bdays = bdays.lower()
        x = bdays.find(bday)
        res = "%s~~%s~~%s" % (bdays[:x], bdays[x:x + len(bday)],
                              bdays[x + len(bday):])
        temp = db["bdays"]
        temp.remove(bday)
        db["bdays"] = temp
        return "%s was removed from Bday list %s" % (bday.capitalize(), res)
    return "%s was not in list :(" % bday.capitalize()


@tasks.loop(hours=24)
async def bday_check():
    channel = bot.get_channel(testing_chat)
    #await channel.send("b-day check")
    e = datetime.datetime.now()
    bdays = [each.split("-") for each in db["bdays"]]
    day = (e.strftime("%m/%d"))
    bdays_today = []
    for each in bdays:
        if each[1].strip() == day:
            bdays_today.append(each[0].strip())
    if (len(bdays_today) > 0):
        title = "**HAPPY BIRTHDAY %s!!!**" % bdays_today[0].upper()
        desc = "Happy Birthday Yay! :relieved::leafy_green: :tada: :partying_face::birthday::tada::confetti_ball::gift:"
        color = 0xff00bf
        embed = discord.Embed(title=title, description=desc, color=color)

        embed.set_thumbnail(url="https://i.imgur.com/Q2ZST9f.jpg")
        embed.set_footer(text="@everyone")

        channel = bot.get_channel(lettuce_chat)
        await channel.send(embed=embed)
        await channel.send(
            "https://youtu.be/oBloyiprdEM \n https://youtu.be/HvYgke2fBeg")
    await asyncio.sleep(60)


@bday_check.before_loop
async def before_bday_check():
    print(dt.datetime.now().hour)
    print(dt.datetime.now().minute)
    for _ in range(24 * 60):  # loop the whole day

        if dt.datetime.now().hour == 13 and dt.datetime.now(
        ).minute == 0:  # 24 hour format, 13 is 8AM my time
            print('It is time')
            return
        await asyncio.sleep(60)


#blocks sofia from chatting or being mentioned
# @bot.event
# async def on_message(message):
#   msg = message.content
#   if (str(message.author) == "sofia f#6356" or msg.find("sofia") != -1):
#       time.sleep(1)
#       await message.delete()

#keeps server alive when tab is closed
keep_alive()

#runs all
bot.run(os.getenv('TOKEN'))
