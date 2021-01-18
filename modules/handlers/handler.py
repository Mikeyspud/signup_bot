from .. import settings

class Handler():

    def __init__(self, ctx, *args):

        self.ctx = ctx
        self.args = args
        self.user = ctx.message.author
        self.channel_id = ctx.channel.id
        self.operation = settings.operation_dict.get(self.channel_id)

    async def error(self, error, error_message):

        error_handler = error(self.ctx, error_message)
        await error_handler.debug()
        raise error_handler
