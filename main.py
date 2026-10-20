import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from prompt import SYSTEM_CHEF_PROMPT, CHEF_PROMPT
from tools import web_search
from photo_decoder import choose_image_file, build_image_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

load_dotenv()


def ask(agent, message, config) -> None:
    response = agent.invoke({"messages": [message]}, config)
    print(f"\n{response['messages'][-1].text}\n")


def main() -> None:
    logging.info("creating our agent...")
    agent = create_agent(model="claude-haiku-5-5",
                         tools=[web_search],
                         system_prompt=SYSTEM_CHEF_PROMPT,
                         checkpointer=InMemorySaver())
    # the checkpointer remembers the conversation for this thread, so follow-ups have context
    config = {"configurable": {"thread_id": "kitchen"}}

    logging.info("choosing our image...")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else choose_image_file()
    message = build_image_message(path, CHEF_PROMPT)

    logging.info("invoking our agent...")
    ask(agent, message, config)

    print("Ask a follow-up (e.g. 'make it vegetarian'), or press Enter to quit.")
    while True:
        try:
            question = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question or question.lower() in {"q", "quit", "exit"}:
            break
        ask(agent, HumanMessage(question), config)


if __name__ == "__main__":
    main()
