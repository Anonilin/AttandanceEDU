import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# GRADES, STUDENTS

cfg = open('config.json', 'r', encoding="utf-8").read()
cfg = json.loads(cfg)

bot = Bot(cfg["TOKEN"])
dp = Dispatcher()

def log_write(text:str) -> None:
    global file
    file.write(text)

def ObjectList(dict_:str) -> list:
    more_list = []
    buttons = [[KeyboardButton(text=x) for x in cfg[dict_]]]
    if(len(buttons[0]) > 3):
        for i in range(0, len(buttons[0])-1, 3):
            more_list.append(buttons[0][i:i+3])
        return more_list
    else:
        return buttons

def list_normalize(text:dict) -> str:
    data = text[0] + '\n' + ''.join([text[x] for x in range(1, len(text))])
    return data

@dp.message()
async def message_handler(message: types.Message):
    if(message.from_user.id == 1286590612 or message.from_user.id == 1359044507):
        global file
        if(message.text.lower() == "/start"):
            markup = ReplyKeyboardMarkup(keyboard=ObjectList("GRADES"), one_time_keyboard=True)
            file = open('log.txt', 'w', encoding='utf-8')
            await message.answer("Выберите дисциплину.", reply_markup=markup)
        if(message.text in cfg["GRADES"]):
            markup = ReplyKeyboardMarkup(keyboard=ObjectList("STUDENTS"))
            log_write(message.text+'\n')
            await message.answer("Присутствующие студенты:", reply_markup=markup)
        if(message.text in cfg["STUDENTS"]):
            log_write(message.text+'\n')
            await message.answer("Зафиксированно 📝")
        if(message.text.lower() == "/stop"):
            file.close()
            file_r = open('log.txt', 'r', encoding='utf-8')
            text = file_r.readlines()
            file_r.close()
            await message.answer(f'Присутствующие:\n{list_normalize(text)}')

async def start():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())