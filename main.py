from ForumUpdater import ForumUpdater # import MyBot from /src
import discord
from discord.ext import commands
import logging
from Data import token


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=discord.Intents.all())

    async def setup_hook(self):
        # подсоединяем модуль
        module = ForumUpdater(self)
        self.add_listener(module.on_ready)
        #self.tree.copy_global_to(guild=discord.Object(id=974022203987357766))
        #await self.tree.sync()
        print("Синхронизация модулей")

    async def on_ready(self):
        print("Бот запущен")


bot = MyBot()

bot.run(token)