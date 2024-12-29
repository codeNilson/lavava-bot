from api.api_client import api_client


async def get_map(map_name: str):
    """Get map by name"""
    map_model = await api_client.get_maps(map_name)
    return map_model
