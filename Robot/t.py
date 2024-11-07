# -*- coding: utf-8 -*-


from telethon import TelegramClient, events
import asyncio
import RPi.GPIO as GPIO
import websockets
import Adafruit_DHT
SERVO_PIN = 17
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 19  # Replace with your GPIO pin

api_id = ''  # Thay th? v?i API ID c?a b?n
api_hash = ''  # Thay th? v?i API Hash c?a b?n
bot_token = ''  # Thay th? v?i bot token c?a b?n

# T?o m?t instance c?a TelegramClient
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)


motion = 0
motionNew = 0
servo = GPIO.PWM(SERVO_PIN, 50)  # Tần số PWM 50Hz
servo.start(0)  # Bắt đầu PWM với chu kỳ làm việc 0%

def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 180.0) * 10.0

def servoc(mee):
    if mee == "servo1":
        servo.ChangeDutyCycle(angle_to_duty_cycle(120))
    elif mee =="servo0":
        servo.ChangeDutyCycle(angle_to_duty_cycle(0))

def read_sensor():
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        
        return temperature, humidity
    else:
        
        return None, None

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
#truyen message den GPIO 
def gpio_recv(message):
    if message == "led_on":
        GPIO.output(18,GPIO.HIGH)
    elif message == "led_off":
        GPIO.output(18,GPIO.LOW)
    elif message=="servo_on":
        servo.ChangeDutyCycle(angle_to_duty_cycle(120))
    elif message=="servo_off":
        servo.ChangeDutyCycle(angle_to_duty_cycle(0))
@client.on(events.NewMessage)
async def echo(event):
    me = await client.get_me() 
    if event.message.sender_id == me.id:
        await asyncio.sleep(5)
        #luu message bot phan hoi vao bien
        message_content=event.message.message
        print(message_content)
        gpio_recv(message_content)
    else:
        user_message = event.message.message
        print(f"ĐÂu {user_message}")
        servoc(user_message)
        if user_message =="/tt":
            print(response_message)
        elif user_message in ["temp", "nhiệt độ", "độ ẩm"]:
            global temperature
            global humidity
            temperature, humidity = read_sensor()
            if temperature is not None and humidity is not None:
                response = f"Nhiệt độ: {temperature:.2f}°C\nĐộ ẩm: {humidity:.2f}%"
            await event.reply(response)

        #await get_mes_api_coze(user_message=user_message)
    #in ra tin nh?n ngu?i d�ng g?i 
temperature=None
pre_temp=None
humidity=None
pre_humi=None
async def socket_client():
    uri = "ws://192.168.43.250:3000"
    async with websockets.connect(uri) as websocket:
        # Nh?n tin nh?n ch�o m?ng t? server
        welcome_message = await websocket.recv()
        print(f"< {welcome_message}")

        # G?i tin nh?n d?n server
        await websocket.send("Hello, Server!")
        print("> Hello, Server!")

        # Nh?n v� in ra tin nh?n t? server
        while True:
            global response_message
            global pre_temp
            global pre_humi
            if temperature!=pre_temp and temperature != None and humidity !=None and humidity !=pre_humi:
                await websocket.send(f"{temperature}/{humidity}")
                pre_temp=temperature
                pre_humi=humidity
            response_message = await websocket.recv()
            gpio_recv(response_message)
           
            print(f"< {response_message}")  

async def main():
    # B?t d?u Telegram client
    #await client.start(bot_token=bot_token)
    # Ch?y c? Telegram client v� WebSocket client d?ng th?i
    await asyncio.gather(
        client.run_until_disconnected(),
        socket_client()
    )

if __name__ == '__main__':
    # T?o event loop
    loop = asyncio.get_event_loop()
    # Thi?t l?p event loop cho asyncio n?u chua c�
    asyncio.set_event_loop(loop)
    # Ch?y h�m main() trong event loop
    loop.run_until_complete(main())
