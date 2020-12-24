import os
import pymongo
import discord
import operation

from errors import *
from discord.ext import commands

TOKEN = open("token.txt","r").readline()
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
squad_db = mongo_client["squad_template"]
op_db = mongo_client["operation_template"]
squad_collection = squad_db["template"]
op_collection = op_db["template"]

operation_dict = {}
embed_dict = {}
template_dict = {}
server_name = "BJay"
client = commands.Bot(command_prefix=".")
client.remove_command("help")

@client.event
async def on_ready():
    print(f"{client.user} has connected to discord")

@client.command(pass_context=True)
async def db(ctx, *args):

    user = ctx.message.author

    db_dict = {"show": db_show}


    await db_dict[args[0]](ctx, *args)
    await ctx.message.delete()

async def db_show(ctx, *args):

    user = ctx.message.author

    try:
        if args[1] == "squad":
            for x in squad_collection.find():
                await ctx.send(x)
        if args[1] == "operation":
            for x in op_collection.find():
                await ctx.send(x)
    except IndexError:
        user.send("Invalid Arguments")

@client.command(pass_context=True)
async def hide(ctx, *args):

    user = ctx.message.author

    for squad in args:
        embed = await ctx.channel.fetch_message(embed_dict[ctx.channel.id][squad])
        await embed.delete()

    await ctx.message.delete()

@client.command(pass_context=True)
async def close(ctx):

    user = ctx.message.author
#
#    try:
#        operation_dict[ctx.channel.id] = None
#        for embed_id in embed_dict[ctx.channel.id].values():
#            embed_msg = await ctx.channel.fetch_message(embed_id)
#            await embed_msg.delete()
#        close.stop()
#    except KeyError:
#        await user.send("Operation does not exist")

    await user.send("Not implemented")
    await ctx.message.delete()

@client.command(pass_context=True)
async def set(ctx, *args):

    user = ctx.message.author

    set_dict = {"sl": set_slfl,
            "fl": set_slfl,
            "start": set_start,
            "end": set_end,
            "template": set_template}

    try:
        await set_dict[args[1]](ctx, *args)
    except KeyError:
        await user.send("Command does not exist")
#    except IndexError:
#        await user.send("You must specify an additional option")

    await ctx.message.delete()

async def set_template(ctx, *args):

    user = ctx.message.author

    try:
        if len(args) != 3:
            raise InvalidArguments
        op = operation_dict[ctx.channel.id]
        if args[0] not in op.squads:
            raise InvalidSquad
        squad = op.squads[args[0]]
        if args[2] == "none":
            squad.set_comp(None)
        else:
            query = { "name": args[2] }
            template = squad_collection.find(query)
            for x in template:
                x.pop("_id", None)
                x.pop("name", None)
                squad.set_comp(x)
        await update_embed(ctx, args[0])
    except InvalidArguments:
        await user.send("Invalid Arguments")
    except InvalidSquad:
        await user.send("Invalid squad name")
    except AttributeError:
        await user.send("That squad does not exist")

async def set_start(ctx, *args):

    user = ctx.message.author

    try:
        if len(args) != 2:
            raise InvalidArguments
        op = operation_dict[ctx.channel.id]
        op.set_start(args[1])
        await update_embed(ctx, "op")
    except KeyError:
        await user.send("Operation does not exist")
    except InvalidArguments:
        await user.send("Invalid Arguments")

async def set_end(ctx, *args):

    user = ctx.message.author

    try:
        if len(args) != 2:
            raise InvalidArguments
        op = operation_dict[ctx.channel.id]
        op.set_end(args[1])
        await update_embed(ctx, "op")
    except KeyError:
        await user.send("Operation does not exist")
    except InvalidArguments:
        await user.send("Invalid Arguments")

async def set_slfl(ctx, *args):

    user = ctx.message.author

    try:
        if 2 >= len(args) >= 3:
            raise InvalidArguments
        op = operation_dict[ctx.channel.id]
        if args[0] not in op.squads:
            raise InvalidSquad
        squad = op.squads[args[0]]
        if len(args) == 3:
            user.nick = args[2]
        if args[1] == "sl":
            squad.set_sl(user.nick)
        elif args[1] == "fl":
            squad.set_fl(user.nick)
        else:
            raise InvalidArguments
        await update_embed(ctx, args[0])
    except AttributeError:
        await user.send("ERROR - This squad does not exist")
    except InvalidSquad:
        await user.send("ERROR - Invalid Squad")
    except InvalidArguments:
        await user.send("ERROR - Invalid parameters")
    except KeyError:
        await user.send("ERROR - Operation not created in this channel")

@client.command(pass_context=True)
async def add(ctx, *args):

    user = ctx.message.author

    try:
        if 2 >= len(args) >= 3:
            raise InvalidArguments
        op = operation_dict[ctx.channel.id]
        if args[0] not in op.squads:
            raise InvalidSquad
        squad = op.squads[args[0]]
        if len(args) == 3:
            squad.add(args[2], args[1])
        else:
            squad.add(user.nick, args[1])
        await update_embed(ctx, args[0])
    except KeyError:
        await user.send("ERROR - No operation has been created in this channel")
    except AttributeError:
        await user.send("This squad does not exist")
    except InvalidArguments:
        await user.send("ERROR - You sent bad parameters")
    except InvalidSquad:
        await user.send("ERROR - This is not a squad")
    except operation.squad.SquadCapacity:
        await user.send("Sorry, no more slots for that class")
    except operation.squad.SquadRole:
        await user.send("Sorry, that role is not valid for this squad")

    await ctx.message.delete()

@client.command(pass_context=True)
async def remove(ctx, *args):

    user = ctx.message.author

    try:
        if 1 >= len(args) >= 2:
            raise InvalidArguments
        op = operation_dict[ctx.channel.id]
        if args[0] not in op.squads:
            raise InvalidSquad
        squad = op.squads[args[0]]
        if len(args) == 2:
            user.nick = args[1]
        squad.remove(user.nick)
        await update_embed(ctx, args[0])
    except KeyError:
        await user.send("ERROR - NO operation has been created in this channel")
    except AttributeError:
        await user.send("ERROR - This squad does not exist")

    await ctx.message.delete()

@client.command(pass_context=True)
async def create(ctx, *args):

    user = ctx.message.author

    create_dict = {"operation": create_operation,
                   "squad": create_squad,
                   "squad_template": create_squad_template}

    try:
        await create_dict[args[0]](ctx, *args)
    except KeyError:
        await user.send("That command does not exist")
    except IndexError:
        await create_dict["operation"](ctx, *args)

    await ctx.message.delete()

async def create_operation(ctx, *args):

    user = ctx.message.author

    try:
        if isinstance(operation_dict[ctx.channel.id], operation.main.Operation):
            raise OperationExists
    except OperationExists:
        await user.send("ERROR - an operation already exists")
    except KeyError:
        operation_dict[ctx.channel.id] = operation.Operation()
        op = operation_dict[ctx.channel.id]
        embed_dict[ctx.channel.id] = {"op": 0, "alpha": 0, "bravo": 0, "charlie": 0, "delta": 0}

        if len(args) >= 2:
            op.set_start(args[1])
        if len(args) == 3:
            op.set_end(args[2])
        embed = discord.Embed(title="Operation Created", colour = discord.Colour.green())
        embed.set_author(name="SUCCESS!")
        embed.add_field(name="Start Time (CEST)", value=op.start, inline=True)
        embed.add_field(name="Start Time (CEST)", value=op.end, inline=True)
        embed.add_field(name="To signup to the op", value="add [squad] [class]", inline=False)
        embed.add_field(name="To remove yourself from the op", value="remove [squad] [class]", inline=False)
        embed.set_footer(text="Run help for more information")

        #embed_msg = await ctx.send(embed=embed)
#        embed_dict[ctx.channel.id]["op"] = embed_msg.id
        await display_operation(ctx, ctx.channel.id)

async def create_squad(ctx, *args):

    user = ctx.message.author
    op = operation_dict[ctx.channel.id]

    try:
        squad_name = args[1]
        squad = op.create_squad(squad_name)
        if len(args) >= 3:
            squad.set_sl(args[2])
        else:
            squad.set_sl(user.nick)
        await update_embed(ctx, squad_name)
    except operation.squad.SquadExists:
        await user.send("ERROR - squad exists")

async def update_embed(ctx, squad):

    async for embed, squad_name in generate_embed(operation_dict[ctx.channel.id]):
        if squad == squad_name:
            embed_id = embed_dict[ctx.channel.id][squad]
            embed_msg = await ctx.channel.fetch_message(embed_id)
            await embed_msg.edit(embed=embed)

async def create_squad_template(ctx, *args):

    user = ctx.message.author

    try:
        if len(args) != 2:
            raise InvalidArguments
        template = json.loads(args[1].replace("'", '"'))
        if "name" not in template:
            raise NoNameProperty
        x = squad_collection.insert(template)
        await user.send(f"Entry added to database\n{x}")
    except InvalidArguments:
        await user.send("Invalid Arguments")
    except json.decoder.JSONDecodeError:
        await user.send("Invalid template")
    except NoNameProperty:
        await user.send('Template needs "name" property')

async def generate_embed(ops):

    embed = discord.Embed(title="Operation Created", colour = discord.Colour.green())
    embed.set_author(name="SUCCESS!")
    embed.add_field(name="Start Time (CEST)", value=ops.start, inline=True)
    embed.add_field(name="Start Time (CEST)", value=ops.end, inline=True)
    embed.add_field(name="To signup to the op", value="add [squad] [class]", inline=False)
    embed.add_field(name="To remove yourself from the op", value="remove [squad] [class]", inline=False)
    embed.set_footer(text="Run help for more information")

    yield embed, "op"

    for squad_name, squad in ops.squads.items():
        if squad:
            role_dict = {}
            embed = discord.Embed(title=f"Squad Leader: {squad.sl}", colour = squad_colour(squad_name))
            embed.set_author(name=f"Squad: {squad_name}")
            embed.add_field(name=f"Fireteam Lead", value=squad.fl, inline=False)
            role_summary = ""
            if squad.composition is not None:
                for role, count in squad.composition.items():
                    role_summary += f"{role}={int(count)} "
            else:
                role_summary = "No Restrictions"
            embed.add_field(name=f"Composition", value=role_summary, inline=False)
            for member, role in squad.members.items():
                role = role.upper()
                if role_dict.get(role) is None:
                    role_dict[role] = [member]
                else:
                    role_dict[role].append(f"\n{member}")
            for role, members in role_dict.items():
                role = role.upper()
                member_string = ""
                for member in members:
                    member_string += member
                embed.add_field(name=role, value=member_string, inline=False)
            embed.set_footer(text="Run help for more information")
        else:
            embed = discord.Embed(title="NOT CREATED", colour = discord.Colour.red())
            embed.set_author(name=f"Squad: {squad_name}")
            embed.add_field(name=f"To create a squad", value=f"create {squad_name} [squad_lead]", inline=False)
            embed.set_footer(text="Run help for more information")

        yield embed, squad_name


async def display_operation(ctx, channel_id):

    async for embed, squad_name in generate_embed(operation_dict[ctx.channel.id]):
        embed_msg = await ctx.send(embed=embed)
        embed_dict[channel_id][squad_name] = embed_msg.id

def squad_colour(squad):

    squad_colour_dict = {"alpha": discord.Colour.green(),
            "bravo": discord.Colour.gold(),
            "charlie": discord.Colour.purple(),
            "delta": discord.Colour.dark_theme()}

    return squad_colour_dict[squad]

@client.command(pass_context=True)
async def inspect(ctx, var, *args):

    var_dict = {"op_dict": operation_dict,
            "embed_dict": embed_dict,
            "template_dict": template_dict}

    await ctx.send(var_dict[var])

@client.command(pass_context=True)
async def debug(ctx):

    message = ""
    op = operation_dict[ctx.channel.id]
    message += f"{op}"
    squads = op.squads
    message += "\n################\n"
    for squad in squads:
        message += f"{squads[squad]}"

    await ctx.send(message)

client.run(TOKEN)
