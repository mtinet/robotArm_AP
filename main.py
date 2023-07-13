from time import sleep
from machine import Pin, PWM
import socket
import network

# 접속을 위한 ssid, password 설정 
ssid = 'robotArm_AP'
password = '123456789'

led = machine.Pin("LED",machine.Pin.OUT)

# AP모드 설정
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
  pass

print('Ready to Connection')
print("Connect to the WiFi with the '" + ssid + "'")
print("Connection IP: " + ap.ifconfig()[0])
print()

# 소켓 접속을 위한 설정
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1) # AP 접속자 수를 1명으로 제한함 

# LED 상태를 OFF로 시작함
led.off()

# 서보 핀 설정
servos = [PWM(Pin(i)) for i in range(16, 20)]

# 서보 주파수 설정
for servo in servos:
    servo.freq(50)

# 각 서보의 현재 각도를 저장하는 리스트
current_angles = [90, 90, 90, 90]

# 각 버튼 클릭에 따른 각도 변화량
ANGLE_DELTA = 10

#Template HTML
html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=0.8">
    <title>IoT robotArm</title>
    <center><H1>IoT robotArm</h1></center>
    <style>
      /* 버튼 디자인 */
      .button {{
        border: none;
        color: white;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        background-color: #4CAF50;
        width: 120px;
        height: 60px;
        border-radius: 20%;
        box-shadow: 2px 2px 2px #888888;
      }}
      .button:hover {{
        background-color: #3e8e41;
      }}
      .container {{
        display: inline-block;
        text-align: center;
        padding: 20px;
        margin: 10px;
        background-color: #f1f1f1;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        border-radius: 20px;
      }}
  </style>
  </head>
  <body>
    <center>
      <div class="container">
        <form action="./up">
          <button class="button" type="submit">Up</button>
        </form>
        <br>
        <table>
          <tr>
            <td>
              <form action="./ccw">
                <button class="button" "submit">CCW</button>
              </form>
            </td>
            <td>
              <form action="./stopL">
                <button class="button" "submit">StopL</button>
              </form>
            </td>
            <td>
              <form action="./cw">
                <button class="button" type="submit">CW</button>
              </form>
            </td>
          </tr>
        </table>
        <br>
        <form action="./down">
          <button class="button" type="submit">Down</button>
        </form>
      </div>
      <div class="container">
        <form action="./forward">
          <button class="button" type="submit">Forward</button>
        </form>
        <br>
        <table>
          <tr>
            <td>
              <form action="./close">
                <button class="button" type="submit">Close</button>
              </form>
            </td>
            <td>
              <form action="./stopR">
                <button class="button" type="submit">StopR</button>
              </form>
            </td>
            <td>
              <form action="./open">
                <button class="button" type="submit">Open</button>
              </form>
            </td>
          </tr>
        </table>
        <br>
        <form action="./backward">
          <button class="button" type="submit")>Backward</button>
        </form>
      </div>
    </center>
  </body>
</html>
"""

# 각도를 설정하는 함수
def setAngle(servo, angle):
    if angle < 0:  # 각도가 0도보다 작으면 0도로 설정
        angle = 0
    elif angle > 180:  # 각도가 180도보다 크면 180도로 설정
        angle = 180
    a = int(((((angle) * 2)/ 180) + 0.5)/20 * 65535)
    servo.duty_u16(a)
    return angle

# 서보 각도를 웹서버로부터의 요청에 따라 설정
def set_servo_angle(servos, request):
    global current_angles
    if b'GET /open' in request:
        current_angles[0] = setAngle(servos[0], current_angles[0] + ANGLE_DELTA)
        print("open")
    elif b'GET /close' in request:
        current_angles[0] = setAngle(servos[0], current_angles[0] - ANGLE_DELTA)
        print("close")
    elif b'GET /up' in request:
        current_angles[1] = setAngle(servos[1], current_angles[1] - ANGLE_DELTA)
        print("up")
    elif b'GET /down' in request:
        current_angles[1] = setAngle(servos[1], current_angles[1] + ANGLE_DELTA)
        print("down")
    elif b'GET /forward' in request:
        current_angles[2] = setAngle(servos[2], current_angles[2] - ANGLE_DELTA)
        print("forward")
    elif b'GET /backward' in request:
        current_angles[2] = setAngle(servos[2], current_angles[2] + ANGLE_DELTA)
        print("backward")
    elif b'GET /cw' in request:
        current_angles[3] = setAngle(servos[3], current_angles[3] - ANGLE_DELTA)
        print("cw")
    elif b'GET /ccw' in request:
        current_angles[3] = setAngle(servos[3], current_angles[3] + ANGLE_DELTA)
        print("ccw")
    elif b'GET /stopL' in request:
        for i in [1, 3]:
            current_angles[i] = setAngle(servos[i], 90)
        print("stopL")
    elif b'GET /stopR' in request:
        for i in [0, 2]:
            current_angles[i] = setAngle(servos[i], 90)
        print("stopR")

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)
        led.on()
        set_servo_angle(servos, request)
        print(current_angles)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        led.off()

    except OSError as e:
        cl.close()
        print('connection closed')
        s.close()
