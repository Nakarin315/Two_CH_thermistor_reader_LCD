#include <LiquidCrystal.h>
#include <stdio.h>


LiquidCrystal lcd(7,8,2,3,4,5);

void setup() {
  lcd.begin(8, 2);           // set up the LCD 16x2
  Serial.begin(115200);
}
void loop(){
  // Log data for channel 1
  if(Serial.available() > 0){
    char dummy = 0;
    //Empty serial buffer
    while(Serial.available() > 0){
      dummy = Serial.read();
    }
    float x=0.0;
    //Average 100 ADC measurements
    for(byte j=0; j<100; j++){
      x += analogRead(A0);
    }
    x /= 100.0;
    Serial.println(x);
  }

  double a, b ,c, d;
  float R25= 10000;
  int x1 = analogRead(A0);
  float V1 = 5.0*x1/1024;
  float Rt1 = R25*V1/(5 - V1);
  if (Rt1 >= 187 && Rt1 <= 681.6){
    a = 3.3536166E-03;
    b = 2.5377200E-04;
    c = 8.5433271E-07;
    d = -8.7912262E-08;
    }
  else if (Rt1 > 681.6 && Rt1 <= 3599){
    a = 3.3530481E-03;
    b = 2.5420230E-04;
    c = 1.1431163E-06;
    d = -6.9383563E-08;
    }
  else if (Rt1 > 3599 && Rt1 <= 32770){
    a = 3.3540170E-03;
    b = 2.5617244E-04;
    c = 2.1400943E-06;
    d = -7.2405219E-08;
    }
  else if(Rt1 > 32770 && Rt1 <= 692600){
    a = 3.3570420E-03;
    b = 2.5214848E-04;
    c = 3.3743283E-06;
    d = -6.4957311E-08;
    }
  double Tinv1 = a + b*log(Rt1/R25) + c*pow(log(Rt1/R25),2) + d*pow(log(Rt1/R25),3);
  float T1 = 1/Tinv1 - 273.15;
  if(T1<-50.0){
    lcd.setCursor(0, 0);
    lcd.print("T1:  NaN"); // print a message to the LCD
    }
  else{
    lcd.setCursor(0, 0);
    lcd.print("T1:"+ String(T1,1)+"C"); // print a message to the LCD
  }




  int x2 = analogRead(A1);
  float V2 = 5.0*x2/1024;
  float Rt2 = R25*V2/(5 - V2);
  if (Rt2 >= 187 && Rt2 <= 681.6){
    a = 3.3536166E-03;
    b = 2.5377200E-04;
    c = 8.5433271E-07;
    d = -8.7912262E-08;
    }
  else if (Rt2 > 681.6 && Rt2 <= 3599){
    a = 3.3530481E-03;
    b = 2.5420230E-04;
    c = 1.1431163E-06;
    d = -6.9383563E-08;
    }
  else if (Rt2 > 3599 && Rt2 <= 32770){
    a = 3.3540170E-03;
    b = 2.5617244E-04;
    c = 2.1400943E-06;
    d = -7.2405219E-08;
    }
  else if(Rt2 > 32770 && Rt2 <= 692600){
    a = 3.3570420E-03;
    b = 2.5214848E-04;
    c = 3.3743283E-06;
    d = -6.4957311E-08;
    }
  double Tinv2 = a + b*log(Rt2/R25) + c*pow(log(Rt2/R25),2) + d*pow(log(Rt2/R25),3);
  float T2 = 1/Tinv2 - 273.15;

  if(T2<-50.0){
    lcd.setCursor(0, 1);
    lcd.print("T2:  NaN"); // print a message to the LCD
    }
  else{
    lcd.setCursor(0, 1);
    lcd.print("T2:"+ String(T2,1)+"C"); // print a message to the LCD
  }
  delay(1000); // Delay the display for 1000 ms
}
