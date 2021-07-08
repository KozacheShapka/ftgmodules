#clown... again :/ by @Sekai_Yoneya

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


def register(cb):
 cb(leomatchMod())


class leomatchMod(loader.Module):
 """Леонардо Дайвинчик"""

 strings = {'name': 'Leo'}

 def init(self):
  self.name = self.strings['name']
  self._me = None
  self._ratelimit = []

 async def client_ready(self, client, db):
  self._db = db
  self._client = client
  self.me = await client.get_me()

 async def dizcmd(self, event):
         """Дизлайкнуть пользователь."""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@leomatchbot'
         await event.edit('<b>[👎] Вам не понравился пользователь.</b>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users= 1234060895))
                 await event.client.send_message(chat, '👎')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @leomatchbot</code>')
                 return
             await event.delete()
             yoneya = response.text
             await event.client.send_file(event.to_id, response.media, caption=yoneya)
    
 async def likecmd(self, event):
         """Лайкнуть пользователь."""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@leomatchbot'
         await event.edit('<b>[❤️] Вам понравился пользователь.</b>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users= 1234060895))
                 await event.client.send_message(chat, '❤️')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @leomatchbot</code>')
                 return
             await event.delete()
             yoneya = response.text
             await event.client.send_file(event.to_id, response.media, caption=yoneya)

 async def spackcmd(self, event):
         """Не нужен мне ваш стикерпак."""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@leomatchbot'
         await event.edit('<b>[❌] В другой раз.</b>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users= 1234060895))
                 await event.client.send_message(chat, '❌ В другой раз')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @leomatchbot</code>')
                 return
             await event.delete()
             yoneya = response.text
             await event.client.send_file(event.to_id, response.media, caption=yoneya)
             
 async def ttcmd(self, event):
         """Не нужен мне ваш тик ток."""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@leomatchbot'
         await event.edit('<b>[❌] В другой раз.</b>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users= 1234060895))
                 await event.client.send_message(chat, 'Смотреть анкеты')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @leomatchbot</code>')
                 return
             await event.delete()
             yoneya = response.text
             await event.client.send_file(event.to_id, response.media, caption=yoneya)
             
 async def unafkcmd(self, event):
         """Выйти из АФК и смотреть анкеты."""
         user_msg = """{}""".format(utils.get_args_raw(event))
         global text
         text = False
         if event.fwd_from:
             return
             self_mess = True
             if not user_msg:
                 return 
         chat = '@leomatchbot'
         await event.edit('<b>[🚀] Смотрим анкеты.</b>')
         async with event.client.conversation(chat) as conv:
             try:
                 response = conv.wait_event(events.NewMessage(incoming=True,
                                                              from_users= 1234060895))
                 await event.client.send_message(chat, '1 🚀')
                 response = await response
             except YouBlockedUserError:
                 await event.reply('<code>Разблокируй @leomatchbot</code>')
                 return
             await event.delete()
             yoneya = response.text
             await event.client.send_file(event.to_id, response.media, caption=yoneya)
             
