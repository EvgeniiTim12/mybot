from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import emoji

empty=InlineKeyboardMarkup()

markuplang=InlineKeyboardMarkup()
button1=InlineKeyboardButton(text="English"+emoji.emojize("🇬🇧")+emoji.emojize("🇺🇸"),callback_data="eng")
button2=InlineKeyboardButton(text="Українська"+emoji.emojize("🇺🇦"),callback_data="ukr")
button3=InlineKeyboardButton(text="Back"+emoji.emojize("◀️"),callback_data="start")
markuplang.row(button1,button2)
markuplang.add(button3)


markuprof=InlineKeyboardMarkup()
button1=InlineKeyboardButton(text="Back"+emoji.emojize("◀️"),callback_data="start")
button3=InlineKeyboardButton(text="Reload"+emoji.emojize("🔁"),callback_data="reload")
button2=InlineKeyboardButton(text="Card"+emoji.emojize("💳"),callback_data="card")
markuprof.add(button3,button1)
markuprof.add(button2)

reloading=InlineKeyboardMarkup()
button1=InlineKeyboardButton(text="Loading...",callback_data="prof")
reloading.row(button3,button1)


choosedlang=InlineKeyboardMarkup()
button3=InlineKeyboardButton(text="Back"+emoji.emojize("◀️"),callback_data="start")
choosedlang.add(button3)

menui=InlineKeyboardMarkup()
button1=InlineKeyboardButton(text="Language/Мова"+emoji.emojize("🌐"),callback_data="lang")
button2=InlineKeyboardButton(text="Profile"+emoji.emojize("👤"),callback_data="prof")
menui.row(button1,button2)

servmenu=InlineKeyboardMarkup()
create=InlineKeyboardButton(text="create",callback_data="create")
edit=InlineKeyboardButton(text="edit",callback_data="edit")
delete=InlineKeyboardButton(text="delete",callback_data="delete")
servmenu.row(create,edit)
servmenu.add(delete)