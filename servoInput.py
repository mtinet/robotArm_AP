from time import sleep
from machine import Pin, PWM

# 서보 핀 설정
servos = [PWM(Pin(i)) for i in range(16, 20)]

# 서보 주파수 설정
for servo in servos:
    servo.freq(50)

# 각 서보의 현재 각도를 저장하는 리스트
current_angles = [90, 90, 90, 90]

# 서보 각도를 0~180도로 입력할 수 있도록 함수를 하나 만듬
def setAngle(servo, angle):
    if angle < 0:  # 각도가 0도보다 작으면 0도로 설정
        angle = 0
    elif angle > 180:  # 각도가 180도보다 크면 180도로 설정
        angle = 180
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)

# 천천히 움직이는 함수
def move_servo_slowly(servo, servo_num, target_angle, delay_time=0.01):
    current_angle = current_angles[servo_num]
    step = 1 if target_angle > current_angle else -1
    for angle in range(current_angle, target_angle, step):
        setAngle(servo, angle)
        current_angles[servo_num] = angle  # 현재 각도를 저장
        sleep(delay_time)
    setAngle(servo, target_angle)  # 마지막으로 목표 각도로 정확하게 맞춤
    current_angles[servo_num] = target_angle  # 최종 각도를 저장

# 반복동작 
while True:
    servo_num = int(input("Enter servo number (0-3): "))
    target_angle = int(input("Enter target angle (0-180): "))
    move_servo_slowly(servos[servo_num], servo_num, target_angle)
    sleep(1)
