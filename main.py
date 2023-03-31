import logging
from aiogram import Bot, Dispatcher, executor, types

from api_token import API_TOKEN
from constants import START_COMMAND, BUYRUQLAR
import functions as func
from datas import data_ot_soz_turkumi, count

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(START_COMMAND)

@dp.message_handler(commands=["test"])
async def test(message: types.Message):
    await message.answer_photo("rasm.PNG")

@dp.message_handler(commands=["topilmaganlar"])
async def check_count(message: types.Message):
    with open("topilmaganlar.txt") as file:
        s = file.read()
    if s == "":
        res = "Topilmagan so'zlar yo'q."
    else:
        res = s
    await message.answer(res)

@dp.message_handler(commands=["topilmaganlarniYangilash"])
async def top_yangi(message: types.Message):
    ot_soz_turkumi = set()
    for i in data_ot_soz_turkumi:
        for j in i["ozbekcha-bosh-birlik"]:
            ot_soz_turkumi.add(j)
    with open("topilmaganlar.txt") as file:
        data = file.read()
    top_dagi_otlar_toplami = set(data.split("\n"))
    top_dagi_otlar_toplami -= ot_soz_turkumi
    with open("topilmaganlar.txt", "w") as file:
        s = ""
        for i in top_dagi_otlar_toplami:
            s += f"{i}\n"
        file.write(s[:-1])
    await message.answer("Topilmaganlar to'plami yangilandi.")
    
@dp.message_handler(commands=["buyruqlar"])
async def buyruqlar(message: types.Message):
    await message.answer(BUYRUQLAR, parse_mode="HTML")

@dp.message_handler(commands=["topilmaganlardanOchirish"])
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

@dp.message_handler(commands=['elementQoshish'])
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
        with open("topilmaganlar.txt", "a") as file:
            file.write(f'{s}\n')
        await message.answer("Natija topilmadi!")
    else:
        await message.answer(func.f(x))

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)