import socket
import network
import machine

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

# print('listening on', addr)
led.off()

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
                <button class="button" type="submit">CCW</button>
              </form>
            </td>
            <td>
              <form action="./stopL">
                <button class="button" type="submit">StopL</button>
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
          <button class="button" type="submit">Backward</button>
        </form>
      </div>
    </center>
  </body>
</html>
"""


# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        # print('client connected from', addr)
        
        request = cl.recv(1024)
        led.on()
        # print(request)
        
        if b'GET /up' in request:
            # forward 동작 수행
            print("Input Command: Up")
        elif b'GET /ccw' in request:
            # left 동작 수행
            print("Input Command: CCW")
        elif b'GET /stopL' in request:
            # right 동작 수행
            print("Input Command: StopL")
        elif b'GET /cw' in request:
            # stop 동작 수행
            print("Input Command: CW")
        elif b'GET /down' in request:
            # back 동작 수행
            print("Input Command: Down")
        elif b'GET /forward' in request:
            # back 동작 수행
            print("Input Command: Forward")
        elif b'GET /close' in request:
            # back 동작 수행
            print("Input Command: Close")
        elif b'GET /stopR' in request:
            # back 동작 수행
            print("Input Command: StopR")
        elif b'GET /open' in request:
            # back 동작 수행
            print("Input Command: Open")
        elif b'GET /backward' in request:
            # back 동작 수행
            print("Input Command: Backward")
            
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        led.off()

    except OSError as e:
        cl.close()
        print('connection closed')
        s.close()

