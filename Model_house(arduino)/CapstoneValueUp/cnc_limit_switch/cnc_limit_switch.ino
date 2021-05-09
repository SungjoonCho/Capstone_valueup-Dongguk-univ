

/* 라이브러리 include */
#include <HCMotor.h>


/* 모터드라이버 연결핀 */
#define DIR_PIN 8 //스텝모터드라이버 DIR 연결핀
#define CLK_PIN 9 //스텝모터드라이버 CLK 연결핀
/* 리미트스위치 연결핀 */
#define LLIMITPIN 3
#define RLIMITPIN 2

/* HCMotor 라이브러리 인스턴스 생성 */
HCMotor HCMotor;

int Speed = 10;

void setup() 
{
  /* 라이브러리 초기화 */
  HCMotor.Init();

  /* 모터0을 스텝모터로 설정하고 연결된 핀을 지정 */
  HCMotor.attach(0, STEPPER, CLK_PIN, DIR_PIN);

  /* 모터를 연속동작모드로 설정*/
  HCMotor.Steps(0,CONTINUOUS);
  /* 속도설정 */
  HCMotor.DutyCycle(0, Speed);
  
  pinMode(LLIMITPIN, INPUT); 
  pinMode(RLIMITPIN, INPUT); 
  Serial.begin(9600); // (9600)의 통신속도로 통신을 시작합니다.
  
}

void loop() {
  if(Serial.available()>0)
 {
  char a;
  a = Serial.read();
  if(a =='1')
{
  /* 왼쪽 리미트스위치가 감지되면 정방향, 오른쪽 리미트스위치가 감지되면 역방향 */
  (digitalRead(LLIMITPIN) == HIGH);
    HCMotor.Direction(0, FORWARD);
     if (digitalRead(RLIMITPIN) == LOW)
    HCMotor.Direction(0, REVERSE);
}
  else if(a =='0')
{
    HCMotor.Direction(0, 0);
}
 }
}
  
