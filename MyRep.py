from .. import loader, utils

@loader.tds
class MyRepMod(loader.Module):
    """Модуль с вашей репутацией | creator seen"""
    strings={"name":"MyRep"}

    async def client_ready(self, message, db):
        self.db=db
        self.db.set("MyRep", "repstatus", True)

    async def repcmd(self, message):
        """Включить режим репутаций."""
        repstatus = self.db.get("MyRep", "repstatus")
        if repstatus is not True:
            self.db.set("MyRep", "repstatus", True)
            await message.edit(f"<b>[MyRepMod] Режим репутаций включен!</b>")
        else:
            self.db.set("MyRep", "repstatus", False)
            await message.edit(f"<b>[MyRepMod] Режим репутаций выключен!</b>")

    async def myrepcmd(self, message):
        """Посмотреть свою репутацию. Используй: .myrep clear (очистка репутации)."""
        args = utils.get_args_raw(message)
        if args == "clear":
            self.db.set("MyRep", "my_repa", 0)
            return await message.edit("<b>[MyRepMod] Моя Репутация очищена.</b>")
        myrep = self.db.get("MyRep", "my_repa")
        repstatus = self.db.get("MyRep", "repstatus")
        if repstatus is not False:
            msg_repstatus = "[<i>Включен.</i>]"
        else:
            msg_repstatus = "[<i>Выключен.</i>]"
        await message.edit(f"♻️ <b>[</b><i>MyRepMod</i><b>]</b> ♻️\n<b>Статус режима: </b>{msg_repstatus}<b>\nМоя репутация: <i>{myrep}</i>.</b>")

    async def watcher(self, message):
        try:
            number = self.db.get("MyRep", "my_repa", 0)
            repstatus = self.db.get("MyRep", "repstatus")
            if message.mentioned:
                if repstatus is not False:
                    if message.text == "+":
                        number += 1
                        self.db.set("MyRep", "my_repa", number)
                        await message.reply(f"<b>Ты повысил(а) мою репутацию. \nИ теперь кол-во репутации в мою сторону: {number}👍.</b>")
                    elif message.text == "-":
                        total = int(number) - 1
                        self.db.set("MyRep", "my_repa", total)
                        await message.reply(f"<b>Ты понизил(а) мою репутацию. \n И теперь кол-во репутации в мою сторону: {total}👎.</b>")
        except: pass
