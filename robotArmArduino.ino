#include  <Servo.h>


// Create servo objects 
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

// Create names to the analog input pins 
int pin0 = A0;
int pin1 = A1;
int pin2 = A2;
int pin3 = A3;

// Setup of angle variables we have to use further down in the program 
int angle1;
int angle2;
int angle3;
int angle4;

// Setup of value variables we have to use further down in the program 
int value1;
int value2;
int value3;
int value4;

// Setup of limit values 
long int forservo1 = 20000;
long int forservo2 = 20000;
long int forservo3 = 20000;
long int forservo4 = 20000;

void setup() 
{ 
  Serial.begin(9600);   //시리얼모니터 
  pinMode(3, INPUT); /* Use button on thumbstick to set pin 3 as input */
  pinMode(4, OUTPUT); /* Set pin 4 as output to the magnet */

  // Attaches the servo on pins to the servo objects 
  servo1.attach(5);
  servo2.attach(3);
  servo3.attach(6);
  servo4.attach(9);
  Serial.println("meArm with Joystick");
} 
 
void loop() 
{ 
  // read analog values from joysticks 
  value1 = analogRead(pin0);
  value2 = analogRead(pin1);
  value3 = analogRead(pin2);
  value4 = analogRead(pin3);
  
//  시리얼 출력을 하게 되면 로봇팔 움직임이 느려집니다. 
//  Serial.print("value1 : ");
//  Serial.print(value1);
//  Serial.print(" | value2 : ");
//  Serial.print(value2);
//  Serial.print(" | value3 : ");
//  Serial.print(value3);
//  Serial.print(" | value4 : ");
//  Serial.println(value4);
  
  
  // 10 bit value is too big, so we change the scale from 0 - 1023 proportionately to 1 - 29 
  value1 = map(value1, 0, 1023, 1, 29);
  value2 = map(value2, 0, 1023, 1, 29);
  value3 = map(value3, 0, 1023, 1, 29);
  value4 = map(value4, 0, 1023, 1, 29);
  
  // it needs correction of positions, because joysticks are not very precise to stay exactly in the center  
  if(value1  <= 17 && value1 >= 13) // if value1 if between 13-17, then it's equal to 15 */
      value1 = 15;
  if(value2  <= 17 && value2 >= 13)
      value2 = 15;
  if(value3  <= 17 && value3 >= 13)
      value3 = 15;
  if(value4  <= 17 && value4 >= 13)
      value4 = 15;
    
  // Change initial value 'forservo' which is used to turn servo slower. This value has got very big scale.
  // We add or substract (depends on turning direction) difference between analog value and center from 'forservo'  
  forservo1 = forservo1 - (value1 - 15);
  forservo2 = forservo2 - (value2 - 15);
  forservo3 = forservo3 + (value3 - 15);
  forservo4 = forservo4 + (value4 - 15);
  
  // this part do not let variables 'forservo' go out of the limits 
  if(forservo1  < 1) // if forservo1 is less than 1, then it's equal to 1 
      forservo1 = 1;
  if(forservo1  > 20000) // if forservo1 is greater than 20000, then it's equal to 20000 
      forservo1 = 20000;
  if(forservo2  < 1) 
      forservo2 = 1;
  if(forservo2  > 20000)
      forservo2 = 20000; 
  if(forservo3  < 1) 
      forservo3 = 1;
  if(forservo3  > 20000)
      forservo3 = 20000;
  if(forservo4  < 1)
      forservo4 = 1;
  if(forservo4  > 20000)
      forservo4 = 20000;
  
  // change used value to angle of servo. Angles are adjusted during testing 
  angle1 = map(forservo1, 1, 20000, 170, 10);
  angle2 = map(forservo2, 1, 20000, 170, 10);
  angle3 = map(forservo3, 1, 20000, 170, 10); 
  angle4 = map(forservo4, 1, 20000, 170, 10);
  
  // send angles to servos 
  servo1.write(angle1);
  servo2.write(angle2);
  servo3.write(angle3);
  servo4.write(angle4);

  // activates the magnet
//  while (digitalRead(3) == HIGH) { /* Read pin 3 from the thumbstick */
//    digitalWrite(4, HIGH); /* Write to pin 4 (magnet) */
//  }

}
