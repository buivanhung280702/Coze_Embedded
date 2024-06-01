# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
import RPi.GPIO as GPIO
import time
from time import sleep
import asyncio

api_id = '25616146'  # Thay the v?i API ID cua b?n
api_hash = '2a9896803ebea0b5adeff92643b7ad7a'  # Thay the v?i API Hash cua b?n
bot_token = '6939367105:AAGrDy26zodC9SWzpSD_sOqu2upfLk2V6Ac'# mã token cua bot chat

# Thi?t l?p GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_PIN = 12
Checking = 16
MOISTURE_SENSOR_PIN = 27  # Chân GPIO cho c?m bi?n d? ?m d?t

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(Checking, GPIO.OUT)
GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

# T?o m?t instance c?a TelegramClient
client = TelegramClient('bot', api_id, api_hash)

async def start_bot():
    await client.start(bot_token=bot_token)
    print("Da khoi dong thanh cong")

@client.on(events.NewMessage)
async def echo(event):
    me = await client.get_me()
    if event.message.sender_id == me.id:
        message_content = event.message.message.lower()
        print(message_content)
        
        if message_content == 'batmaybom' or message_content == 'datkho':
             GPIO.output(LED_PIN, GPIO.HIGH)  # Bat may bom nuoc
        elif message_content == 'tatmaybom' or message_content == 'datam':
             GPIO.output(LED_PIN, GPIO.LOW)  # Tat may bom nuoc
        elif message_content == 'checking...':
        
            # Blink LED
            for _ in range(5):
                GPIO.output(Checking, GPIO.HIGH)
                await asyncio.sleep(0.5)
                GPIO.output(Checking, GPIO.LOW)
                await asyncio.sleep(0.5)
                
            moisture_level = GPIO.input(MOISTURE_SENSOR_PIN)
            if moisture_level == 0:
                await event.reply('datam')
                #print(moisture_level)
            else:
                await event.reply('datkho')
               # print(moisture_level)
    else:
        return

async def main_loop():
    while True:
        moisture_level = GPIO.input(MOISTURE_SENSOR_PIN)
        if moisture_level == 0:
            print("datam")
            print(moisture_level)
        else:
            print("datkho")
            print(moisture_level)
        await asyncio.sleep(10)  # Ki?m tra c?m bi?n m?i 10 giây

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    loop.create_task(main_loop())
    loop.run_forever()

