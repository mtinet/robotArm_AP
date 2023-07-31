#include <Servo.h>

Servo myServo;  // 서보모터 객체 생성

const int servoPin = 9;       // 서보모터를 연결한 디지털 핀 번호
const int sensorPin = A0;     // 센서를 연결한 아날로그 핀 번호

void setup() {
  myServo.attach(servoPin);  // 서보모터를 핀에 연결
}

void loop() {
  int sensorValue = analogRead(sensorPin);  // 센서값 읽기

  // 센서값을 서보모터의 동작 범위에 매핑. 
  // 아날로그 센서값은 0~1023 범위이며, 서보모터의 범위는 0~180도 입니다.
  int servoAngle = map(sensorValue, 0, 1023, 0, 180); 

  myServo.write(servoAngle);  // 매핑된 각도로 서보모터 제어
}
