from time import sleep
from machine import Pin, PWM

# 서보 핀, 주파수 설정
servo0 = PWM(Pin(16))
servo0.freq(50)
servo1 = PWM(Pin(17))
servo1.freq(50)
servo2 = PWM(Pin(18))
servo2.freq(50)
servo3 = PWM(Pin(19))
servo3.freq(50)

# 서보 각도를 0~180도로 입력할 수 있도록 함수를 하나 만듬
def setAngle(servoName, angle):
    servo = servoName
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)
    
# 반복동작 
while True:
    setAngle(servo0, 120)
    setAngle(servo1, 90)
    setAngle(servo2, 60)
    setAngle(servo3, 60)


