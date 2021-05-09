#include <Servo.h>

Servo servo1; 

long num;     
void setup()
{
servo1.attach(7);

Serial.begin(9600); 

while (!Serial);

Serial.println("Input 1 to Turn On and 0 to Off");
}

void loop() 
{ 
  if(Serial.available()>0)
  { 
    char a;
    a = Serial.read(); 
    
 if (a == '0')
{
  num= 25;   
  Serial.println("Command completed turned Off");

  servo1.write(num);
 
}

else if (a =='1')
{
  num= 0;   
  Serial.println("Command completed turned On");

  servo1.write(num);
  
}
  }
  }
