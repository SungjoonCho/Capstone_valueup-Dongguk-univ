int fan=7;

void setup()
{
pinMode(fan,OUTPUT);
digitalWrite(fan,LOW);


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
      
      
      digitalWrite(fan,HIGH);
      
    Serial.println("Command completed turned On");
    
   
    
     
  }

 
    else if (a =='0')
{
   digitalWrite(fan,LOW);//반대로 넣어줘야함
 
  Serial.println("Command completed turned Off");
  
 
}
  }
  }
