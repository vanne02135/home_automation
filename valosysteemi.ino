#include <LiquidCrystal.h>

const int temperaturePin = 0;

 LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

void setup() {
  // put your setup code here, to run once:
  int i; 
  for (i = 8; i < 14; i++) 
    pinMode(i, OUTPUT);

  lcd.begin(16, 2);

  lcd.clear();

  lcd.print("It is ALIVE!");


 Serial.begin(9600);

}

void loop() {

  float temperature = voltageToC(getVoltage(temperaturePin));
  Serial.print(temperature);  
  Serial.print("  deg C\n");
  ledDisplay(temperature); 
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print(temperature); 
  
  lcd.setCursor(6, 1); 
  lcd.print("astetta");
  
  lcd.setCursor(0, 0); 
  lcd.print("Lampomittari"); 
  delay(100); 
  
  //ledikikka();

}

void ledDisplay(float temp) {
 // map 23 - 30 to leds on pins 8-13. 13 is the coolest. 
  int i; 
  for (i = 8; i < 14; i++) { 
    digitalWrite(i, LOW); 
  }

  if (temp < 23  ) return;
  if (temp > 23  ) digitalWrite(13, HIGH); 
  if (temp > 24.5) digitalWrite(12, HIGH); 
  if (temp > 26  ) digitalWrite(11, HIGH); 
  if (temp > 27.5) digitalWrite(10, HIGH); 
  if (temp > 29  ) digitalWrite(9, HIGH); 
  if (temp > 31.5) digitalWrite(8, HIGH); 

}

float voltageToC(float U) {

  return (U - 0.5) * 100.0;
}

float getVoltage(int pin)
{
  // This function has one input parameter, the analog pin number
  // to read. You might notice that this function does not have
  // "void" in front of it; this is because it returns a floating-
  // point value, which is the true voltage on that pin (0 to 5V).

  return (analogRead(pin) * 0.004882814);

  // This equation converts the 0 to 1023 value that analogRead()
  // returns, into a 0.0 to 5.0 value that is the true voltage
  // being read at that pin.
}


void ledikikka() {
   int i; 
  for (i = 8; i < 14; i++) { 
    digitalWrite(i, HIGH); 
    delay(100); 
  }

  for (i = 8; i < 14; i++) { 
    digitalWrite(i, LOW); 
    delay(100); 
  }

int l = 0; 

 while (l++ < 10) {
  for (i = 8;i < 14; i++)
  {
   digitalWrite(i, HIGH); 
   delay(l*10);
   digitalWrite(i, LOW);  
  }

  for (i = 13;i>7; i--)
  {
   digitalWrite(i, HIGH); 
   delay(l*10);
   digitalWrite(i, LOW);  
  }
 }
 
}
