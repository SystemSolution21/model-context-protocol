from typing import Any
import pytest
from httpx import Response, AsyncClient
import json
from pokemon import (
    fetch_pokemon_data,
    get_pokemon_info,
    create_tournament_squad,
    list_popular_pokemon,
)
from pathlib import Path


# Get the current file path
current_dir: Path = Path(__file__).parent
print(f"Current directory: {current_dir}")
file_path: Path = current_dir / "example-pokemon-api-response.json"

# Do mock response file exists
if not file_path.exists():
    pytest.skip(
        reason="Mock response file not found, skipping tests", allow_module_level=True
    )

# Mock response data
with open(file=file_path, mode="r") as f:
    MOCK_POKEMON_DATA: Any = json.load(fp=f)


@pytest.mark.asyncio
async def test_fetch_pokemon_data_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(*args, **kwargs) -> Response:
        response = Response(
            status_code=200,
            json=MOCK_POKEMON_DATA,
            request=None,  # This prevents raise_for_status from failing
        )
        # Mock the raise_for_status method to do nothing
        response.raise_for_status = lambda: response
        return response

    monkeypatch.setattr(target=AsyncClient, name="get", value=mock_get)

    result = await fetch_pokemon_data("bulbasaur")
    assert (
        result == MOCK_POKEMON_DATA
    )  # The response should match our mock data exactly


@pytest.mark.asyncio
async def test_get_pokemon_info_success(monkeypatch):
    mock_data = {
        **MOCK_POKEMON_DATA,
        "id": 1,
        "height": 7,
        "weight": 69,
        "stats": [
            {"stat": {"name": "hp"}, "base_stat": 45},
            {"stat": {"name": "attack"}, "base_stat": 49},
        ],
    }

    async def mock_fetch(*args, **kwargs):
        return mock_data

    monkeypatch.setattr("pokemon.fetch_pokemon_data", mock_fetch)

    result = await get_pokemon_info("bulbasaur")
    assert "Name: Bulbasaur" in result
    assert "Types: grass, poison" in result
    assert "Abilities: overgrow, chlorophyll" in result


@pytest.mark.asyncio
async def test_create_tournament_squad(monkeypatch):
    async def mock_fetch(*args, **kwargs):
        pokemon_name = kwargs.get("pokemon_name")
        return {"name": pokemon_name}  # Use kwargs instead of args

    monkeypatch.setattr("pokemon.fetch_pokemon_data", mock_fetch)

    result = await create_tournament_squad()
    assert "Charizard" in result
    assert "Garchomp" in result
    assert len(result.split(",")) == 10


@pytest.mark.asyncio
async def test_list_popular_pokemon():
    result = await list_popular_pokemon()
    assert "charizard" in result.lower()
    assert "garchomp" in result.lower()
    assert len(result.split(",")) == 10


@pytest.mark.asyncio
async def test_fetch_pokemon_data_error(monkeypatch):
    async def mock_get(*args, **kwargs):
        raise Exception("API Error")

    monkeypatch.setattr(AsyncClient, "get", mock_get)

    result = await fetch_pokemon_data("bulbasaur")
    assert "error" in result
    assert "Exception Error" in result["error"]
