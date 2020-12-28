import discord

class Error(Exception):
    pass

class EmptyTemplate(Error):
    pass

class NoOperationExists(Error):
    pass

class OperationExists(Error):
    pass

class InvalidArguments(Error):
    pass

class InvalidSquad(Error):
    pass

def debug_message(error_class, message, channel_id):

    debug_class_dict = {"information": discord.Colour.from_rgb(r=255, g=255, b=255),
                        "warning": discord.Colour.from_rgb(r=255, g=255, b=0),
                        "error": discord.Colour.from_rgb(r=255, g=0, b=0)}

    embed = discord.Embed(title=error_class, colour=debug_class_dict[error_class])
    embed.set_author(name=channel_id)
    embed.add_field(name="message", value=message)

    return embed
