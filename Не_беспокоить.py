# @Sekai_Yoneya

from .. import loader 
from asyncio import sleep 
 
@loader.tds 
class EternalOnlineMod(loader.Module): 
    """Вечный онлайн, который будет читать сообщения в чатах.""" 
    strings = {'name': 'Не беспокоить'} 
 
    async def client_ready(self, client, db): 
        self.db = db 
 
    async def cmd(self, message): 
        """Режим "Не беспокоить".""" 
        if not self.db.get("Eternal Online", "status"): 
            self.db.set("Eternal Online", "status", True) 
            await message.edit("<b>⛔️Режим (Не беспокоить) включено!</b>") 
            while self.db.get("Eternal Online", "status"): 
                msg = await message.client.send_message("me", "Telegram best messenger! 🤩")
                await msg.delete()
                await sleep(1000) 
 
        else: 
            self.db.set("Eternal Online", "status", False) 
            await message.edit("<b>❌Режим (Не беспокоить) отключено!</b>")

    async def watcher(self, message): 
        if self.db.get("Eternal Online", "status"):
            await message.client.send_read_acknowledge(message.chat_id, clear_mentions=True)
