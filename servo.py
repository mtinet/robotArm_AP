from time import sleep
from machine import Pin, PWM

# 서보 핀, 주파수 설정
servo = PWM(Pin(0))
servo.freq(50)

# 서보 각도를 0~180도로 입력할 수 있도록 함수를 하나 만듬
def setAngle(servoName, angle):
    servo = servoName
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)
    
# 반복동작 
while True:
    setAngle(servo,30)
    sleep(1)
    setAngle(servo,60)
    sleep(1)
    setAngle(servo,95)
    sleep(1)





