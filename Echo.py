#mod by Anonumyc Economy Team.

from .. import loader

@loader.tds
class EchoMod(loader.Module):
    """Эхо модуль."""
    strings = {'name': 'Echo'}

    async def client_ready(self, client, db):
        self.db = db

    async def echocmd(self, message):
        """Активировать/деактивировать Echo."""
        echos = self.db.get("Echo", "chats", []) 
        chatid = str(message.chat_id)

        if chatid not in echos:
            echos.append(chatid)
            self.db.set("Echo", "chats", echos)
            return await message.edit("<b>[Попуг]</b> ✅Включен! ")

        echos.remove(chatid)
        self.db.set("Echo", "chats", echos)
        return await message.edit("<b>[Попуг]</b> ❌Отключено!")


    async def watcher(self, message):
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in str(echos): return
        if message.sender_id == (await message.client.get_me()).id: return

        await message.client.send_message(int(chatid), message, reply_to=await message.get_reply_message() or message)
