from .. import loader
from telethon.tl.types import *
@loader.tds
class InformationMod(loader.Module):
  "Статистика чата"
  strings = {"name": "ChatStatistic"}
  @loader.owner
  async def statacmd(self, m):
	  await m.edit("<b>📊Подсчитываем...</b>")
	  al = str((await m.client.get_messages(m.to_id, limit=0)).total)
	  ph = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterPhotos())).total)
	  vi = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterVideo())).total)
	  mu = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterMusic())).total)
	  vo = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterVideo())).total)
	  vv = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterRoundVideo())).total)
	  do = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterDocument())).total)
	  urls = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterUrl())).total)
	  gifs = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterGif())).total)
	  geos = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterGeo())).total)
	  cont = str((await m.client.get_messages(m.to_id, limit=0, filter=InputMessagesFilterContacts())).total)
	  await m.edit(
	    ("<b>✉️Всего сообщений:</b> {}\n"+
	    "<b>🖼️Всего фотографий:</b> {}\n"+
	    "<b>📹Всего видео:</b> {}\n"+
	    "<b>🎵Всего аудиосообщений: :</b> {}\n"+
	    "<b>🎶Всего голосовых сообщений:</b> {}\n"+
	    "<b>🎥Всего видеосообщений (круглых):</b> {}\n"+
	    "<b>📂Всего файлов:</b> {}\n"+
	    "<b>🔗Всего ссылок:</b> {}\n"+
	    "<b>🎞️Всего GIF:</b> {}\n"+
	    "<b>🗺️Всего отправленных координат:</b> {}\n"+
	    "<b>👭Контаков:</b> {}").format(al, ph, vi, mu, vo, vv, do, urls, gifs, geos, cont))