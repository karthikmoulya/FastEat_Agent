from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from prompt import SYSTEM_CHEF_PROMPT, CHEF_PROMPT
from tools import web_search
from photo_decoder import choose_image_file, build_image_message
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

load_dotenv()

logging.info("creating our agent...")
agent = create_agent(model="claude-haiku-4-5-20251001",
                     tools=[web_search],
                     system_prompt=SYSTEM_CHEF_PROMPT)

logging.info("choosing our image...")
path = choose_image_file()
message = build_image_message(path, CHEF_PROMPT)

logging.info("invoking our agent...")
response = agent.invoke(
    {"messages": [message]}
)

print(response["messages"][-1].content)