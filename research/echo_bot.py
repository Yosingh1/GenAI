from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import os
import logging
import sys
import asyncio
from langchain import HuggingFaceHub
from aiogram.types import Message
from aiogram import executor

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

#iniate LLM here

llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs = {"temperature":0.5},)
#print(llm.invoke("how are you?"))

#configure logging

logging.basicConfig(level=logging.INFO)

# #Initialize bot 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# print(dp,"working")


class Reference:
    def __init__(self) -> None:
        self.response = ""

reference = Reference()

def clear_past():
    reference.response = ""

@dp.message_handler(commands=["clear"])
async def clear(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")


@dp.message_handler(commands=["start"])
async def command_start_handler(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi!\n I am an Echo Bot!\n Created by Yogendra Pratap Singh\n How May I help you?")


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    print(types.Message)
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    
    await message.reply("Hi\nI am a Chat Bot! Created by Yogendra. How can i assist you?")

@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dp.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")
    if message.text=="hi" or message.text =="Hi" or message.text=="hello" or message.text=="Hello" or message.text=="Hi there":
        await message.reply("Hi\nI am a Chat Bot! Created by Yogendra. How can i assist you?") 
    else:  
        response=llm.invoke(message.text)
        print(f">>> chatGPT: \n\t{response}")
        await bot.send_message(chat_id = message.chat.id, text = response)

# @dp.message_handler()
# async def echo(message: types.Message):
#     """This will return echo message

#     Args:
#         message (types.Message): _description_
#     """

#     await message.reply(message.text)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    