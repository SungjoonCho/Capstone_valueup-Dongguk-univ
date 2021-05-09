#include <Servo.h>
Servo myservo;  

int pos=0;
int trig =6;
int echo =7;


void setup() {
  Serial.begin(9600);
  
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  myservo.attach(13);
  }
 int endangle = 90;
void loop()
{
   myservo.write(0); 
       for(pos = 0; pos < endangle; pos += 1)  
      {                                  // 이동할때 각도는 1도씩 이동합니다.  
        myservo.write(pos);              // 'pos'변수의 위치로 서보를 이동시킵니다. 
                                 
                                        } 
  
  digitalWrite(trig, LOW);
  digitalWrite(echo, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW); 

  unsigned long duration = pulseIn(echo, HIGH);
  float distance = duration / 29.0 / 2.0;
  
  Serial.print(distance);
  Serial.println("cm");   

  if (distance < 20) {
      myservo.write(0);
        for(pos = 0; pos < endangle; pos += 1)  
      {                                  // 이동할때 각도는 1도씩 이동합니다.  
        myservo.write(pos);              // 'pos'변수의 위치로 서보를 이동시킵니다. 
                                 
                                        } 
        Serial.println("1");
       
        delay(5000);
  }
        else(distnace>20){
          for(pos = endangle; pos>=0; pos-=1)     
       {                                 
         myservo.write(pos);              // 서보를 반대방향으로 이동합니다. 
         delay(15);                      
       }  
        Serial.println("0");
  }
  }

  
     
     
    }
