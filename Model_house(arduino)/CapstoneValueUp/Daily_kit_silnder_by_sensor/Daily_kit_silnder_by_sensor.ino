
int motion=2;
int relay1=8;
int relay2=9;

void setup() {
  pinMode(motion, INPUT);
  pinMode(relay1,OUTPUT);
  pinMode(relay2,OUTPUT);
  
  Serial.begin(9600);
  
 //while (!Serial);
  
  //Serial.println("Input 1 to Turn on and 0 to off");
}

void loop()
{
    int sensor = digitalRead(motion);
    Serial.println(sensor);
    
      if (sensor == 1)
      {
        Serial.println("Command completed turned ON");
        digitalWrite(relay1,HIGH);
        digitalWrite(relay2,LOW);
        delay(10000);
        
      }
      else if (sensor == 0)
      {
        Serial.println("Command completed turned Off");
        digitalWrite(relay1,LOW);
        digitalWrite(relay2,HIGH);
        delay(10000);
          
      
    }
}
