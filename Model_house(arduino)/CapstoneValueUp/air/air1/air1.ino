int air=7;

void setup() {
  pinMode(air,OUTPUT);
  Serial.begin(9600);
}

void loop() {
    if(Serial.available()>0)
 {
  char a;
  a = Serial.read();
  if(a =='1')
  {
  digitalWrite(air,HIGH);
  Serial.println("on");//시리얼 모니터에 "1"신호 들어오면 on이라 뜸
  }

  else if(a =='0')
  {
  digitalWrite(air,LOW);
  Serial.println("off");//시리얼 모니터에 "0"신호 들어오면 off라 뜸    
  }
}
}
