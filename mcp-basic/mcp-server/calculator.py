"""Calculator MCP server."""

# calculator.py
import signal
import sys
from mcp.server import FastMCP

mcp = FastMCP(name="calculator")


@mcp.tool()
async def calculator(
    operation: str, a: int | float, b: int | float
) -> int | float | str:
    """Perform basic arithmetic operations."""
    operation = operation.lower()
    match operation:
        case "add":
            return a + b
        case "subtract":
            return a - b
        case "multiply":
            return a * b
        case "divide":
            if b == 0:
                return "Cannot divide by zero!"

            return (a / b).__format__(".2f")
        case _:
            return "Invalid operation"


@mcp.resource(uri="calculator://greetings")
async def get_greetings() -> str:
    return "Welcome to mcp server calculator!"


if __name__ == "__main__":
    mcp.run(transport="stdio")
