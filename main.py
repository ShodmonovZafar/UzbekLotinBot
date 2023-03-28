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

count = set()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(START_COMMAND)

@dp.message_handler(commands=["top"])
async def check_count(message: types.Message):
    global count
    if count:
        re_str = ""
        for i in count:
            re_str += f"{i}\n"
    else:
        re_str = "Topilmagan so'zlar yo'q."
    
    await message.answer(re_str)

@dp.message_handler(commands=["top_ochir"])
async def top_ochir(message: types.Message):
    global count
    try:
        s = func.tutuq_belgisi(message.text[11:].lower())
    except:
        await message.answer("Dasturda xatolik yuz berdi! \n Iltimos! Boshqatdan urinib ko'ring. ")
    if s in count:
        count.remove(s)
        await message.answer(f"{s} so'zi topilmaganlardan o'chirildi.")
    else:
        await message.answer(f"{s} so'zi topilmaganlar ichida yo'q.")

@dp.message_handler(commands=['ot'])
async def f(message: types.Message):
    try:
        s = func.tutuq_belgisi(message.text[4:].lower())
    except:
        await message.answer("Dasturda xatolik yuz berdi! \n Iltimos! Boshqatdan urinib ko'ring. ")
    m = func.g(s)
    if m in data_ot_soz_turkumi:
        await message.answer("Bu so'z bor.")
    else:
        data_ot_soz_turkumi.append(m)
        for i in m["ozbekcha-bosh-birlik"]:
            if i in count:
                count.remove(i)
            else:
                pass
        await message.answer("Bu so'z qo'shildi, hamda topilmaganlardan o'chirildi.")


@dp.message_handler()
async def echo(message: types.Message):
    global count
    try:
        s = message.text.lower()
        s = func.tutuq_belgisi(s)
        x = func.ot(data_ot_soz_turkumi, s)
    except:
        await message.answer("Dasturda xatolik yuz berdi! \n Iltimos! Boshqatdan urinib ko'ring. ")
    if type(x) == int:
        count.add(s)
        await message.answer("Natija topilmadi!")
    else:
        await message.answer(func.f(x))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)