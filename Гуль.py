import io, inspect
from .. import loader, utils
from asyncio import sleep

@loader.tds
class GULMod(loader.Module):
    """Я - гуль!"""
    strings = {'name': 'ГУУУУЛЬ'}
    
    async def гульcmd(self, message):
        x = 1000
        await message.client.send_message(message.to_id, "Я - гуль!")
        await sleep(2)
        while x >0:
            await message.client.send_message(message.to_id, str(x) + " - 7 = " + str(x-7))
            x -= 7
            await sleep(0.01)