/* 라이브러리 include */
#include <HCMotor.h>

/* HCMotor 라이브러리 인스턴스 생성 */
HCMotor HCMotor;
// 핀번호 정하기
const int stepPin = 5; 
const int dirPin = 2; 
const int enPin = 8;
void setup() {
  
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);

  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);

  Serial.begin(9600); // (9600)의 통신속도로 통신을 시작합니다.
}
void loop() {
   if(Serial.available()>0)
 {
  char a;
  a = Serial.read();
  if(a =='1')
  {
  digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 800; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(500); 
  }
  delay(5000); // 5초 딜레이
  }
  else if(a =='0')
  {
  digitalWrite(dirPin,LOW); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 800; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(500);
  }
  delay(5000); // 5초 딜레이
  }
 }
}
