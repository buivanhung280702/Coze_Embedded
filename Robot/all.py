# -*- coding: utf-8 -*-
import requests
import json
from telethon import TelegramClient, events
import asyncio
import RPi.GPIO as GPIO
import websockets
import Adafruit_DHT

SERVO_PIN = 17
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 19  # Replace with your GPIO pin


api_id = '28741519'  # Thay th? v?i API ID c?a b?n
api_hash = '13fd535bdc42a7c3af2ed201fb544eb6'  # Thay th? v?i API Hash c?a b?n
bot_token = '7187467922:AAGVKkTdMTSwXdvRkWgNJdGvUnV5TCPyKnY'  # Thay th? v?i bot token c?a b?n

# T?o m?t instance c?a TelegramClient
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
servo1 = GPIO.PWM(SERVO_PIN, 50)  # Tần số PWM 50Hz
servo1.start(0)  # Bắt đầu PWM với chu kỳ làm việc 0%
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def read_sensor():
    
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        
        return temperature, humidity
    else:
        
        return None, None

def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 180.0) * 10.0

#truyen message den GPIO 
def gpio_recv(led, servo, horn):
    if led == "led_on" and servo == "servo_on" and horn == "horn_on":
        GPIO.output(25, GPIO.HIGH)
        servo1.ChangeDutyCycle(angle_to_duty_cycle(120))
        GPIO.output(5, GPIO.HIGH)
    elif led == "led_off" and servo == "servo_off" and horn == "horn_off":
        GPIO.output(25, GPIO.LOW)
        servo1.ChangeDutyCycle(angle_to_duty_cycle(0))
        GPIO.output(5, GPIO.LOW)
    else:
        if led == "led_on":
            GPIO.output(25, GPIO.HIGH)
        elif led == "led_off":
            GPIO.output(25, GPIO.LOW)

        if servo == "servo_on":
            servo1.ChangeDutyCycle(angle_to_duty_cycle(120))
        elif servo == "servo_off":
            servo1.ChangeDutyCycle(angle_to_duty_cycle(0))

        if horn == "horn_on":
            GPIO.output(5, GPIO.HIGH)
        elif horn == "horn_off":
            GPIO.output(5, GPIO.LOW)
user_message=None
pre_user_message=None
@client.on(events.NewMessage)
async def echo(event):
    me = await client.get_me() 
    
    if event.message.sender_id == me.id:
        await asyncio.sleep(5)
        #luu message bot phan hoi vao bien
        
        message_content=event.message.message
        
        print(message_content)
        gpio_recv(message_content,message_content,message_content)
    else:
        global user_message
        user_message = event.message.message
        print(f"đây là1{user_message}")
        if user_message in ["temp", "nhiệt độ", "độ ẩm"]:
            global temperature
            global humidity
            temperature, humidity = read_sensor()
            if temperature is not None and humidity is not None:
                response = f"Nhiệt độ: {temperature:.2f}°C\nĐộ ẩm: {humidity:.2f}%"
            await event.reply(response)
        await get_mes_api_coze(user_message=user_message)
        await socket_client(led_sta=led_sta,horn_sta=horn_sta,servo_sta=servo_sta)
        
        
          # N?u tin nh?n t? bot th� b? qua kh�ng x? l�
    #in ra tin nh?n ngu?i d�ng g?i 
temperature=None
pre_temp=None
humidity=None
pre_humi=None
async def socket_client(led_sta,horn_sta,servo_sta):
    uri = "ws://192.168.43.250:3000"
    async with websockets.connect(uri) as websocket:
        # Nh?n tin nh?n ch�o m?ng t? server
        
        welcome_message = await websocket.recv()
        print(f"< {welcome_message}")
        
        # G?i tin nh?n d?n server
        await websocket.send("Hello, Server!")
        print("> Hello, Server!")
        #await websocket.send(led_sta)
        # Nh?n v� in ra tin nh?n t? server
        pre_led_sta=None
        pre_servo_sta=None
        pre_horn_sta=None
        while True:
            
            global pre_temp
            global pre_humi
            print("đang chạy socket....")
            if led_sta != pre_led_sta:
                
                await websocket.send(led_sta)
                pre_led_sta=led_sta
            if servo_sta != pre_servo_sta:
                await websocket.send(servo_sta)
                pre_servo_sta=servo_sta
            if horn_sta != pre_horn_sta:
                await websocket.send(horn_sta)
                pre_horn_sta=horn_sta
            
            response_message = await websocket.recv()

            gpio_recv(response_message,response_message,response_message)
            
            print(f"< {response_message}")
led_sta=None
servo_sta=None
horn_sta=None
async def get_mes_api_coze(user_message):
    
    token='pat_raTjlBFcDxb407ESrwH2ahfcWjbBBOx72exn8nh1JuvP4JbFaPNcd6EVnUEJrtKt'
    

    coze_url="https://api.coze.com/open_api/v2/chat"
    coze_headers={
    'Authorization': f'Bearer {token}',
    'Content-Type':'application/json',
    'Connection': 'keep-alive',
    'Accept':'*/*',
}
    
    
    global pre_user_message
    print("Starting get_mes_api_coze...")
    if(user_message!=pre_user_message and user_message !=None):
        print(f"đây là{user_message}")
        
        pre_user_message=user_message
        query=user_message
        data=json.dumps({
        "bot_id":"7369197409735327751",
        "user":"demo",
        "query":f"sử dụng các biến led,horn,servo để phản hồi yêu cầu liên quan đến bật tắt thiết bị :{query}",
        "stream": False
    })
        print("Sending request to API...")
        resp=requests.post(coze_url,data=data,headers=coze_headers)
        
        a=resp.json()

        
            
    #print(resp)
    
        # #a={'messages': [{'role': 'assistant',
        # 'type': 'function_call',
        # 'content': '{"name":"keyword_memory-setKeywordMemory","arguments":{"data":[{"keyword":"servo","value":"off"},{"keyword":"led","value":"on"},{"keyword":"horn","value":"on"}]},"plugin_id":7263427170075148306,"api_id":7288908904883322882,"plugin_type":1}',
        # 'content_type': 'text'},
        # {'role': 'assistant',
        # 'type': 'tool_response',
        # 'content': '{"status":"success","reason":""}',
        # 'content_type': 'text'},
        # {'role': 'assistant',
        # 'type': 'answer',
        # 'content': 'Đã thực hiện theo yêu cầu của bạn:\n\n-   🪄 Servo: off\n-   🪄 Đèn(Led): on\n-   🪄 Còi(Horn): on\n\nNếu bạn cần thay đổi trạng thái của các thiết bị, hãy yêu cầu!',
        # 'content_type': 'text'},
        # {'role': 'assistant',
        # 'type': 'verbose',
        # 'content': '{"msg_type":"generate_answer_finish","data":""}',
        # 'content_type': 'text'}],
        # 'conversation_id': '8201b3b6838844fba6b011fd73248d60',
        # 'code': 0,
        # 'msg': 'success'}
    
        json_string = json.dumps(a)

        #chuyển sang dạng data
        jsondt=json.loads(json_string)
        messages=jsondt["messages"]  # lấy value của key "message"
        #print(messages)
        print(messages)
        typea=messages[0]["type"]
        print(typea)
        print("chuan bi vao if.............. ")
        if typea =="function_call":
            a
            led_status=messages[0]["content"]
            print(f"led_status: {led_status}")
            led_dt=json.loads(led_status)
            argument=led_dt["arguments"]
            #print(argument)
            print(f"đây là1{user_message}")
            for keyword in argument["data"]:
                if(keyword["keyword"]=="servo"):
                    global servo_sta
                    servo_sta=keyword["keyword"]+'_'+keyword["value"]
                elif(keyword["keyword"]=="led"):
                    global led_sta
                    led_sta=keyword["keyword"]+'_'+keyword["value"]
                else:
                    global horn_sta
                    horn_sta=keyword["keyword"]+'_'+keyword["value"]
                # print(horn_sta)
                # print(led_sta)
                # print(servo_sta)
                gpio_recv(led_sta,servo_sta,horn_sta)
        else:
            print("ko co function......")
async def main():
    # B?t d?u Telegram client
    #await client.start(bot_token=bot_token)
    # Ch?y c? Telegram client v� WebSocket client d?ng th?i
    await asyncio.gather(
        client.run_until_disconnected(),
        socket_client(led_sta,horn_sta,servo_sta)
        # get_mes_api_coze(user_message=user_message)
    )

if __name__ == '__main__':
    # T?o event loop
    loop = asyncio.get_event_loop()
    # Thi?t l?p event loop cho asyncio n?u chua c�
    asyncio.set_event_loop(loop)
    # Ch?y h�m main() trong event loop
    loop.run_until_complete(main())
