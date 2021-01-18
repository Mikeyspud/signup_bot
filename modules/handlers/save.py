import discord
from modules import settings
from . import errors, handler


class Save(handler.Handler):

    async def __call__(self):

        try:
            template_name = args[0]
        except IndexError:
            await self.help()
            await self.error(InvalidArguments, "Invalid Arguments")

        try:
            template = {template_name: history_dict[channel_id]}
        except KeyError:
            await self.help()
            await self.error(NoOperation, "No operation exists")

        if len(template[template_name]) < 1:
            await self.help()
            await self.error(EmptyTemplate, "Template is empty")

        count = op_collection.count_documents(
            {template_name: {'$exists': True}})
        if count == 0:
            op_collection.insert_one(template)
        else:
            op_collection.find_one_and_update({template_name: {'$exists': True}}, {
                                              '$set': {template_name: template[template_name]}})

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(
            name="Command:",
            value="Allows a user to save command history")
        embed.add_field(
            name=".save [template_name]",
            value="Saves command history by name [template_name]")

        await self.user.send(embed=embed)


class NoOperation(errors.Error):

    pass


class InvalidArguments(errors.Error):

    pass
