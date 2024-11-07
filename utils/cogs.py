import inspect
from core import cogs

cogs = [cog for cog_name, cog in inspect.getmembers(cogs, inspect.isclass)]


async def add_cogs(bot):
    for cog in cogs:
        try:
            await bot.add_cog(cog(bot))
            print(f"Loaded {cog.__name__}")
        except Exception as e:
            print(f"Error loading {cog.__name__}: {e}")
