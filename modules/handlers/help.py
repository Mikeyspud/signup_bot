from .. import settings                     # Global Variables
import discord                      # Discord API

from . import handler, show, create, close


class Help(handler.Handler):

    '''
    This command sends a help embed to the user

    Example:
        .help
        .help adv
    '''

    def __init__(self, ctx, *args):

        handler.Handler.__init__(self, ctx, args)
        self.help_dict = {"show": show.Show(ctx, "help"),
                          "create": create.Create(ctx, "help"),
                          "close": close.Close(ctx, "help")}

    async def __call__(self):

        if len(self.args) < 1:
            sub_commands = self.help_dict.keys()
        else:
            sub_commands = self.args

        for sub_command in sub_commands:
            await self.help_dict[sub_command]()
