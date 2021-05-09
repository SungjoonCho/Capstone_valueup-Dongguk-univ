#include <Adafruit_NeoPixel.h>
#define PIN            7
#define PIN2           8
#define NUMPIXELS      6                             // 제어하고 싶은 LED 개수
#define NUMPIXELS2     2                             // 제어하고 싶은 LED 개수
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS,PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels2 = Adafruit_NeoPixel(NUMPIXELS2,PIN2, NEO_GRB + NEO_KHZ800);

void setup() {

  pixels.begin(); // This initializes the NeoPixel library.
  pixels2.begin(); // This initializes the NeoPixel library.
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
     for(int i=0;i<NUMPIXELS2;i++)
    {
   
    pixels.setPixelColor(i, pixels.Color(0,150,0)); // Moderately bright green color.
 
    pixels.show(); // This sends the updated pixel color to the hardware.

    pixels2.setPixelColor(i, pixels2.Color(0,150,0)); // Moderately bright green color.
 
    pixels2.show(); // This sends the updated pixel color to the hardware.
    
    Serial.println("led on!!");
    delay(500);
  }
  }
  else if(a =='0')
  {
     for(int i=0;i<NUMPIXELS;i++)
      for(int i=0;i<NUMPIXELS2;i++)
     {   
    pixels.setPixelColor(i, pixels.Color(0,0,0)); // led 6개 동시에(delay 없앴음) led off
    
    pixels.show(); // This sends the updated pixel color to the hardware.
    
    pixels2.setPixelColor(i, pixels2.Color(0,0,0)); // led 2개 동시에(delay 없앴음) led off
    
    pixels2.show(); // This sends the updated pixel color to the hardware.
    Serial.println("led off!!");    
     }
  } 
 }
}
