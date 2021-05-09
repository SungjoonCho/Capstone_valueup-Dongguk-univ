#include <Servo.h>

Servo servo1;  

int fan=6;

void setup()
{
pinMode(fan,OUTPUT);

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
      digitalWrite(fan,LOW);
      
    Serial.println("Command completed turned On");
        
    delay(15); 
  }

  
                    
    else if (a =='0')
    
{
   digitalWrite(fan,HIGH);//반대로 넣어줘야함
 
  Serial.println("Command completed turned Off");
   
}
  }
  }
  
