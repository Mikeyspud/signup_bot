import discord
from . import settings


def update_history_dict(channel_id, message):

    if channel_id in settings.history_dict:
        settings.history_dict[channel_id].append(message)
    else:
        settings.history_dict[channel_id] = [message]


async def update_operation_summary(ctx):

    channel_id = ctx.channel.id
    operation = settings.operation_dict[channel_id]

    async for embed, squad in generate_embed(operation):
        if settings.embed_dict[channel_id][squad] and embed:
            embed_id = settings.embed_dict[channel_id][squad]
            embed_message = await ctx.channel.fetch_message(embed_id)
            await embed_message.edit(embed=embed)
        elif embed:
            embed_message = await ctx.send(embed=embed)
            settings.embed_dict[channel_id][squad] = embed_message.id
        else:
            settings.embed_dict[channel_id][squad] = embed


async def generate_embed(operation_object):

    '''
    Generator that yields a discord.Embed object and the appropriate squad_name.
    First we need to create the embed for the operation and then yield it under the squad_name "op"
    '''
    embed = discord.Embed(
        title=f"Operation {operation_object.name} Created",
        colour=discord.Colour.green())
    embed.set_author(name="SUCCESS!")
    embed.add_field(
        name="Start Time (CEST)",
        value=operation_object.start,
        inline=True)
    embed.add_field(
        name="End Time (CEST)",
        value=operation_object.end,
        inline=True)
    embed.add_field(
        name="To signup to the op",
        value=".add [squad] [class]",
        inline=False)
    embed.add_field(name="To remove yourself from the op",
                    value=".remove [squad]", inline=False)

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
            embed = discord.Embed(
                title=f"Squad Leader: {squad.sl}",
                colour=squad_colour_dict[squad_name])
            embed.set_author(name=f"Squad: {squad_name}")
            embed.add_field(
                name=f"Fireteam Lead",
                value=squad.fl,
                inline=False)

            # We create a nice printable version of the composition summary as
            # opposed to str(squad.composition)
            composition_summary = ""
            if squad.composition:
                for role, count in squad.composition.items():
                    composition_summary += f"{role}={int(count)}  "
            else:
                composition_summary = "No Restrictions"

            embed.add_field(
                name="Composition",
                value=composition_summary,
                inline=False)

            '''
            To obtain a nice summary of each member and their role, we need to iterate through squad.members and the number of members with each role
            squad.members is a dict ({member, role}). We create role_dict to store these values
            '''

            role_dict = {}
            for planetman in squad.members:
                if role_dict.get(planetman.role) is None:
                    role_dict[planetman.role] = [
                        (planetman.name, planetman.fisu)]
                else:
                    role_dict[planetman.role].append(
                        (planetman.name, planetman.fisu))

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


def parse_alias_dict(role=None):
    '''
    pymongo does not contain a codec for python set objects. So we need
    to parse the alias_dict into a form where the values are lists and
    not sets
    '''

    parsed_alias_dict = {}

    if role:
        parsed_alias_dict[role] = list(settings.alias_dict[role])
    else:
        for role in settings.alias_dict:
            parsed_alias_dict[role] = list(settings.alias_dict[role])

    return parsed_alias_dict


def update_alias_dict():

    query = settings.alias_collection.find({}, {'_id': False})
    for document in query:
        for role in document:
            document[role] = set(document[role])
        alias_dict.update(document)
