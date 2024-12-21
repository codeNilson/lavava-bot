from discord.ext import commands


class LoginError(commands.CommandError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
