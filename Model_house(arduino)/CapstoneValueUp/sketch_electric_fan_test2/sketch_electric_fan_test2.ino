#include <Servo.h>

Servo servo1;  

int angle = 0;
int fan=7;

void setup()
{
pinMode(fan,OUTPUT);
digitalWrite(fan,HIGH);
servo1.attach(9);

Serial.begin(9600); 

while (!Serial);

Serial.println("Input 1 to Turn On and 0 to Off");
}

void loop() 
{ 
    if(Serial.available())
  { 
    char a;
    a = Serial.read(); 
    
    if (a == '1')
    {
      
      for(int cnt =0; cnt<=5; cnt++)
        if(cnt<5){
          for(angle = 0; angle < 1; angle++) 
  { 
      digitalWrite(fan,LOW);
      
    Serial.println("Command completed turned On");
    
    servo1.write(angle); 
    
    delay(15); 
  }

  for(angle = 120; angle > 0; angle--) 
  { 
    servo1.write(angle); 
   
    delay(15);     
  }
        }
        

    }
    else if (a =='0')
{
   digitalWrite(fan,HIGH);//반대로 넣어줘야함
 
  Serial.println("Command completed turned Off");
  
  servo1.write(angle);
  
}
  }
  }
