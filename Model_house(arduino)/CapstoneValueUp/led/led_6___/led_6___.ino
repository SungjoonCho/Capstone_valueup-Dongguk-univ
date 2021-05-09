#include <Adafruit_NeoPixel.h>
#define PIN            7
#define NUMPIXELS      6                             // 제어하고 싶은 LED 개수
                         
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS,PIN, NEO_GRB + NEO_KHZ800);

void setup() {

  pixels.begin(); // This initializes the NeoPixel library.
  Serial.begin(9600); // (9600)의 통신속도로 통신을 시작합니다.

}
 
void loop() {
  if(Serial.available()>0)
 {
  char a;
  a = Serial.read();
  if(a =='1')
  {
    for(int i=0;i<NUMPIXELS;i++)
    {
   
    pixels.setPixelColor(i, pixels.Color(0,150,0)); // Moderately bright green color.
 
    pixels.show(); // This sends the updated pixel color to the hardware.
    
    Serial.println("led on!!");
    delay(500);
  }
  }
  else if(a =='0')
  {
     for(int i=0;i<NUMPIXELS;i++)      
     {   
    pixels.setPixelColor(i, pixels.Color(0,0,0)); // led 6개 동시에(delay 없앴음) led off
    
    pixels.show(); // This sends the updated pixel color to the hardware.
  
    Serial.println("led off!!");    
     }
  } 
 }
}
