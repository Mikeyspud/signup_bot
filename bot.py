import pymongo                          #mongodb API
import discord                          #discord API
from discord.ext import commands        #discord API

from modules import handlers, 
    settings,
    functions


#TOKEN required to authenticate with Discord API Servers
TOKEN = open("token.txt", "r").readline()

#Command Prefix (This can be changed without adverse affects)
client = commands.Bot(command_prefix=".")

#Removes the built-in help command so that we can add our own later
client.remove_command("help")

@client.event
async def on_ready():
    settings.init()
    print(f"{client.user} has connected to discord")


@client.command(pass_context=True)
async def show(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Show(ctx, *args)
    await handler()


@client.command(pass_context=True)
async def load(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Load(ctx, *args)
    await handler()


@client.command(pass_context=True)
async def close(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Close(ctx, *args)
    await handler()


@client.command(pass_context=True)
async def create(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Create(ctx, *args)
    await handler()
    await functions.update_operation_summary(ctx)


@client.command(pass_context=True)
async def help(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Help(ctx, *args)
    await handler()


@client.command(pass_context=True)
async def save(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Save(ctx, *args)
    await handler()


@client.command(pass_context=True)
async def alias(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Alias(ctx, *args)
    await handler()


@client.command(pass_context=True)
async def squad(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Squad(ctx, *args)
    await handler()
    await functions.update_operation_summary(ctx)


@client.command(pass_context=True)
async def add(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Add(ctx, *args)
    await handler()
    await functions.update_operation_summary(ctx)


@client.command(pass_context=True)
async def remove(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Remove(ctx, *args)
    await handler()
    await functions.update_operation_summary(ctx)


@client.command(pass_context=True)
async def debug(ctx, *args):

    await ctx.message.delete()
    handler = handlers.Debug(ctx, *args)
    await handler()


'''
We pull the alias data from the database and immediately load it into memory
because i dont know tbh

maybe change it later
'''
functions.update_alias_dict()
client.run(TOKEN)
