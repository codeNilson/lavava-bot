from discord.ext import commands


class LoginError(commands.CommandError):
    pass


class MissingPlayersException(commands.CommandError):
    pass
