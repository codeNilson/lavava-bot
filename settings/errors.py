from discord import app_commands


class LoginError(app_commands.AppCommandError):
    pass


class MissingPlayersException(app_commands.AppCommandError):
    pass
