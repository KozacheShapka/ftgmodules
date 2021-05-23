#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import ast
import time
import logging
from io import BytesIO
from telethon.tl import functions
from .. import loader, utils

logger = logging.getLogger(__name__)

try:
    from PIL import Image
except ImportError:
    pil_installed = False
else:
    pil_installed = True


@loader.tds
class AutoProfileMod(loader.Module):
    """Автоматическое управление вашим профилем :P"""
    strings = {"name": "Autoprofile",
               "missing_pil": "<b>У вас не установлен модуль Pillow</b>",
               "missing_pfp": "<b>У вас нет изображения профиля для вращения</b>",
               "invalid_args": "<b>Отсутствуют параметры, пожалуйста, прочитайте документацию </b>",
               "invalid_degrees": "<b>Неверное значение градусов, пожалуйста, прочитайте документацию</b>",
               "invalid_delete": "<b>Пожалуйста, укажите, удалять старые фотографии или нет</b>",
               "enabled_pfp": "<b>Включен поворот изображения профиля</b>",
               "pfp_not_enabled": "<b>Вращение изображения профиля не включено</b>",
               "pfp_disabled": "<b>Поворот изображения профиля отключен</b>",
               "missing_time": "<b>Время в био не указано</b>",
               "enabled_bio": "<b>Часы в био включены</b>",
               "bio_not_enabled": "<b>Часы в био не включены</b>",
               "disabled_bio": "<b>Часы в био выключены</b>",
               "enabled_name": "<b>Включены часы в имени</b>",
               "name_not_enabled": "<b>Часы в имени не включены</b>",
               "disabled_name": "<b>Часы в имени выключены</b>",
               "how_many_pfps": "<b>Пожалуйста, укажите, сколько фотографий профиля должно быть удалено</b>",
               "invalid_pfp_count": "<b>Неверное количество фотографий профиля для удаления</b>",
               "removed_pfps": "<b>Удалено {} фотографий профиля</b>"}

    def __init__(self):
        self.bio_enabled = False
        self.name_enabled = False
        self.pfp_enabled = False
        self.raw_bio = None
        self.raw_name = None

    async def client_ready(self, client, db):
        self.client = client

    async def autopfpcmd(self, message):
        """Поворот изображения профиля (аватарки) каждые 60 секунд на x градусов, использование:
           .autopfp <градусы> <True/1/False/0>

           Градусы - 60, -10, и т.д.
           Удаление последнего изображения - True/1/False/0, чувствительный к регистру"""

        if not pil_installed:
            return await utils.answer(message, self.strings("missing_pil", message))

        if not await self.client.get_profile_photos("me", limit=1):
            return await utils.answer(message, self.strings("missing_pfp", message))

        msg = utils.get_args(message)
        if len(msg) != 2:
            return await utils.answer(message, self.strings("invalid_args", message))

        try:
            degrees = int(msg[0])
        except ValueError:
            return await utils.answer(message, self.strings("invalid_degrees", message))

        try:
            delete_previous = ast.literal_eval(msg[1])
        except (ValueError, SyntaxError):
            return await utils.answer(message, self.strings("invalid_delete", message))

        with BytesIO() as pfp:
            await self.client.download_profile_photo("me", file=pfp)
            raw_pfp = Image.open(pfp)

            self.pfp_enabled = True
            pfp_degree = 0
            await self.allmodules.log("start_autopfp")
            await utils.answer(message, self.strings("enabled_pfp", message))

            while self.pfp_enabled:
                pfp_degree = (pfp_degree + degrees) % 360
                rotated = raw_pfp.rotate(pfp_degree)
                with BytesIO() as buf:
                    rotated.save(buf, format="JPEG")
                    buf.seek(0)

                    if delete_previous:
                        await self.client(functions.photos.
                                          DeletePhotosRequest(await self.client.get_profile_photos("me", limit=1)))

                    await self.client(functions.photos.UploadProfilePhotoRequest(await self.client.upload_file(buf)))
                    buf.close()
                await asyncio.sleep(60)

    async def stopautopfpcmd(self, message):
        """Остановка вращения аватарки"""

        if self.pfp_enabled is False:
            return await utils.answer(message, self.strings("pfp_not_enabled", message))
        else:
            self.pfp_enabled = False

            await self.client(functions.photos.DeletePhotosRequest(
                await self.client.get_profile_photos("me", limit=1)
            ))
            await self.allmodules.log("stop_autopfp")
            await utils.answer(message, self.strings("pfp_disabled", message))

    async def autobiocmd(self, message):
        """Автоматически изменяет биографию вашего аккаунта в зависимости от текущего времени и использование:
            .autobio '<сообщение, время как {time}>'"""

        msg = utils.get_args(message)
        if len(msg) != 1:
            return await utils.answer(message, self.strings("invalid_args", message))
        raw_bio = msg[0]
        if "{time}" not in raw_bio:
            return await utils.answer(message, self.strings("missing_time", message))

        self.bio_enabled = True
        self.raw_bio = raw_bio
        await self.allmodules.log("start_autobio")
        await utils.answer(message, self.strings("enabled_bio", message))

        while self.bio_enabled is True:
            current_time = time.strftime("%H:%M")
            bio = raw_bio.format(time=current_time)
            await self.client(functions.account.UpdateProfileRequest(
                about=bio
            ))
            await asyncio.sleep(60)

    async def stopautobiocmd(self, message):
        """Остановка автобио"""

        if self.bio_enabled is False:
            return await utils.answer(message, self.strings("bio_not_enabled", message))
        else:
            self.bio_enabled = False
            await self.allmodules.log("stop_autobio")
            await utils.answer(message, self.strings("disabled_bio", message))
            await self.client(functions.account.UpdateProfileRequest(about=self.raw_bio.format(time="")))

    async def autonamecmd(self, message):
        """Автоматически меняет ваше имя в Telegram с текущим временем, использование:
            .autoname '<сообщение, время как {time}>'"""

        msg = utils.get_args(message)
        if len(msg) != 1:
            return await utils.answer(message, self.strings("invalid_args", message))
        raw_name = msg[0]
        if "{time}" not in raw_name:
            return await utils.answer(message, self.strings("missing_time", message))

        self.name_enabled = True
        self.raw_name = raw_name
        await self.allmodules.log("start_autoname")
        await utils.answer(message, self.strings("enabled_name", message))

        while self.name_enabled is True:
            current_time = time.strftime("%H:%M")
            name = raw_name.format(time=current_time)
            await self.client(functions.account.UpdateProfileRequest(
                first_name=name
            ))
            await asyncio.sleep(60)

    async def stopautonamecmd(self, message):
        """Остановка часов в имени"""

        if self.name_enabled is False:
            return await utils.answer(message, self.strings("name_not_enabled", message))
        else:
            self.name_enabled = False
            await self.allmodules.log("stop_autoname")
            await utils.answer(message, self.strings("disabled_name", message))
            await self.client(functions.account.UpdateProfileRequest(
                first_name=self.raw_name.format(time="")
            ))

    async def delpfpcmd(self, message):
        """Удалить n-ное количество фото профиля из вашего профиля.
        .delpfp <pfps count/unlimited - удалить все>"""

        args = utils.get_args(message)
        if not args:
            return await utils.answer(message, self.strings("how_many_pfps", message))
        try:
            pfps_count = int(args[0])
        except ValueError:
            return await utils.answer(message, self.strings("invalid_pfp_count", message))
        if pfps_count < 0:
            return await utils.answer(message, self.strings("invalid_pfp_count", message))
        if pfps_count == 0:
            pfps_count = None

        to_delete = await self.client.get_profile_photos("me", limit=pfps_count)
        await self.client(functions.photos.DeletePhotosRequest(to_delete))

        await self.allmodules.log("delpfp")
        await utils.answer(message, self.strings("removed_pfps", message).format(len(to_delete)))
        return await utils.answer(message, self.strings("how_many_pfps", message))
