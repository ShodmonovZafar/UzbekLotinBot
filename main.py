import logging
import functions as func
from message_constants import START_COMMAND
from aiogram import Bot, Dispatcher, executor, types
from constants import API_TOKEN

data_ot_soz_turkumi = []

with open("ot.txt") as file:
    ot_str = file.read()

bitta_element = ot_str.split("\n")

for i in bitta_element:
    data_ot_soz_turkumi.append(func.g(i))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

with open("top.txt") as file:
    top_str = file.read()

count = func.f1(top_str)

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
        qosh = []
        for i in m["ozbekcha-bosh-birlik"]:
            qosh.append(f'"{i}"')
        qoshiladigan_str = '("{1}", "{2}", "{3}"){0}'.format(qosh,
                                     m["lotincha-bosh-birlik"],
                                     m["lotincha-qaratqich-birlik-qoshimcha"],
                                     m["rod"])
        with open("ot.txt", "a") as file:
            file.write(f"\n{qoshiladigan_str}")
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
        with open("top.txt", "a") as file:
            file.write(f'\n"{s}"')
        await message.answer("Natija topilmadi!")
    else:
        await message.answer(func.f(x))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)