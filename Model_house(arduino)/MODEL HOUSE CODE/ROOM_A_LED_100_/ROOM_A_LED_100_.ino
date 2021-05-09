//A방 LED

#include "ESP8266.h"
#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h> //RGB Led 모듈

#define PIN            7

#define NUMPIXELS      6                             // 제어하고 싶은 LED 개수
                         
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS,PIN, NEO_GRB + NEO_KHZ800);

                         
#define SSID        "iptime_mst"  

#define PASSWORD    "0123456789"  

#define HOST_NAME   "192.168.0.11"  

#define HOST_PORT   (9009)

SoftwareSerial mySerial(2, 3); /* RX:2, TX:3 */
ESP8266 wifi(mySerial);


void printUsage()
{
    uint8_t buf[]="Usage\na : Turn On\nz : Turn Off\n";
    wifi.send(buf, strlen(buf));
}

bool isConnected = false;

void setup(void)
{
    Serial.begin(9600);
    Serial.print("setup begin\r\n");
    
    Serial.print("FW Version:");
    Serial.println(wifi.getVersion().c_str());
      
    if (wifi.setOprToStationSoftAP()) {
        Serial.print("to station + softap ok\r\n");
    } else {
        Serial.print("to station + softap err\r\n");
    }
 
    if (wifi.joinAP(SSID,PASSWORD)) {
        Serial.print("Join AP success\r\n");
        Serial.print("IP:");
        Serial.println( wifi.getLocalIP().c_str());       
    } else {
        Serial.print("Join AP failure\r\n");
    }
    
    if (wifi.disableMUX()) {
        Serial.print("single ok\r\n");
    } else {
        Serial.print("single err\r\n");
    }
    
    Serial.print("setup end\r\n");



    pinMode(7, OUTPUT);

}



void loop(void)
{
    if ( isConnected == false){
      
        while(1){
            if (wifi.createTCP(HOST_NAME, HOST_PORT)) {
                Serial.print("create tcp ok\r\n");
                isConnected = true;
                printUsage();
                break;
            } else {
                Serial.print("create tcp err\r\n");
            }
        }
    }
   
    uint8_t buffer[128] = {0};
    
    uint32_t len = wifi.recv(buffer, sizeof(buffer), 10000);
    if (len > 0) {
        Serial.print("Received:[");
        for(uint32_t i = 0; i < len; i++) {
            Serial.print((char)buffer[i]);
        }
        Serial.print("]\r\n");


        char command = buffer[0];
       
        

        switch (command){
        
            case 'a':
              
              if (command == 'a'){
                for(int i=0;i<NUMPIXELS;i++)
             {
                 pixels.setPixelColor(i, pixels.Color(0,150,0)); // Moderately bright green color.
 
                 pixels.show(); // This sends the updated pixel color to the hardware.
                
                sprintf(buffer, "Room A LED is on\n");
                wifi.send(buffer, strlen(buffer));
                delay(500);
             }
              }
              else{
                sprintf(buffer, "LED is already on\n");
                wifi.send(buffer, strlen(buffer));
              }
              break;
        
            case 'z':
            
              if (command == 'z'){
                for(int i=0;i<NUMPIXELS;i++)      
                {   
                pixels.setPixelColor(i, pixels.Color(0,0,0)); // led 6개 동시에(delay 없앴음) led off
    
                pixels.show(); // This sends the updated pixel color to the hardware.
  
                sprintf(buffer, "Smart Front Door System Turn off.\n");
                wifi.send(buffer, strlen(buffer));
              }
              }
              else{
                sprintf(buffer, "Smart Front Door System Turn off.\n");
                wifi.send(buffer, strlen(buffer));
              }
              break;
        
            case 'S':
            case 's':
                
             //if (ledStatus == LOW){
                //sprintf(buffer, "LED status: off\n");
                //wifi.send(buffer, strlen(buffer));
              //}
             // else {
                //sprintf(buffer, "LED status: on\n");
                //wifi.send(buffer, strlen(buffer));
            //  }
              break;
              
            default:

              break;
              
        }      
    }
}
