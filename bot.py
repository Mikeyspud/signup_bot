import pymongo                          #mongodb API
import discord                          #discord API
from discord.ext import commands        #discord API
import json                             #used to dictify json strings

import operation                        #custom objects
from errors import *                    #custom errors


#TOKEN required to authenticate with Discord API Servers
TOKEN = open("token.txt", "r").readline()

#Mongodb variables
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

squad_db = mongo_client["squad_template"]
squad_collection = squad_db["template"]

op_db = mongo_client["operation_template"]
op_collection = mongo_client["template"]

alias_db = mongo_client["alias"]
alias_collection = mongo_client["alias"]

#General Global Variables
#Holds the discord channel id's where operations have been started
operation_dict = {}

#Nested dict that holds the message id's for each squad and its embedded message
embed_dict = {}

#History dict that holds the command history for each channel id
history_dict = {}

#Alias dict stores the alias names for roles
alias_dict = {}

#Server Name
server_name = "BJay"

#Command Prefix (This can be changed without adverse affects)
client = commands.Bot(command_prefix=".")

#Removes the built-in help command so that we can add our own later
client.remove_command("help")


@client.event
async def on_ready():
    print(f"{client.user} has connected to discord")


'''
Command listener for alias command
Alias command syntax:
    .alias [role] [alias] [alias] -> infinity
'''
@client.command(pass_context=True)
async def alias(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    Checks if the number of arguments supplied is correct. If not raise InvalidArguments and
    inform the user
    '''
    if len(args) < 2:
        await user.send(embed=debug_message(error_class="warning",
            message=f"Alias: syntax is as follows = .alias [role] [alias-1...alias-n]",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    if args[0] is "force". Then we overwrite existing aliases and remove mentions of each alias
    in other roles
    '''
    if args[0] == "force":
        await alias_force(ctx, *args)
    else:

        '''
        Checks if a request alias is already an alias for another class
        OR if reqeusted alias is already a class
        '''
        for alias in args[1:]:
            if alias in alias_dict:
                await user.send(embed=debug_message(error_class="information",
                    message=f"Alias: alias {alias} is already a role",
                    channel_id=channel_id))
                await ctx.message.delete()
                raise InvalidArguments

        for role, alias_set in alias_dict.items():
            for alias in alias_set:
                if alias in args[1:]:
                    await user.send(embed=debug_message(error_class="information",
                        message=f"Alias: {alias} is already an alias for {role}",
                        channel_id=channel_id))
                    await ctx.message.delete()
                    raise InvalidArguments

        role = args[0]
        if role not in alias_dict:
            alias_dict[role] = set()

        alias_dict[role].update(args[1:])

    '''
    Updates the alias database entry on mongodb. First, the alias_set needs to be
    converted into a JSON String
    '''
    #json_alias_dict = json.loads(alias_dict)
    #alias_collection.insert(alias_dict)

    await ctx.message.delete()

'''
Alias Force allows a user to update an existing alias entry
'''
async def alias_force(ctx, *args):

    for role, alias_set in alias_dict.items():
        for alias in args[2:]:
            alias_set.discard(alias)

    role = args[1]
    alias_dict[role] = set()
    alias_dict[role].update(args[2:])

'''
The command listener for the 'create' command
'''
@client.command(pass_context=True)
async def create(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    The list of arguments for the create command

    operation - Creates a new operation in that discord channel
    squad - Creates a new squad for the operation in that discord channel
    '''
    commands = {"operation": create_operation,
                "squad": create_squad}

    '''
    Checks for args[0] (create argument). If it does not exist inform the user who sent
    the command by sending them a direct embed message before raising InvalidArguments to
    prevent additional errors
    '''
    try:
        command = args[0]
    except IndexError:
        await user.send(embed=debug_message(error_class="information",
            message=f"Command: create - takes the following arguments\n{str(commands.keys())}",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Calls the respective function inside the command_dict depending on args[0].
    If there is no respective function, then inform the user they sent the wrong argument
    with the 'create {args[0]}' command
    '''
    try:
        await commands[command](ctx, *args)
    except KeyError:
        await user.send(embed=debug_message(error_class="information",
            message=f"Command: create {args[0]} does not exist",
            channel_id=channel_id))

    update_history_dict(channel_id, ctx.message.content)
    await ctx.message.delete()

async def create_operation(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id


    '''
    Checks for the existence of arg[1]. If it doesnt exist, inform the user
    they missed a positional argument
    '''
    try:
        operation_name = args[1]
    except IndexError:
        await user.send(embed=debug_message(error_class="warning",
            message=f"Command create operation - takes the following positional arguments\n[name]",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Checks operation_dict for an existing operation in that channel_id. If there is no
    existing operation, then create it, assign it the name args[1] and send a summary of the operation in
    the channel. If there is an existing operation, then inform the user.
    '''
    if channel_id not in operation_dict:
        operation_dict[channel_id] = operation.Operation(name=operation_name)
        embed_dict[channel_id] = {"op": None, "alpha": None, "bravo": None, "charlie": None, "delta": None}
        await update_operation_summary(ctx)
    else:
        operation_name = operation_dict[channel_id].name
        await user.send(embed=debug_message(error_class="error",
            message=f"Operation: {operation_name} exists in channel {channel_id}",
            channel_id=channel_id))

async def create_squad(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    Checks for existence of args[1] (squad_name). If it doesnt exist, inform
    the user they missed a positional argument
    '''

    try:
        squad_name = args[1]
    except:
        await user.send(embed=debug_message(error_class="warning",
            message=f"Command create squad - takes the following positional arguments\n[squad_name]",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Checks the existence of the operation in that channel_id. If there is no existing operation,
    inform the user, delete their message and raise NoOperationExists to prevent further errors
    '''
    if channel_id not in operation_dict:
        await user.send(embed=debug_message(error_class="error",
            message=f"Operation: does not exist in this channel. Please create one",
            channel_id=channel_id))
        await ctx.message.delete()
        raise NoOperationExists

    '''
    Attempts to create the squad [args(1)]. Squad name should be valid. If the squad exists, inform the user.
    If the squad_name is invalid, inform the user
    '''
    operation_object = operation_dict[channel_id]
    if squad_name not in operation_object.squads:
        await user.send(embed=debug_message(error_class="warning",
            message=f"Squad: {squad_name} is not a valid squad name. Please choose alpha|bravo|charlie|delta",
            channel_id=channel_id))
    elif isinstance(operation_object.squads[squad_name], operation.squad.Squad):
        await user.send(embed=debug_message(error_class="warning",
            message=f"Squad: {squad_name} already exists for operation {operation_object.name}",
            channel_id=channel_id))
    else:
        operation_object.squads[squad_name] = operation.squad.Squad()
        await update_operation_summary(ctx)


@client.command(pass_context=True)
async def squad(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    The list of arguments for the squad command

    composition - Sets the squad composition
    sl - Sets the squad sl
    fl - Sets the squad fl
    '''
    command_list = ["composition", "sl", "fl"]

    '''
    The squad command should only take 3 arguments. Therefor, raise InvalidArguments to prevent further errors
    and inform the user
    '''
    if len(args) != 3:
        await ctx.send(len(args))
        await user.send(embed=debug_message(error_class="warning",
            message=f"Command: squad takes the following argument {command_list} - Exmaple: squad alpha sl bob",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Checks for args[1] (create argument). If it does not exist inform the user who sent
    the command by sending them a direct embed message before raising InvalidArguments to
    prevent additional errors
    '''
    if args[1] not in command_list:
        await user.send(embed=debug_message(error_class="information",
            message=f"Command: squad - takes the following arguments {command_list} - Example: squad alpha sl bob",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments
    else:
        command = args[1]

    '''
    Checks to see if an operation exists in the channel. If not,
    inform the user and raise NoOperationExists to prevent further errors
    '''
    try:
        operation_object = operation_dict[channel_id]
    except KeyError:
        await user.send(embed=debug_message(error_class="error",
            message="Squad: No operation created in this channel yet",
            channel_id=channel_id))
        await ctx.message.delete()
        raise NoOperationExists


    '''
    Checks if args[0] (squad name) is a valid squad name. If not, inform the user and raise
    InvaldArguments to prevent further errors
    '''
    if args[0] not in operation_object.squads:
        await user.send(embed=debug_message(error_class="error",
            message=f"Squad: {args[0]} is not a valid squad. Please use alpha|bravo|charlie|delta",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments
    else:
        squad_name = args[0]
        squad = operation_object.squads[squad_name]

    '''
    The command issued (args[1]) will execute the respective block of code
    '''
    if command  == "composition":
        '''
        If the composition sent is not a JSON String, inform the user and raise InvalidArguments
        to prevent any further errors.
        '''
        try:
            composition = json.loads(args[2].replace("'", '"'))
            squad.composition = composition
            update_history_dict(channel_id, ctx.message.content)
        except json.decoder.JSONDecodeError:
            await user.send(embed=debug_message(error_class="warning",
                message=f"Squad: {args[0]} composition {args[2]} is not a valid composition\nNeeds to be JSON String",
                channel_id=channel_id))
            await ctx.message.delete()
            raise InvalidArguments
    elif command == "sl":
        squad_leader = args[2]
        squad.sl = squad_leader
    else:
        fireteam_leader = args[2]
        squad.fl = fireteam_leader

    await update_operation_summary(ctx)
    await ctx.message.delete()

@client.command(pass_context=True)
async def squad_composition(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    Checks to see if an operation exists in the channel. If not,
    inform the user and raise NoOperationExists to prevent further errors
    '''
    try:
        operation_object = operation_dict[channel_id]
    except KeyError:
        await user.send(embed=debug_message(error_class="error",
            message="Squad: No operation created in this channel yet",
            channel_id=channel_id))
        await ctx.message.delete()
        raise NoOperationExists

    '''
    Checks if the appriopriate number of arguments have been sent.
    If not, inform the user and then raise InvalidArguments to prevent any
    other errors
    '''
    if len(args) == 3:
        await user.send(embed=debug_message(error_class="error",
            message="Add: not sent correct number of arguments. The syntax is \nsquad [squad_name] composition [composition]",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments


@client.command(pass_context=True)
async def add(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    Checks to see if an operation exists in the channel. If not,
    inform the user and raise NoOperationExists to prevent further errors
    '''
    try:
        operation_object = operation_dict[channel_id]
    except KeyError:
        await user.send(embed=debug_message(error_class="error",
            message="Add: No operation created in this channel yet",
            channel_id=channel_id))
        await ctx.message.delete()
        raise NoOperationExists

    '''
    Checks if the appriopriate number of arguments have been sent.
    If not, inform the user and then raise InvalidArguments to prevent any
    other errors
    '''
    if 2 > len(args) > 3:
        await user.send(embed=debug_message(error_class="error",
            message="Add: not sent correct number of arguments. The syntax is \nadd [squad] [role] (squad_role)",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Checks if args[0] (squad name) is a valid squad name. If not, inform the user and raise
    InvaldArguments to prevent further errors
    '''
    if args[0] not in operation_object.squads:
        await user.send(embed=debug_message(error_class="error",
            message=f"Add: {args[0]} is not a valid squad. Please use alpha|bravo|charlie|delta",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Checks if args[2] (sl or fl) is a valid argument. If not, inform the user and raise
    InvalidArguments to prevent further errors
    '''
    try:
        if args[2] not in ["sl", "fl"]:
            await user.send(embed=debug_message(error_class="error",
                message=f"Add: {args[2]} is not a valid squad_role. Please use sl|fl",
                channel_id=channel_id))
            await ctx.message.delete()
            raise InvalidArguments
    except IndexError:
        pass

    squad_name = args[0]
    role = args[1]
    squad = operation_object.squads[squad_name]

    '''
    Check if role is an alias for another role
    '''
    for key, alias_set in alias_dict.items():
        if role in alias_dict[key]:
            role = key

    '''
    Checks that the user hasnt signed up to the squad with that role already. If they have
    inform them they are dumb
    '''
    for member in squad.members:
        if member.name == user.display_name and member.role == role:
            await user.send(embed=debug_message(error_class="information",
                message=f"You have the memory of a goldfish and/or cannot read. You have already signed up with that class",
                channel_id=channel_id))
            await ctx.message.delete()
            raise InvalidArguments

    '''
    Checks the squad composition to see if it can accomodate the new addition
    '''
    if await check_squad_composition(ctx, squad, role):
        squad.add(user.display_name, role)
        try:
            if args[2] == "sl":
                squad.sl = user.display_name
                '''
                Checks is user being added as sl is already fl.
                If he is fl, then remove from fl
                '''
                if squad.fl == user.display_name:
                    squad.fl = None
            if args[2] == "fl":
                squad.fl = user.display_name
                '''
                Checks if user being added as fl is already sl.
                If he is sl, then remove from sl
                '''
                if squad.sl == user.display_name:
                    squad.sl = None
        except IndexError:
            pass

    await update_operation_summary(ctx)
    await ctx.message.delete()

@client.command(pass_context=True)
async def remove(ctx, *args):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    Checks to see if an operation has been created in the channel.
    If not, inform the user and raise InvalidArguments to prevent further errors
    '''
    try:
        operation_object = operation_dict[channel_id]
    except IndexError:
        await user.send(embed=debug_message(error_class="error",
            message=f"Remove: No operation created in this channel",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    '''
    Checks to see if a valid squad has been provided (args[0]). If not, inform
    the user and raise InvalidArguments to prevent further errors
    '''
    if args[0] not in operation_object.squads:
        await user.send(embed=debug_message(error_class="error",
            message="Remove: Not a valid squad name. Please choose alpha|bravo|charlie|delta",
            channel_id=channel_id))
        await ctx.message.delete()
        raise InvalidArguments

    squad_name = args[0]
    squad = operation_object.squads[squad_name]
    squad.remove(user.display_name)

    await ctx.message.delete()

async def check_squad_composition(ctx, squad, role):

    user = ctx.message.author
    channel_id = ctx.channel.id

    '''
    Checks operation.squad.Squad.composition and returns False if there is no room.
    Will return True if there is room OR if composition is None
    '''

    if squad.composition is None:
        return True

    '''
    Checks if the role is in squad. If not, then it is an invalid role and the user
    should be informed. operation.squad.SquadRole is raised to prevent any further errors
    '''
    if role not in squad.composition:
        await user.send(embed=debug_message(error_class="warning",
            message=f"Role: {role} is not a valid role for squad {squad}",
            channel_id=channel_id))
        await ctx.message.delete()
        raise operation.squad.SquadRole


    if squad.composition[role] >= 1:
        return True
    else:
        await user.send(embed=debug_message(error_class="information",
            message=f"Add: There is no room in the squad for that role",
            channel_id=channel_id))
        return False

async def update_operation_summary(ctx):

    channel_id = ctx.channel.id
    operation_object = operation_dict[channel_id]

    '''
    Calls the generate_embed generator. The generate_embed generator returns a discord.Embed
    object. We will then check if an embed has already been sent for each squadby referring
    to embed_dict. If it has, then it will update the existing embed. If not, it will send a new embed
    '''

    async for embed, squad in generate_embed(operation_object):
        if embed_dict[channel_id][squad] and embed:
            embed_id = embed_dict[channel_id][squad]
            embed_message = await ctx.channel.fetch_message(embed_id)
            await embed_message.edit(embed=embed)
        elif embed:
            embed_message = await ctx.send(embed=embed)
            embed_dict[channel_id][squad] = embed_message.id
        else:
            embed_dict[channel_id][squad] = embed

async def generate_embed(operation_object):

    '''
    Generator that yields a discord.Embed object and the appropriate squad_name.
    First we need to create the embed for the operation and then yield it under the squad_name "op"
    '''
    embed = discord.Embed(title=f"Operation {operation_object.name} Created", colour=discord.Colour.green())
    embed.set_author(name="SUCCESS!")
    embed.add_field(name="Start Time (CEST)", value=operation_object.start, inline=True)
    embed.add_field(name="End Time (CEST)", value=operation_object.end, inline=True)
    embed.add_field(name="To signup to the op", value="add [squad] [class]", inline=False)
    embed.add_field(name="To remove yourself from the op", value="remove [squad]", inline=False)

    yield embed, "op"

    '''
    A dictionary that defines the colour for the embed depending on the squad_name
    '''
    squad_colour_dict = {"alpha": discord.Colour.green(),
            "bravo": discord.Colour.gold(),
            "charlie": discord.Colour.purple(),
            "delta": discord.Colour.dark_theme()}


    '''
    Now, we generate an embed for every active squad in the operation and yield. If the squad is not active, we yield None, None
    '''
    for squad_name, squad in operation_object.squads.items():
        if squad:
            embed = discord.Embed(title=f"Squad Leader: {squad.sl}", colour=squad_colour_dict[squad_name])
            embed.set_author(name=f"Squad: {squad_name}")
            embed.add_field(name=f"Fireteam Lead", value=squad.fl, inline=False)

            #We create a nice printable version of the composition summary as opposed to str(squad.composition)
            composition_summary = ""
            if squad.composition:
                for role, count in squad.composition.items():
                    composition_summary += f"{role}={int(count)}"
            else:
                composition_summary = "No Restrictions"

            embed.add_field(name="Composition", value=composition_summary, inline=False)

            '''
            To obtain a nice summary of each member and their role, we need to iterate through squad.members and the number of members with each role
            squad.members is a dict ({member, role}). We create role_dict to store these values
            '''

            role_dict = {}
            for planetman in squad.members:
                if role_dict.get(planetman.role) is None:
                    role_dict[planetman.role] = [(planetman.name, planetman.fisu)]
                else:
                    role_dict[planetman.role].append((planetman.name, planetman.fisu))

            '''
            We can now iterate through role_dict to create a nice summary of each member and their role
            '''

            for role, member in role_dict.items():
                member_string = ""
                for item in member:
                    name = item[0]
                    fisu_link = item[1]
                    member_string += f"[{name}]({fisu_link})\n"
                embed.add_field(name=role, value=member_string, inline=False)
        else:
            embed = None

        yield embed, squad_name

@client.command(pass_context=True)
async def debug(ctx, *args):

    '''
    Return debug information to the channel
    '''

    user = ctx.message.author
    channel_id = ctx.channel.id

    try:
        debug_message = f"{operation_dict[channel_id]}"
        await ctx.send(debug_message)

        debug_message = f"history_dict {history_dict[channel_id]}"
        await ctx.send(debug_message)

        debug_message = f"embed_dict {embed_dict[channel_id]}"
        await ctx.send(debug_message)
    except KeyError:
        pass

    debug_message = f"alias_dict {alias_dict}"
    await ctx.send(debug_message)

    await ctx.message.delete()

def update_history_dict(channel_id, message):

    if channel_id in history_dict:
        history_dict[channel_id].append(message)
    else:
        history_dict[channel_id] = [message]

client.run(TOKEN)

