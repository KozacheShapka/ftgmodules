from .. import loader, utils

@loader.tds
class ChannelRepostMod(loader.Module):
    """Модуль ChannelRepost"""
    strings = {'name': 'ChannelRepost'}

    async def client_ready(self, client, db):
        self.db = db

    async def setchcmd(self, message):
        """Используй: .setch «айди канала» чтобы отслеживать посты с канала."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Укажи аргументы.")
        try:
            chat = await message.client.get_entity(int(args))
            self.db.set("ChannelRepost", "channel", str(chat.id))
        except ValueError: return await message.edit("Канал/чат не найден.")
        await message.edit(f"Канал/чат «{chat.title}» для просмотра текста установлен.")

    async def setrhcmd(self, message):
        """Используй: .setrh «айди канала» чтобы пересылать посты с отслеживаемого канала."""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Укажи аргументы.")
        try:
            chat = await message.client.get_entity(int(args))
            self.db.set("ChannelRepost", "repost_channel", str(chat.id))
        except ValueError: return await message.edit("Канал/чат не найден.")
        await message.edit(f"Канал/чат «{chat.title}» для пересылки текста установлен.")

    async def channelrepostcmd(self, message):
        """Используй: .channelrepost чтобы посмотреть инфу о каналах, или аргумент «clear» (по желанию)"""
        args = utils.get_args_raw(message)
        if args == "clear":
            self.db.set("ChannelRepost", "channel", None)
            self.db.set("ChannelRepost", "repost_channel", None)
            await message.edit("Списки очищены.")
        if not args:
            try:
                get = self.db.get("ChannelRepost", "channel")
                rget = self.db.get("ChannelRepost", "repost_channel")
                get_channel = await message.client.get_entity(int(get))
                repost_channel = await message.client.get_entity(int(rget))
                await message.edit(f"Информация крч..\n\n"
                                   f"Для слежки - «{get_channel.title}» | ID: <code>{get_channel.id}</code>\n"
                                   f"Для пересылки - «{repost_channel.title}» | ID: <code>{repost_channel.id}</code>")
            except: return await message.edit("Списки пусты.")

    async def watcher(self, message):
        try:
            me = (await message.client.get_me()).id
            get = self.db.get("ChannelRepost", "channel")
            rget = self.db.get("ChannelRepost", "repost_channel")
            get_channel = f"-100{get}"
            repost_channel = f"-100{rget}"
            if message.chat_id == int(get_channel):
                await message.client.send_message(int(repost_channel), f"{message.text}")
        except: pass
