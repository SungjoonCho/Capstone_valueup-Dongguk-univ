#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const char* ssid     = "DGU-GUEST";
const char* password = "";

const char* host = "10.90.1.221";

void setup() {
lcd.init();
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

  client.setTimeout(10);

  char a;
  char b;
  char c;          
 
//Read all the lines of the reply from server and print them to Serial
 while(1){
  delay(2000);
  String stringone = client.readStringUntil('\r');
  Serial.print(stringone);


  a = stringone.compareTo("k");
  b = stringone.compareTo("l");
  c = stringone.compareTo("off");

  if (a == 0)
      {
        Serial.println("Command completed turned ON");
        lcd.backlight();
        lcd.setCursor(0,0);
        lcd.print("Hello, MST!!");
        
      }
      else if ( b == 0)
        {
          Serial.println("Command completed turn OFF");
          lcd.clear();
          lcd.noBacklight();
        }
      else if ( c == 0)
        {
          Serial.println("Command completed turn OFF");
          lcd.clear();
          lcd.noBacklight();
        }
    


  
 }

}
