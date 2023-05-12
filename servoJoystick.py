from time import sleep
from machine import Pin, PWM, ADC

# 서보 핀, 주파수 설정
servo0 = PWM(Pin(0))
servo0.freq(50)
servo1 = PWM(Pin(1))
servo1.freq(50)

# 아날로그 핀 설정
analog_pin0 = ADC(Pin(26))
analog_pin1 = ADC(Pin(27))

# 서보 각도를 0~180도로 입력할 수 있도록 함수를 하나 만듬
def setAngle(servoName, angle):
    servo = servoName
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)

# 각도를 계산하는 함수
def calculate_angle(analog_value):
    return int(((analog_value - 0) * (180 - 0)) / (65535 - 0) + 0)


# 반복동작
while True:
    analog_value0 = analog_pin0.read_u16()
    analog_value1 = analog_pin1.read_u16()
    
    angle0 = calculate_angle(analog_value0)
    angle1 = calculate_angle(analog_value1)
    
    setAngle(servo0, angle0)
    setAngle(servo1, angle1)
    
    print(angle0, angle1)
    sleep(0.1)
