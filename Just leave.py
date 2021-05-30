from .. import loader, utils
from asyncio import sleep
from telethon.tl.functions.channels import LeaveChannelRequest
@loader.tds
class LeaveMod(loader.Module):
	strings = {"name": "Just leave"}
	@loader.sudo
	async def leavecmd(self, message):
		""".leave"""
		if not message.chat:
			await message.edit("<b>Я выхожу из группы. Всем пока😔...</b>")
			return
		text = utils.get_args_raw(message)
		if not text:
			text = "Я выхожу из группы. Всем пока..."
		if text.lower() == "del":
			await message.delete()
		else:
			await message.edit(f"<b>{text}</b>")
		await sleep(1)
		await message.client(LeaveChannelRequest(message.chat_id))
		
		
