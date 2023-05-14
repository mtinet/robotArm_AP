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
    for angle in range(current_angle, target_angle + step, step):
        setAngle(servo, angle)
        current_angles[servo_num] = angle  # 현재 각도를 저장
        sleep(delay_time)
    current_angles[servo_num] = target_angle  # 최종 각도를 저장

# 각도 리스트를 받아서 로봇 암을 움직이는 함수
def move_all_servos(angles):
    for i in range(4):
        move_servo_slowly(servos[i], i, angles[i])
    sleep(0.1)
    
    
# 특정한 동작을 미리 설정
init = [85, 90, 90, 90]

centerOpenUp = [120, 120, 60, 90]
centerOpenDown = [120, 150, 30, 90]
centerGet = [85, 150, 30, 90]

centerCloseUp = [85, 120, 60, 90]
centerCloseDown = [85, 150, 30, 90]
centerPut = [120, 150, 30, 90]

rightOpenUp = [120, 120, 60, 45]
rightOpenDown = [120, 150, 30, 45]
rightGet = [85, 150, 30, 45]

rightCloseDown = [85, 150, 30, 45]
rightCloseUp = [85, 120, 60, 45]
rightPut = [120, 150, 30, 45]

leftOpenUp = [120, 120, 60, 135]
leftOpenDown = [120, 150, 30, 135]
leftGet = [85, 150, 30, 135]

leftCloseUp = [85, 120, 60, 135]
leftCloseDown = [85, 150, 30, 135]
leftPut = [120, 150, 30, 135]


# 각도초기화 
move_all_servos(init)
sleep(1)


# 반복동작 
while True:
    move_all_servos(centerOpenUp)
    move_all_servos(centerOpenDown)
    move_all_servos(centerGet)
    move_all_servos(centerCloseUp)

    move_all_servos(centerCloseDown)
    move_all_servos(centerPut)
    move_all_servos(centerOpenUp)
    sleep(1)
    
    move_all_servos(rightOpenUp)
    move_all_servos(rightOpenDown)
    move_all_servos(rightGet)
    move_all_servos(rightCloseUp)

    move_all_servos(rightCloseDown)
    move_all_servos(rightPut)
    move_all_servos(rightOpenUp)
    sleep(1)
    
    move_all_servos(leftOpenUp)
    move_all_servos(leftOpenDown)
    move_all_servos(leftGet)
    move_all_servos(leftCloseUp)

    move_all_servos(leftCloseDown)
    move_all_servos(leftPut)
    move_all_servos(leftOpenUp)
    sleep(1)

