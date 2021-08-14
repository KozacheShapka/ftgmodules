from .. import loader, utils

from asyncio import sleep

from telethon.tl.functions.channels import LeaveChannelRequest

@loader.tds

class LeaveMod(loader.Module):

	strings = {"name": "BanMe"}	@loader.sudo

	async def leavecmd(self, message):

		""".banme"""

		if not message.chat:

			await message.edit("<b>Ты забанил себя, очень круто!</b>")

			return

		text = utils.get_args_raw(message)

		if not text:

			text = "Ты забанил себя, очень круто!"

		if text.lower() == "del":

			await message.delete()

		else:

			await message.edit(f"<b>{text}</b>")

		await sleep(1)

		await message.client(LeaveChannelRequest(message.chat_id))

		
