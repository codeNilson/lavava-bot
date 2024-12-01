from pathlib import Path
import importlib
import inspect
from discord.ext import commands
import settings


async def add_cogs(bot):
    COGS_PATH = Path(settings.COGS_PATH)

    for filepath in COGS_PATH.glob("*.py"):
        module_name = f"{settings.COGS_PATH.replace('/', '.')}.{filepath.stem}"

        try:
            module = importlib.import_module(module_name)

            cogs = [
                cog
                for _, cog in inspect.getmembers(module, inspect.isclass)
                if issubclass(cog, commands.Cog)
            ]

            for cog in cogs:
                await bot.add_cog(cog(bot))
                print(f"Loaded module {module_name}")

        except Exception as e:
            settings.LOGGER.warning("Failed to load module %s: %s", module_name, e)
            print(f"Failed to load module {module_name}: {e}")
            continue
