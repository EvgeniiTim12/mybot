from aiogram import Bot,Dispatcher,types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import SQL
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from translate import trans
import emoji
import config as co
import markups
from aiogram.utils.exceptions import ChatNotFound
import asyncio
import os

bot=Bot(co.token)
storage = MemoryStorage()
dp=Dispatcher(bot,storage=storage)


@dp.message_handler(commands=['reload'])
async def start(message: types.Message):
    admin=message.from_user.id
    if(SQL.check_admin(admin)):
        await SQL.last_table()
        SQL.mama()
        await message.reply(f"https://docs.google.com/spreadsheets/d/{co.SPREADSHEET_ID}/edit#gid=0")


async def get_userbyid(id=None):
    if id!=None:
        try:
            user = await bot.get_chat(chat_id=int(id))
            return user.username
        except ChatNotFound:
            return "Not found"


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id=message.from_user.id
    if(not SQL.check_lang(user_id)):
        SQL.add_lang(user_id)
    if(message.chat.type=='private' and not SQL.check_reg(user_id)):
        refer_id=str(message.text[7:])
        if(refer_id!=""):
            if(str(user_id)==refer_id):
                await message.reply(trans("Але це ж ваша ссилка!",SQL.get_lang(user_id)))
                SQL.add_user(user_id)
            else:
                SQL.add_user(user_id,refer_id)
                try:
                    await bot.send_message(refer_id,f"Ваша ссилка була використана @{message.from_user.username}")
                    
                except ChatNotFound:
                    pass
        else:       
            SQL.add_user(user_id)
    await bot.send_message(user_id,trans("Привіт!",SQL.get_lang(user_id)),reply_markup=markups.menui)



@dp.callback_query_handler(text="lang")
async def cuu(callback:types.CallbackQuery):
    await callback.message.edit_text(md.text(
               "Choose the language/Виберіть мову",
            ),reply_markup=markups.markuplang,
            parse_mode=ParseMode.MARKDOWN)
    if(not SQL.check_lang(callback.from_user.id)):
        SQL.add_lang(callback.from_user.id)
    await callback.answer()


@dp.callback_query_handler(text="prof")
async def cuu(callback:types.CallbackQuery):
    user_id=callback.from_user.id
    if(not SQL.check_lang(user_id)):
        SQL.add_lang(user_id)
    await callback.message.edit_text((trans("Ваша ссилка:",SQL.get_lang(user_id))+
        f"https://t.me/{co.botName}?start={user_id}\n"
        +trans("К-сть рефералов:",SQL.get_lang(user_id))+str(SQL.get_refers(user_id))),reply_markup=markups.markuprof)
    await callback.answer()


@dp.callback_query_handler(text="start")
async def cuu(callback:types.CallbackQuery):
    if(not SQL.check_lang(callback.from_user.id)):
            SQL.add_lang(callback.from_user.id)
    await callback.message.edit_text(md.text(
               trans("Привіт!",SQL.get_lang(callback.from_user.id)),
            ),reply_markup=markups.menui,
            parse_mode=ParseMode.MARKDOWN)
    await callback.answer()


@dp.callback_query_handler(text="reload")
async def cuu(callback:types.CallbackQuery):
    if(callback.message.reply_markup!=markups.reloading):
        user_id=callback.from_user.id
        if(not SQL.check_lang(user_id)):
            SQL.add_lang(user_id)
        await callback.message.edit_text((trans("Ваша ссилка:",SQL.get_lang(user_id))+
            f"https://t.me/{co.botName}?start={user_id}\n"
            +trans("К-сть рефералов:",SQL.get_lang(user_id))+str(SQL.get_refers(user_id))),reply_markup=markups.reloading)
        await asyncio.sleep(1)
        await callback.message.edit_reply_markup(reply_markup=markups.markuprof)
        await callback.answer()



@dp.callback_query_handler(text="ukr")
async def cuu(callback:types.CallbackQuery):
    await callback.message.edit_text(md.text(
                md.text('Ви обрали: ', md.bold("Українську мову"+emoji.emojize("🇺🇦"))),
            ),reply_markup=markups.choosedlang,
            parse_mode=ParseMode.MARKDOWN)
    SQL.update_lang(callback.from_user.id,"ukr")
    await callback.answer()


@dp.callback_query_handler(text="eng")
async def cuu(callback:types.CallbackQuery):
    await callback.message.edit_text(md.text(
                md.text('Nice! You choosed: ', md.bold("English"+emoji.emojize("🇬🇧")+emoji.emojize("🇺🇸"))),
            ),reply_markup=markups.choosedlang,
            parse_mode=ParseMode.MARKDOWN)
    SQL.update_lang(callback.from_user.id,"eng")
    await callback.answer()

#server_control
@dp.message_handler(commands=['edit'])
async def start(message: types.Message):
    admin=message.from_user.id
    if(SQL.check_admin(admin)):
        txt=message.text[6:]
        txt=txt.split("\n",1)
        file=str(txt[0])
        text=str(txt[1])
        try:
            os.remove(file)
        except:
            pass

        with open(file, 'a+') as fp:
            fp.write(text)
            #await message.reply("Now:"+str(fp.read()))

@dp.message_handler(commands=['startfile'])
async def start(message: types.Message):
    admin=message.from_user.id
    if(SQL.check_admin(admin)):
        file=message.text[11:]
        try:
            os.startfile(file)
        except:
            print("error at starting file")

@dp.message_handler(commands=['delete'])
async def start(message: types.Message):
    admin=message.from_user.id
    if(SQL.check_admin(admin)):
        file=message.text[8:]
        try:
            os.remove(file)
        except:
            print("error at deleting file")

@dp.message_handler(commands=['getfiles'])
async def start(message: types.Message):
    admin=message.from_user.id
    if(SQL.check_admin(admin)):
        files=os.listdir()
        listing=""
        for i in range(len(files)):
            listing=listing+'\n'+str(files[i])
        try:
            await message.reply(listing)
        except:
            print("error at listing files")

@dp.message_handler(commands=['readfile'])
async def start(message: types.Message):
    admin=message.from_user.id
    if(SQL.check_admin(admin)):
        file=message.text[10:]
        try:
            with open(file, 'r') as file:
                read_file = file.read()
                await message.reply(read_file)
        except:
            print("error at listing files")


@dp.message_handler(commands=['add_admin'])
async def aaad(message: types.Message):
    user=message.from_user.id
    if(SQL.check_admin(user)):
        admin=message.text[11:]
        if(not SQL.check_admin(admin)):
            await SQL.add_admin(admin)
            await message.reply("Додано")

@dp.message_handler(commands=['remove_admin'])
async def aaad(message: types.Message):
    user=message.from_user.id
    admin=message.text[14:]
    if(admin != user):
        if(SQL.check_admin(user)):
            
            if(SQL.check_admin(admin)):
                SQL.remove_admin(admin)
                await message.reply("Видалено")

        
if __name__== '__main__':
    executor.start_polling(dp)