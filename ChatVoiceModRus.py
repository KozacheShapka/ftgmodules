#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

# Перевод от https://t.me/kozacheshapka #

# requires: py-tgcalls

from typing import *

import pytgcalls
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo)
from telethon import types

from .. import loader, utils


@loader.tds
class ChatVoiceMod(loader.Module):
    """Module for working with voicechat"""
    strings = {
        "name": "ChatVoiceMod",
        "downloading": "<b>[ChatVoiceMod]</b> 🟡Скачиваю...",
        "playing": "<b>[ChatVoiceMod]</b> 🟢Воспроизодится...",
        "notjoined": "<b>[ChatVoiceMod]</b> ❌Ты не зашёл(-ла) в голосовой чат",
        "stop": "<b>[ChatVoiceMod]</b> 🔴Остановлено...",
        "leave": "<b>[ChatVoiceMod]</b> 🔴Отключился...",
        "pause": "<b>[ChatVoiceMod]</b> ⏸️На паузе...",
        "resume": "<b>[ChatVoiceMod]</b> ▶️ Воспроизводится...",
        "mute": "<b>[ChatVoiceMod]</b> 🔇Без звука...",
        "unmute": "<b>[ChatVoiceMod]</b> 🔊Восстановлен звук...",
        "error": "<b>[ChatVoiceMod]</b> ⚠️Ошибка: <code>{}</code>",
        "noargs": "<b>[ChatVoiceMod]</b> ❌Нет аргуметов",
    }

    async def client_ready(self, client, _):
        self.client = client
        self.call = PyTgCalls(client)
        @self.call.on_stream_end()
        async def _h(client: PyTgCalls, update):
            try:
                await self.call.leave_group_call(update.chat_id)
            except Exception as e:
                await self.client.send_message(update.chat_id, self.strings("error").format(str(e)))
        await self.call.start()

    async def cplayvcmd(self, m: types.Message):
        "<ссылка/файл/ответ на видео> - Воспроизвести видео в голосовом чате"
        try:
            reply = await m.get_reply_message()
            path = utils.get_args_raw(m)
            chat = m.chat.id
            if not path:
                if not reply:
                    return await utils.answer(m, self.strings("noargs"))
                m = await utils.answer(m, self.strings("downloading"))
                path = await reply.download_media()
            try:
                self.call.get_active_call(chat)
                await self.call.leave_group_call(chat)
            except pytgcalls.exceptions.GroupCallNotFound:
                pass
            await self.call.join_group_call(
                chat,
                AudioVideoPiped(
                    path,
                    HighQualityAudio(),
                    HighQualityVideo(),
                ),
                stream_type=StreamType().pulse_stream
            )
            await utils.answer(m, self.strings("playing"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))

    async def cplayacmd(self, m: types.Message):
        "<ссылка/файл/ответ на аудио> - Воспроизвести музыку в голосовом чате"
        try:
            reply = await m.get_reply_message()
            path = utils.get_args_raw(m)
            chat = m.chat.id
            if not path:
                if not reply:
                    return await utils.answer(m, self.strings("noargs"))
                m = await utils.answer(m, self.strings("downloading"))
                path = await reply.download_media()
            try:
                self.call.get_active_call(chat)
                await self.call.leave_group_call(chat)
            except pytgcalls.exceptions.GroupCallNotFound:
                pass
            await self.call.join_group_call(
                chat,
                AudioPiped(
                    path,
                    HighQualityAudio(),
                ),
                stream_type=StreamType().pulse_stream
            )
            await utils.answer(m, self.strings("playing"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))

    async def cleavecmd(self, m: types.Message):
        "Отключиться от голосового чата"
        try:
            self.call.get_active_call(m.chat.id)
            await self.call.leave_group_call(m.chat.id)
            await utils.answer(m, self.strings("leave"))
        except pytgcalls.exceptions.GroupCallNotFound:
            await utils.answer(m, self.strings("notjoined"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))

    async def cmutecmd(self, m: types.Message):
        "Без звука"
        try:
            self.call.get_active_call(m.chat.id)
            await self.call.mute_stream(m.chat.id)
            await utils.answer(m, self.strings("mute"))
        except pytgcalls.exceptions.GroupCallNotFound:
            await utils.answer(m, self.strings("notjoined"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))

    async def cunmutecmd(self, m: types.Message):
        "Восстановить звук"
        try:
            self.call.get_active_call(m.chat.id)
            await self.call.unmute_stream(m.chat.id)
            await utils.answer(m, self.strings("unmute"))
        except pytgcalls.exceptions.GroupCallNotFound:
            await utils.answer(m, self.strings("notjoined"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))

    async def cpausecmd(self, m: types.Message):
        "Пауза"
        try:
            self.call.get_active_call(m.chat.id)
            await self.call.pause_stream(m.chat.id)
            await utils.answer(m, self.strings("pause"))
        except pytgcalls.exceptions.GroupCallNotFound:
            await utils.answer(m, self.strings("notjoined"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))

    async def cresumecmd(self, m: types.Message):
        "Продолжить воспроизведение"
        try:
            self.call.get_active_call(m.chat.id)
            await self.call.resume_stream(m.chat.id)
            await utils.answer(m, self.strings("resume"))
        except pytgcalls.exceptions.GroupCallNotFound:
            await utils.answer(m, self.strings("notjoined"))
        except Exception as e:
            await utils.answer(m, self.strings("error").format(str(e)))
