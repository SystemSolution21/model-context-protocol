"""
This is a Gradio web interface for an Airbnb search agent using AI."""

from praisonaiagents import Agent, MCP
import gradio as gr

# Set llm model
llm_model: str = "ollama/llama3.2:3b"


# Create an agent
def search_airbnb(query: str):
    """Search Airbnb for apartments."""

    agent = Agent(
        instructions="""You help book apartments on Airbnb.""",
        llm=llm_model,
        tools=[
            MCP(
                command_or_string="npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"
            )
        ],
    )

    result = agent.start(prompt=query)
    return f"## Airbnb Search Result: {result}"


demo = gr.Interface(
    fn=search_airbnb,
    inputs=gr.Textbox(
        placeholder="I want to book an apartment in New York City for 2 nights...."
    ),
    outputs=gr.Markdown(),
    title="Airbnb Search Agent",
    description="Enter your booking requirements below:",
)

if __name__ == "__main__":
    demo.launch()
