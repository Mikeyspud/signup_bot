import discord
from modules import settings
from . import errors, handler

class Alias(handler.Handler):

    async def __call__(self):

        if len(self.args) < 2:
            await self.help()
            await self.error(InvalidArguments, "No Arguments supplied")

        if self.args[0] == "force":
            await self.alias_force()
        else:
            for alias in self.args[1:]:
                if alias in settings.alias_dict:
                    await self.help()
                    await self.error(AliasIsRole, f"Alias {alias} is already a role")

            for role, alias_set in settings.alias_dict.items():
                for alias in alias_set:
                    if alias in self.args[1:]:
                        await self.help()
                        await self.error(AliasIsAliasForOtherRole, f"Alias {alias} is already an alias for {role}")

            role = self.args[0]
            if role not in settings.alias_dict:
                settings.alias_dict[role] = set()

            settings.alias_dict[role].update(self.args[1:])

        settings.alias_collection.insert_one(parse_alias_dict(role=role))

    async def alias_force(self):

        for role, alias_set in settings.alias_dict.itemss():
            for alias in self.args[2:]:
                alias_set.discard(alias)

        role = self.args[1]
        settings.alias_dict[role] = set().update(self.args[2:])

    async def help(self):

        embed = settings.help_embed()
        embed.add_field(name="Command:", value="Allows a user to create an alias for a role", inline=False)
        embed.add_field(name=".alias [role] [alias]", value="Creates alias [alias] for [role]", inline=True)

        await self.user.send(embed=embed)


class InvalidArguments(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.alias.InvalidArguments", inline=False)

class AliasIsRole(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.alias.AliasIsRole", inline=False)


class AliasIsAliasForOtherRole(errors.Error):

    def __init__(self, ctx, error):

        super().__init__(self, ctx, error)
        self.embed.add_field(name="Exception", value="handlers.alias.AliasIsAliasForOtherRole", inline=False)
