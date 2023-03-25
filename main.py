import logging
import functions as func
from message_constants import START_COMMAND
from datas import data_ot_soz_turkumi

from aiogram import Bot, Dispatcher, executor, types

from constants import API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(START_COMMAND)

@dp.message_handler(commands=['topilmaganlar'], commands_prefix="+")
async def f(message: types.Message):
    with open("topilmagan_sozlar.txt") as file:
        data_str = file.read()
    await message.answer(data_str)


@dp.message_handler()
async def echo(message: types.Message):
    try:
        s = message.text.lower()
        s = func.tutuq_belgisi(s)
        x = func.ot(data_ot_soz_turkumi, s)
    except:
        await message.answer("Dasturda xatolik yuz berdi! \n Iltimos! Boshqatdan urinib ko'ring. ")
    if type(x) == int:
        with open("topilmagan_sozlar.txt", "a") as file:
            s1 = "{} ".format(s)
            try:
                file.write(s1)
            except:
                await message.answer("Xatolik! Iltimos, lotin alifbosida o'zbekcha so'z kiriting!")

        await message.answer("Natija topilmadi!")
    else:
        await message.answer(func.f(x))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)