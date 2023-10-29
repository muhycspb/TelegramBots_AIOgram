from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from random import randint

f = open('token.txt')
BOT_TOKEN = f.readline()
f.close()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

attempts = 5

users = {}


def get_random_int() -> int:
    return randint(1, 100)


@dp.message(Command(commands='start'))
async def start(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': attempts,
                                       'total_games': 0,
                                       'wins': 0}


@dp.message(Command(commands='help'))
async def help(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, а вам нужно его угадать\n'
        f'У вас есть {attempts} попыток\n\nДоступные команды:\n'
        f'/help - правила игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


@dp.message(Command(commands='stat'))
async def stat(message: Message):
    await message.answer(
        f'Сыграно игр: {users[message.from_user.id]["total_games"]}\nПобед: {users[message.from_user.id]["wins"]}'
    )


@dp.message(Command(commands='cancel'))
async def cancel(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы итак с вами не играем. Может, сыграем разок?'
        )


@dp.message(F.text.lower().in_(['ок', 'да', 'давай', 'конечно']))
async def positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_int()
        users[message.from_user.id]['attempts'] = attempts
        await message.answer(
            'Я загадал число от 1 до 100, попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу']))
async def negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def num_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')
        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
