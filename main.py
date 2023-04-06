from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.force_reply import ForceReply
import ast
from algorithms.groupers import group_by
from db import get_db
import datetime
import json

bot = Bot(token="token")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_id = message.from_id
    result_message = f'Hi [{user_name} {user_last_name}](tg://user?id={str(user_id)})!'
    await message.answer(result_message, parse_mode="Markdown", reply_markup=ForceReply().create())


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    try:
        data = ast.literal_eval(message.text)
        result = await group_by(data.get('group_type'), datetime.datetime.strptime(data.get('dt_from'), "%Y-%m-%dT%H:%M:%S"), datetime.datetime.strptime(data.get('dt_upto'), "%Y-%m-%dT%H:%M:%S"), get_db())
        await message.answer(json.dumps(result))
    except ValueError:
        await message.answer('Невалидный запос. Пример запроса:"\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": '
                             '"2022-12-31T23:59:00", "group_type": "month"}')


if __name__ == '__main__':
    executor.start_polling(dp)
