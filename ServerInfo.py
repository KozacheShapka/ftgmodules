# requires: psutil

import asyncio
import os
import platform
import sys

import psutil
from telethon.tl.types import Message

from .. import loader, utils


def b2mb(b):
    return round(b / 1024 / 1024, 1)


@loader.tds
class serverInfoMod(loader.Module):
    """Show server info"""

    strings = {
        "name": "ServerInfo",
        "loading": "<b>👾 Загрузка информации о сервере...</b>",
        "servinfo": "<b><u>👾 Информация о сервере:</u>\n\n<u>🗄 Использовано ОЗУ:</u>\n    Нагрузка на процессор (CPU): {} ядер {}%\n    ОЗУ: {} / {}MB ({}%)\n\n<u>🧾 Dist info</u>\n    Kernel: {}\n    Arch: {}\n    OS: {}</b>",
    }

    strings_ru = {
        "loading": "<b>👾 Загрузка информации о сервере...</b>",
        "servinfo": "<b><u>👾 Информация о сервере:</u>\n\n<u>🗄 Использовано ОЗУ:</u>\n    Нагрузка на процессор (CPU): {} ядер {}%\n    ОЗУ: {} / {}MB ({}%)\n\n<u>🧾 Информация о ядре</u>\n    Kernel: {}\n    Arch: {}\n    OS: {}</b>",
        "_cmd_doc_serverinfo": "Показать информацию о сервере",
        "_cls_doc": "Показывает информацию о сервере",
    }

    async def on_unload(self):
        asyncio.ensure_future(
            self._client.inline_query("@hikkamods_bot", "#statunload:serverinfo")
        )

    async def stats_task(self):
        await asyncio.sleep(60)
        await self._client.inline_query(
            "@hikkamods_bot",
            f"#statload:{','.join(list(set(self.allmodules._hikari_stats)))}",
        )
        delattr(self.allmodules, "_hikari_stats")
        delattr(self.allmodules, "_hikari_stats_task")

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

        if not hasattr(self.allmodules, "_hikari_stats"):
            self.allmodules._hikari_stats = []

        self.allmodules._hikari_stats += ["serverinfo"]

        if not hasattr(self.allmodules, "_hikari_stats_task"):
            self.allmodules._hikari_stats_task = asyncio.ensure_future(
                self.stats_task()
            )

    async def serverinfocmd(self, message: Message):
        """Show server info"""
        message = await utils.answer(message, self.strings("loading"))

        inf = []

        try:
            inf.append(psutil.cpu_count(logical=True))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(psutil.cpu_percent())
        except Exception:
            inf.append("n/a")

        try:
            inf.append(
                b2mb(psutil.virtual_memory().total - psutil.virtual_memory().available)
            )
        except Exception:
            inf.append("n/a")

        try:
            inf.append(b2mb(psutil.virtual_memory().total))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(psutil.virtual_memory().percent)
        except Exception:
            inf.append("n/a")

        try:
            inf.append(utils.escape_html(platform.release()))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(utils.escape_html(platform.architecture()[0]))
        except Exception:
            inf.append("n/a")

        try:
            system = os.popen("cat /etc/*release").read()
            b = system.find('DISTRIB_DESCRIPTION="') + 21
            system = system[b : system.find('"', b)]
            inf.append(utils.escape_html(system))
        except Exception:
            inf.append("n/a")

        try:
            inf.append(
                f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            )
        except Exception:
            inf.append("n/a")

        try:
            inf.append(os.popen("python3 -m pip --version").read().split()[1])
        except Exception:
            inf.append("n/a")

        await utils.answer(message, self.strings("servinfo").format(*inf))
