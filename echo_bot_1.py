from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '5621624079:AAGxRyIBTKuj5ziba1NKX7Os1yUnZSOyJGs'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[0].file_id)

async def send_sticker_echo(message: Message):
    await message.reply_sticker(message.sticker.file_id)

async def send_audio_echo(message: Message):
    await message.reply_sticker(message.audio.file_id)

async def send_video_echo(message: Message):
    await message.reply_sticker(message.video.file_id)

async def send_voice_echo(message: Message):
    await message.reply_sticker(message.voice.file_id)

async def send_animation_echo(message: Message):
    await message.reply_sticker(message.animation.file_id)

async def send_video_note_echo(message: Message):
    await message.reply_sticker(message.video_note.file_id)

async def send_echo(message: Message):
    await message.reply(text=message.text)

dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_sticker_echo, F.sticker)
dp.message.register(send_audio_echo, F.audio)
dp.message.register(send_video_echo, F.video)
dp.message.register(send_voice_echo, F.voice)
dp.message.register(send_animation_echo, F.animation)
dp.message.register(send_video_note_echo, F.video_note)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)