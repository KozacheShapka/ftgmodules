from .. import loader, utils
import os
def register(cb):
	cb(RipperMod())
class RipperMod(loader.Module):
	"""Ripper"""
	strings = {'name': 'Ripper'}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
	async def ripcmd(self, message):
		
		
		reply = await message.get_reply_message()
		if utils.get_args_raw(message):
			ript = utils.get_args_raw(message)
		else:
			try:
				reply.sender
				ript = reply.sender.first_name
			except:
				await message.edit("""<code>
⁠      _
    __| |__ 
   |_R.I.P_|
      | |   
      | |   
      | |   
      |_|
</code>""")
				return
		await message.edit(f"""<code>
⁠      _
    __| |__ 
   |_R.I.P_|
      | |   
      | |   
      | |   
      |_|

{ript} я сделал тебе крест</code>
""")