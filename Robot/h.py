from telethon import TelegramClient, events
import asyncio
import RPi.GPIO as GPIO
import websockets
api_id = ''  # Thay thế với API ID của bạn
api_hash = ''  # Thay thế với API Hash của bạn
bot_token = ''  # Thay thế với bot token của bạn

# Tạo một instance của TelegramClient
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def gpio_recv(message):
    if message == "turn_on":
        GPIO.output(12,GPIO.HIGH)
    elif message == "turn_off":
        GPIO.output(12,GPIO.LOW)

@client.on(events.NewMessage)
async def echo(event):
    me = await client.get_me() 
    if event.message.sender_id == me.id:
        await asyncio.sleep(5)
        message_content=event.message.message
        print(message_content)
        if message_content == "turn_on":
                GPIO.output(12,GPIO.HIGH)
        elif message_content == "turn_off":
                GPIO.output(12,GPIO.LOW)
    else:
        return  # Nếu tin nhắn từ bot thì bỏ qua không xử lý
    #in ra tin nhắn người dùng gửi 
    
def main():
    # Bắt đầu bot

    client.run_until_disconnected()

if __name__ == '__main__':
    main()
