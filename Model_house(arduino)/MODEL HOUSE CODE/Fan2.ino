//Electric Fan


#include <ESP8266WiFi.h>

int relay1 = 13;

const char* ssid     = "DGU-WIFI";
const char* password = "";

const char* host = "10.90.1.221";

void setup() {

  pinMode(relay1, OUTPUT);
  digitalWrite(relay1,HIGH); 
  Serial.begin(115200);
  delay(10);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
   delay(500);
   Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

int value = 0;

void loop() {

 Serial.print("connecting to ");
 Serial.println(host);
 // Use WiFiClient class to create TCP connections
 WiFiClient client;
 const int httpPort = 9009;
 if (!client.connect(host, httpPort)) {
  Serial.println("connection failed");
  return;
 }

 // We now create a URI for the request
 String url = "/";

 Serial.print("Requesting URL: ");
 Serial.println(url);

 // This will send the request to the server
 client.print(String("GET ") + url + " HTTP/1.1\r\n" +
           "Host: " + host + "\r\n");
 client.setTimeout(5);
             char a;
  char b;
  char c;
//Read all the lines of the reply from server and print them to Serial
 while(1){
  delay(2000);
  String stringone = client.readStringUntil('\r');
  Serial.print(stringone);

  a = stringone.compareTo("i");
  b = stringone.compareTo("j");
  c = stringone.compareTo("off");

  if (a == 0)
      {
        Serial.println("Command completed turned ON");
        digitalWrite(relay1,LOW);//LOW, HIGH 반대로 해줘야됨 ON은 LOW OFF는 HIGH
       
        
      }
      else if (b == 0)
      {
        Serial.println("Command completed turned Off");
        digitalWrite(relay1,HIGH);
       
          
      }
      else if (c == 0)
      {
        Serial.println("Command completed turned Off");
        digitalWrite(relay1,HIGH);
        
      }


  
 }

}
