import random
from .. import loader
from telethon.tl.types import Message


@loader.tds
class PremiumStickersMod(loader.Module):
    """Sends premium stickers for free"""

    strings = {"name": "PremiumStickers"}

    async def premstickcmd(self, message: Message):
        """Send random premium sticker without premium"""
        if message.out:
            await message.delete()

        await message.respond(
            f'<a href="https://t.me/hikka_premum_stickers/{random.randint(2, 106)}">­</a>',
        )
