#include <Ultrasonic.h>

#define pino_trigger_1 D7
#define pino_echo_1 D8

#define pino_trigger_2 D1 
#define pino_echo_2 D2
 
Ultrasonic ultrasonic_1(pino_trigger_1, pino_echo_1);
Ultrasonic ultrasonic_2(pino_trigger_2, pino_echo_2);
float cm1,cm2;
 
void setup()
{
  Serial.begin(115200);
  Serial.println("Lendo dados do sensor...");
}
 
void loop()
{
   
  
  long microsec1 = ultrasonic_1.timing();
  long microsec2 = ultrasonic_2.timing();
  cm1 = ultrasonic_1.convert(microsec1, Ultrasonic::CM);
  cm2 = ultrasonic_2.convert(microsec2, Ultrasonic::CM);
   
  Serial.print(cm1);
  Serial.print("| ");
  Serial.print(cm2);

  
  
  delay(200);
}
