from typing import Any

from httpx import AsyncClient, HTTPStatusError, RequestError, Response
from mcp.server import FastMCP

# Initialize the FastMCP server
mcp = FastMCP(name="pokemon")

# Pokemon API endpoint
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"


# Fetch data from the PokeAPI
async def fetch_pokemon_data(pokemon_name: str) -> dict:
    """Fetch data from the PokeAPI."""

    pokemon_name = pokemon_name.lower().strip()

    async with AsyncClient() as client:
        try:
            response: Response = await client.get(url=f"{POKEAPI_URL}{pokemon_name}")
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()

        except RequestError as exc:
            return {"error": f"Request Error: {exc.request.url!r}."}

        except HTTPStatusError as exc:
            return {
                "error": f"Response Error: {exc.response.status_code} while requesting {exc.request.url!r}."
            }

        except Exception as exc:
            return {"error": f"Exception Error: {exc}"}

    return {}


# Tool: Get information about a Pokemon
@mcp.tool()
async def get_pokemon_info(pokemon_name: str) -> str:
    """
    Get information about a specific Pokemon, including its ID, types, abilities, height, weight, and base stats.
    Args:
        pokemon_name (str): The name of the Pokemon to look up (e.g., 'pikachu', 'charizard').
    Returns:
        str: A formatted string containing the Pokemon's information, or an error message if not found or an error occurs.
    """
    data: dict[Any, Any] = await fetch_pokemon_data(pokemon_name=pokemon_name)

    if "error" in data:
        return data["error"]

    try:
        # Extract relevant information
        name: Any = data.get("name", "N/A").capitalize()
        pokemon_id: Any = data.get("id", "N/A")
        height: Any = data.get("height", "N/A")
        weight: Any = data.get("weight", "N/A")

        # Extract stats, types, and abilities
        stats: dict[Any, Any] = {
            stats["stat"]["name"]: stats["base_stat"] for stats in data["stats"]
        }
        types: list[Any] = [types["type"]["name"] for types in data["types"]]
        abilities: list[Any] = [
            abilities["ability"]["name"] for abilities in data["abilities"]
        ]

    except Exception as exc:
        return f"Pokemon data processing Error: {exc}"

    # Format the information into a readable string
    return f"""
    Name: {name}
    ID: {pokemon_id}
    Height: {height} decimeters
    Weight: {weight} hectograms
    Types: {", ".join(types) if types else "N/A"}
    Abilities: {", ".join(abilities) if abilities else "N/A"}
    Base Stats: {", ".join(f"{k}: {v}" for k, v in stats.items())}
    """


# Tool: Create a tournament squad
@mcp.tool()
async def create_tournament_squad() -> str:
    """
    Create a tournament squad with the specified Pokemon names.
    Args:
        pokemon_names (str): Comma-separated list of Pokemon names (e.g., 'pikachu, charizard, bulbasaur').
    Returns:
        str: A formatted string listing the Pokemon in the tournament squad.
    """
    top_pokemon: list[str] = [
        "charizard",
        "garchomp",
        "lucario",
        "dragonite",
        "metagross",
        "gardevoir",
        "tyranitar",
        "entei",
        "suicune",
        "raikou",
    ]

    squd: list[str] = []

    for pokemon in top_pokemon:
        data: dict[Any, Any] = await fetch_pokemon_data(pokemon_name=pokemon)
        if "error" in data:
            return data["error"]
        squd.append(data["name"].capitalize())

    return f"Your tournament squad: \n\n {', '.join(squd)}"


# Tool: List popular Pokemon
@mcp.tool()
async def list_popular_pokemon() -> str:
    """
    List the top 10 most popular Pokemon based on their usage in tournaments.
    Returns:
        str: A formatted string listing the top 10 popular Pokemon.
    """
    top_pokemon: list[str] = [
        "charizard",
        "garchomp",
        "lucario",
        "dragonite",
        "metagross",
        "gardevoir",
        "tyranitar",
        "entei",
        "suicune",
        "raikou",
    ]

    return f"Top 10 popular Pokemon: \n\n {', '.join(top_pokemon)}"


# Entry point for the FastMCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
