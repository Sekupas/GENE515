import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

#48 и 82 строки - время реактивации веток
class ForumUpdater: # subclass discord.Bot
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    global scheduler
    scheduler = AsyncIOScheduler()

    global timestamp
    global data
    global message_ceo
    global debug
    timestamp = 0

    message_ceo = "1179848493746102302" #Id главного сообщения в ветке управления
    debug = 0

    async def timestamps(self):
        global timestamp
        global data

        if timestamp == 0:
            channel = self.bot.get_channel(int(message_ceo))
            message = (await channel.fetch_message(int(message_ceo))).content
            timestamp = int(message.split("\n")[0].split(" ")[2].split(":")[0])
            
            text = message.split("\n")[0].split(" ")[0]
            
            message = message.split("\n")
            message.remove(message[0])

            ids = [m.split("/")[5] for m in message]

            data = {"text":text, "ids":ids}
            if debug == 1:
                print(data)

    
    async def on_ready(self):
        global scheduler
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

        if debug == 1:
            print('Tick! The time is: %s' % datetime.now())

    async def on_raw_message_edit(self, payload):
        if payload.data["id"] == message_ceo: #Id главного сообщения в ветке управления
            scheduler.remove_job("renews")

            inc_message = payload.data["content"]
            inc_message = inc_message.split("\n")

            timestamp = int(inc_message[0].split(" ")[2].split(":")[0])
            text = inc_message[0].split(" ")[0]
            inc_message.remove(inc_message[0])

            ids = [m.split("/")[5] for m in inc_message]

            data = {"text":text, "ids":ids}

            scheduler.add_job(self.tick, 'interval', [data], seconds=timestamp, id="renew") #Время реактивации ветки
            


            if debug == 1:
                print('Tick! The time is: %s' % datetime.now())

