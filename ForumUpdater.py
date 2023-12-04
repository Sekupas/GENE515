import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio

#49 и 83 строки - время реактивации веток
class ForumUpdater: # subclass discord.Bot
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    global scheduler
    scheduler = AsyncIOScheduler()

    global timestamp
    global data
    global message_ceo
    global debug

    timestamp = 0 #Переменная для времени по умолчанию, НЕ ТРОГАТЬ!

    message_ceo = "1179848493746102302" #Id главного сообщения в ветке управления
    debug = 1  #Переменная для вывода времени в терминал, при 1 - включено

    async def timestamps(self):
        global timestamp
        global data

        if timestamp == 0:
            channel = self.bot.get_channel(int(message_ceo))
            messages = [message.content.split("\n") async for message in channel.history(limit=10)]

            timestamp = int(messages[-1][0].split(" ")[2].split(":")[0])
            text = messages[-1][0].split(" ")[0]

            messages[-1].remove(messages[-1][0])
            
            ids = []

            for message in messages:
                ids = ids + message
            
            ids = [int(id.split("/")[5]) for id in ids]
            ids = list(set(ids))
            data = {"text":text, "ids":ids}

            if debug == 1:
                print(data)

    
    async def on_ready(self):
        print("Модуль загружен")
        await self.timestamps()
        scheduler.add_job(self.tick, 'interval', [data], seconds=timestamp, id="renews") #Время реактивации ветки

        if debug == 1:
            print('Tick! The time is: %s' % datetime.now())
        
        scheduler.start()

    async def tick(self, data: list):
        
        text = data["text"]
        ids = data["ids"]
        for id in ids:
            #print(f'IDS: {id}')
            channel = self.bot.get_channel(int(id))
            msg = await channel.send(text)
            await msg.delete()
            await asyncio.sleep(10)

        if debug == 1:
            print('Tick! The time is: %s' % datetime.now())

