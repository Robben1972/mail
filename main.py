import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from db import engine, Base, UserForm
from sqlalchemy import select
from sqlalchemy.orm import Session
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

msg = MIMEMultipart()


def send(to, body):
    msg['Subject'] = 'Test'
    msg['From'] = 'bozorovshahob27@gmail.com'
    msg['To'] = to
    msg.attach(MIMEText(body, 'html'))
    if to.endswith('gmail.com'):
        with SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('bozorovshahob27@gmail.com', 'dapqtmlkkjfgljnb')
            smtp.sendmail('bozorovshahob27@gmail.com', to, msg.as_string())


TOKEN = "6705025528:AAE8NsAZ2LpGB1piK7BZDx5Qbe0Lgl4IaiI"

dp = Dispatcher()


class ApplicationForm(StatesGroup):
    name = State()
    email = State()
    password = State()


class EmailSending(StatesGroup):
    add = State()
    texta = State()


class SearchState(StatesGroup):
    search = State()


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b'


def check(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    await message.answer("Please enter your email")
    await state.update_data(name=message.from_user.full_name)
    await state.set_state(ApplicationForm.email)


@dp.message(Command('give'))
async def search_by_name(message: Message, state: FSMContext) -> None:
    keyboard1 = ReplyKeyboardBuilder()
    with Session(engine) as session:
        users = select(UserForm)
        results = session.scalars(users).all()
        for result in results:
            keyboard1.row(KeyboardButton(text=result.name + "  " + result.email))
    await state.set_state(EmailSending.add)
    await message.answer('Take them ->', reply_markup=keyboard1.as_markup(input_field_placeholder='Take them'))


@dp.message(F.content_type == ContentType.TEXT, EmailSending.add)
async def message_text(message: Message, state: FSMContext):
    ok = False
    with Session(engine) as session:
        users = select(UserForm)
        results = session.scalars(users).all()
        for result in results:
            if result.name + "  " + result.email == message.text:
                ok = True
                await state.update_data(add=result.email)
                break
        if ok:
            await message.answer("What you want to write: ")
            await state.set_state(EmailSending.texta)
        else:
            await message.answer('We can\'t find you')


@dp.message(F.content_type == ContentType.TEXT, EmailSending.texta)
async def send_it(message: Message, state: FSMContext):
    data = await state.get_data()
    send(data.get('add'), message.text)
    await message.answer("Sent successfully")


@dp.message(F.content_type == ContentType.TEXT, ApplicationForm.email)
async def set_gmail(message: Message, state: FSMContext):
    if check(message.text):
        await message.answer("Now enter your password for sending email")
        await state.update_data(email=message.text)
        await state.set_state(ApplicationForm.password)
    else:
        await message.answer('Please enter correct email')


@dp.message(F.content_type == ContentType.TEXT, ApplicationForm.password)
async def set_name(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    data = await state.get_data()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    await message.answer(f'{name}-{email}-{password}!')

    with Session(engine) as session:
        user = UserForm(name=name, email=email, password=password)
        session.add(user)
        session.commit()

        await message.answer(f'{user.id}-{user.name} sizni malumotlaringiz saqlandi')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    Base.metadata.create_all(engine)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
