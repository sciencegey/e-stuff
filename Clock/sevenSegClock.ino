//Written by Samuel Knowles

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_LEDBackpack.h>
#include <RTClib.h>

#define aref_voltage      3.3
#define DISPLAY_ADDRESS   0x70

int tempPin = 0;  //analogue pin for the temperature sensor
int hours = 0;
int minutes = 0;
int seconds = 0;
int dayInt = 0;
int monthInt = 0;
int yearInt = 0;
int matrixTime = 0;
int dots = 0x0;
int low = 0; //brightness of clock at night
int high = 15; //brightness of clock during the day

volatile bool hzFlag = true;

bool blinkColon = false; 
bool twentyFourHour = false;
bool timeSense = false;
bool debug = false; //Turns debug mode on or off
bool b = true;

Adafruit_7segment matrix = Adafruit_7segment(); //Creates the object for the display (matrix)
RTC_DS3231 rtc;

void blankDisplay(){
  //sets all the digits on the display to nothing, turning it off
  matrix.writeDigitRaw(0,0x0);
  matrix.writeDigitRaw(1,0x0);
  matrix.writeDigitRaw(2,0x0);
  matrix.writeDigitRaw(3,0x0);
  matrix.writeDigitRaw(4,0x0);
  matrix.writeDisplay();
}

void setup() {
  // put your setup code here, to run once:
  matrix.begin(DISPLAY_ADDRESS);
  Serial.begin(9600);
  analogReference(EXTERNAL);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);   // LED on = initializing
  
  //set the clock
  rtc.begin();
  bool setClockTime = false;  //whether to set the time or not
  if (setClockTime) {
    if(debug){Serial.println("Setting DS3231 time!");}
    // This line sets the DS1307 time to the exact date and time the
    // sketch was compiled:
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // Alternatively you can set the RTC with an explicit date & time, 
    // for example to set January 21, 2014 at 3am you would uncomment:
    //RTC.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }

  // Enable 1 Hz square wave output from RTC.
  // RTC.writeSqwPinMode((Ds3231SqwPinMode)SquareWave1HZ); *should* handle
  // this, but for whatever reason is not, so fiddle registers directly...
   Wire.beginTransmission(0x68);
   Wire.write(0x0e);
   Wire.endTransmission();
   Wire.requestFrom(0x68, 1);
   uint8_t register0E = Wire.read();

   // clear bits 3 and 4 for 1Hz
   register0E &= ~(1 << 3);
   register0E &= ~(1 << 4);

   // put the value of the register back
   Wire.beginTransmission(0x68);
   Wire.write(0x0e);
   Wire.write(register0E);
   Wire.endTransmission();
  //rtc.writeSqwPinMode((Ds3231SqwPinMode)SquareWave1HZ);
  
  pinMode(2, INPUT_PULLUP); //RTC square-wave in
  pinMode(3, INPUT_PULLUP); //Function button
  pinMode(4, INPUT_PULLUP); //jumper for 24 hour time
  pinMode(5, INPUT_PULLUP); //jumper for time-sensitive display
  attachInterrupt(digitalPinToInterrupt(2), hzInt, RISING);
  digitalWrite(LED_BUILTIN, LOW); // LED off = successful init

  DateTime now = rtc.now();
  hours = now.hour();
  minutes = now.minute();
  blankDisplay();

  //sets the clock to 24 hour mode if the jumper is set
  if(digitalRead(4) == LOW){
    twentyFourHour = true;
  } else {
    twentyFourHour = false;
  }
  //turns off time-sensitive display if the jumper is set
  if(digitalRead(5) == LOW){
    timeSense = false;
  } else {
    timeSense = true;
  }
}

void hzInt(){
  //sets the hzFlag (so the arduino knows when to update)
  hzFlag = true;
}

void calcTemp(){
  //get the voltage from the temp pin
  int tempReading = analogRead(tempPin);
  
  //convert reading to voltage (3.3v)
  float voltage = tempReading * aref_voltage;
  voltage /= 1024.0;
  if(debug){Serial.print(voltage); Serial.println(" volts");}
  
  //converts voltage to temperature in C
  float tempC = (voltage - 0.5) * 100;  //converting from 10 mv per degree wit 500 mV offset to degrees ((voltage - 500mV) times 100)
  if(debug){Serial.print(tempC); Serial.println(" degrees C");}
  
  int tempDec = (tempC - (int)tempC + 0.005) * 100;  //Finds the numbers after the decimal point
  int tempRound = floor(tempC);  //floors the displayed temperature, and converts to an int
  if(debug){Serial.print(tempRound); Serial.println(" degrees C");}
  matrix.print((int)tempRound*100,DEC); //displays the temperature on the display, but moved over 2 digits
  if(debug){Serial.print(tempDec); Serial.println();}
  if (tempDec <= 50){
    matrix.writeDigitNum(3,0);
  } else {
    matrix.writeDigitNum(3,5);
  }
  matrix.writeDigitRaw(4,0x39);
  matrix.writeDigitRaw(2,0x12);
  matrix.writeDisplay();
}

void getDate(){
  DateTime now = rtc.now();
  yearInt = now.year();
  monthInt = now.month();
  dayInt = now.day();
  int digYear = 4;
  int digMonth = 4;
  int yearArray[4] = {0,0,0,0};
  int monthArray[4] = {0,0,0,0};
  int combiArray[8];
    
  Serial.print("Current date: ");
  Serial.print(yearInt, DEC);
  Serial.print('/');
  Serial.print(monthInt, DEC);
  Serial.print('/');
  Serial.print(dayInt, DEC);
  Serial.println(' ');
  
  //split each reading to an array
  //Year
  //Serial.println(yearInt);
  for(int i = digYear - 1; i >= 0; i--){
    //Serial.println(yearInt % 10);
    yearArray[i] = yearInt % 10;
    yearInt /= 10;
  }
  
  for(int i = 0; i < digYear; i++){
    Serial.print(yearArray[i]);
  }
  Serial.println();
  
  //Day
  //Serial.println(dayInt);
  for(int i = digMonth - 3; i >= 0; i--){
    //Serial.println(dayInt % 10);
    monthArray[i] = dayInt % 10;
    dayInt /= 10;
  }
  for(int i = 0; i < digMonth-2; i++){
    Serial.print(monthArray[i]);
  }
  Serial.println();
  
  //Month
  //Serial.println(monthInt);
  for(int i = digMonth - 1; i >= 2; i--){
    //Serial.println(monthInt % 10);
    monthArray[i] = monthInt % 10;
    monthInt /= 10;
  }
  for(int i = 0; i < digMonth; i++){
    Serial.print(monthArray[i]);
  }
  Serial.println();
  //writes each number to the display
  matrix.writeDigitNum(0,monthArray[0]);
  matrix.writeDigitNum(1,monthArray[1]);
  matrix.writeDigitNum(3,monthArray[2]);
  matrix.writeDigitNum(4,monthArray[3]);
  matrix.writeDigitRaw(2,0x4);
  matrix.writeDisplay();
  delay(2000);
  matrix.writeDigitNum(0,yearArray[0]);
  matrix.writeDigitNum(1,yearArray[1]);
  matrix.writeDigitNum(3,yearArray[2]);
  matrix.writeDigitNum(4,yearArray[3]);
  matrix.writeDigitRaw(2,0x8);
  matrix.writeDisplay();
  delay(2000);
}

void altDisplay(){
  //show the date
  getDate();
  
  //blank display
  matrix.print(10000, DEC);
  matrix.writeDigitRaw(2,0x0);
  matrix.writeDisplay();
  delay(1000);

  //show the temperature
  calcTemp();
  delay(5000);
}

void altTime(){
  for(int i; i < 20; i++){
    while(!hzFlag);
     DateTime now = rtc.now();
    
    if(minutes != now.minute()){
      minutes = now.minute();
    }

    if(hours != now.hour()){
      hours = now.hour();
    }
    matrixTime = hours*100 + minutes;
    if(!twentyFourHour){
      // Handle when hours are past 12 by subtracting 12 hours (1200 value).
      if (hours > 12) {
        matrixTime -= 1200;
      }
      // Handle hour 0 (midnight) being shown as 12.
      else if (hours == 0) {
        matrixTime += 1200;
      }
    }
    
    blinkColon = !blinkColon;
    if(blinkColon == true){
      dots = 0x2;
    } else {
      dots = 0x0;
    }
    
    matrix.print(matrixTime, DEC);
    
    if(!twentyFourHour){
      if (hours > 12){
        dots += 0x8;
        matrix.writeDigitRaw(2,dots);
      } else {
        dots += 0x4;
        matrix.writeDigitRaw(2,dots);
      }
    } else {
      matrix.writeDigitRaw(2,dots);
    }
    // Add zero padding when in 24 hour mode and it's midnight.
    // In this case the print function above won't have leading 0's
    // which can look confusing.  Go in and explicitly add these zeros.
    if (twentyFourHour && hours == 0) {
      // Pad hour 0.
      matrix.writeDigitNum(1, 0);
      // Also pad when the 10's minute is 0 and should be padded.
      if (minutes < 10) {
        matrix.writeDigitNum(2, 0);
      }
    }
    
    matrix.writeDisplay();
    hzFlag = false;
  }
}

void loop() {
  DateTime now = rtc.now();
  if(now.hour() < 22 && now.hour() >= 9 && timeSense == true){
    matrix.setBrightness(high);
    if (b = true){
      blankDisplay();
      b = false;
    }
    if (digitalRead(3) == LOW){
      altTime();
      altDisplay();
      blankDisplay();
    }
  } else {
    if(b = false){
      b = true;
    }
    if (now.hour() < 22 && now.hour() >= 9){
      matrix.setBrightness(high);
    } else {
      matrix.setBrightness(low);
    }
    if(hzFlag == true){
      DateTime now = rtc.now();
      
      if(minutes != now.minute()){
        minutes = now.minute();
      }
  
      if(hours != now.hour()){
        hours = now.hour();
      }
      matrixTime = hours*100 + minutes;
      if(!twentyFourHour){
        // Handle when hours are past 12 by subtracting 12 hours (1200 value).
        if (hours > 12) {
          matrixTime -= 1200;
        }
        // Handle hour 0 (midnight) being shown as 12.
        else if (hours == 0) {
          matrixTime += 1200;
        }
      }
      
      blinkColon = !blinkColon;
      if(blinkColon == true){
        dots = 0x2;
      } else {
        dots = 0x0;
      }
      
      matrix.print(matrixTime, DEC);
      
      if(!twentyFourHour){
        if (hours > 12){
          dots += 0x8;
          matrix.writeDigitRaw(2,dots);
        } else {
          dots += 0x4;
          matrix.writeDigitRaw(2,dots);
        }
      } else {
        matrix.writeDigitRaw(2,dots);
      }
      // Add zero padding when in 24 hour mode and it's midnight.
      // In this case the print function above won't have leading 0's
      // which can look confusing.  Go in and explicitly add these zeros.
      if (twentyFourHour && hours == 0) {
        // Pad hour 0.
        matrix.writeDigitNum(1, 0);
        // Also pad when the 10's minute is 0 and should be padded.
        if (minutes < 10) {
          matrix.writeDigitNum(2, 0);
        }
      }
      
      matrix.writeDisplay();
      hzFlag = false;
    }
    if (digitalRead(3) == LOW){
      altDisplay();
    }
  }
}
