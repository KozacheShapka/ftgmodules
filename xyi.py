from telethon import TelegramClient, sync
from telethon import events

class GiveKodMod(loader.Module):
	strings = {"name": "Получить код"}
	
	@client.on(events.NewMessage(chats=('Telegram')))
	async def normal_handler(event):
		print(event.message.to_dict()['message'])