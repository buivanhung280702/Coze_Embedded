from telethon import TelegramClient, events
import RPi.GPIO as GPIO
import time
from time import sleep
import asyncio

api_id = ''  # Thay thế với API ID của bạn
api_hash = ''  # Thay thế với API Hash của bạn
bot_token = ''

# Thiết lập GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_PIN = 12
LED_PIN_1 = 16
PIR = 4
SERVO_PIN = 17
TRIG = 23
ECHO = 24
LED_PIN_ULTRASONIC = 25  # LED được điều khiển bởi cảm biến siêu âm (chân 29)
MQ2_PIN = 13  # Chân GPIO cho cảm biến MQ-2
BUZZER_PIN = 5  # Chân GPIO cho loa piezo

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN_ULTRASONIC, GPIO.OUT)
GPIO.setup(MQ2_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

motion = 0
motionNew = 0
servo = GPIO.PWM(SERVO_PIN, 50)  # Tần số PWM 50Hz
servo.start(0)  # Bắt đầu PWM với chu kỳ làm việc 0%

buzzer = GPIO.PWM(BUZZER_PIN, 1000)  # Thiết lập PWM cho loa piezo với tần số 1kHz
mq2_value = 1;

# Trạng thái điều khiển servo
servo_controlled_by_bot = False

# Tạo một instance của TelegramClient
client = TelegramClient('bot', api_id, api_hash)

async def start_bot():
    await client.start(bot_token=bot_token)
    print("Bot đã được khởi động và kết nối thành công.")

@client.on(events.NewMessage)
async def echo(event):
    global servo_controlled_by_bot
    global mq2_value
    me = await client.get_me()
    if event.message.sender_id == me.id:
        message_content = event.message.message.lower()
        print(message_content)
        asyncio.sleep(5)
        
        if message_content == 'onpk':
            GPIO.output(LED_PIN, GPIO.HIGH)  # Bật LED
            response = "đèn phòng khách đã bật"
          #  await event.reply(response)
        elif message_content == 'offpk':
            GPIO.output(LED_PIN, GPIO.LOW)  # Tắt LED
            response = "đèn phòng khách đã tat"
        elif message_content == 'onpn':
            GPIO.output(LED_PIN_1, GPIO.HIGH)  # Bật LED 1
            response = "đèn phòng ngu đã bật"
        elif message_content == 'offpn':
            GPIO.output(LED_PIN_1, GPIO.LOW)  # Tắt LED 1
            response = "đèn phòng ngu đã tat"
        elif message_content == 'mocua':
            servo_controlled_by_bot = True
            controlServo(1)  # Mở cửa (quay servo 90 độ)
            response = "cua da mo"
            servo_controlled_by_bot = False
        elif message_content == 'dongcua':
            servo_controlled_by_bot = True
            controlServo(0)  # Đóng cửa (quay servo về 0 độ)
            response = "da dong cua"
            servo_controlled_by_bot = False
        elif message_content == 'tatden':
            GPIO.output(LED_PIN_1, GPIO.LOW)  # Tắt LED 1
            GPIO.output(LED_PIN, GPIO.LOW)
            response = "đa tat den"
        elif message_content == 'batden':
            GPIO.output(LED_PIN_1, GPIO.HIGH)  # Tắt LED 1
            GPIO.output(LED_PIN, GPIO.HIGH)
            response = "đa bat den"
        elif message_content == 'dangkiemtra':
            mq2_value = GPIO.input(MQ2_PIN)
            if mq2_value == 0:  # MQ-2 phát hiện khí gas
                await event.reply('co gas nguy hiem')
                #await send_gas_alert()  # Gửi cảnh báo lên bot Telegram
            else:
                await event.reply('khong co gas')
        
        await event.reply(response)
    else:
        return

async def main_loop():
    global motion 
    global motionNew
    global servo_controlled_by_bot
    global mq2_value

    while True:
        if not servo_controlled_by_bot:  # Chỉ kiểm tra cảm biến nếu không bị bot điều khiển
            if GPIO.input(PIR) == 1:
                print("Motion detected")
                motion = 1
                if motionNew != motion:
                    motionNew = motion
                    controlServo(motion)
            elif GPIO.input(PIR) == 0:
                print("No motion detected")
                motion = 0
                if motionNew != motion:
                    motionNew = motion
                    controlServo(motion)
            
            distance = measure_distance()
            print("khoang cach: {} cm".format(distance))
            if distance < 20:  # Giới hạn khoảng cách để bật đèn
                GPIO.output(LED_PIN_ULTRASONIC, GPIO.HIGH)  # Bật đèn LED
            else:
                GPIO.output(LED_PIN_ULTRASONIC, GPIO.LOW)  # Tắt đèn LED
            
            # Đọc giá trị từ cảm biến MQ-2
            mq2_value = GPIO.input(MQ2_PIN)
            print("MQ-2 value: {}".format(mq2_value))
            if mq2_value == 0:  # MQ-2 phát hiện khí gas
                buzzer.start(50)  # Phát âm thanh báo động
                #await send_gas_alert()  # Gửi cảnh báo lên bot Telegram
            else:
                buzzer.stop()  # Dừng âm thanh báo động nếu không phát hiện khí gas

            
        await asyncio.sleep(1)  # Kiểm tra cảm biến mỗi giây

def controlServo(motion):
    if motion == 1:
        # Quay servo đến 90 độ
        servo.ChangeDutyCycle(angle_to_duty_cycle(120))  # Giá trị PWM tương ứng với góc 90 độ
    else:
        # Quay servo trở lại vị trí ban đầu (0 độ)
        servo.ChangeDutyCycle(angle_to_duty_cycle(0))  # Giá trị PWM tương ứng với góc 0 độ
    sleep(1)  # Chờ cho servo di chuyển
    servo.ChangeDutyCycle(0)  # Ngừng PWM để servo không bị rung

def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 180.0) * 10.0

def measure_distance():
    # Đảm bảo chân TRIG ở mức thấp
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    # Gửi xung siêu âm
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Đo thời gian xung phản hồi
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Tính khoảng cách
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    loop.create_task(main_loop())
    loop.run_forever()


