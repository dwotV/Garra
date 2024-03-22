#include "SoftWire.h"
#include "Ultrasound.h"
#include "SoftwareSerial.h"
#include "Adafruit_APDS9960.h"
#include <U8g2lib.h>
#include <string.h>

//Distance
Ultrasound ultrasound;  //Instantiate the ultrasonic class

float distance;
int i;                //Current data location
uint16_t R;
uint16_t G;
uint16_t B;
uint8_t dis;

//Color
SoftWire sw(6,7);   //sda,scl
Adafruit_APDS9960 apds=Adafruit_APDS9960(sw);
U8G2_SSD1306_128X64_NONAME_1_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

#define RED   1
#define GREEN 2
#define BLUE  3
#define WHITE 4

int R_F = 13000;
int G_F = 19000;
int B_F = 25000;
int r_f = 768;
int g_f = 1024;
int b_f = 1280;

//Touch
#define LED  13
#define TOUCH 12  


//Presence

#define IR1 2
#define IR2 4
#define IR3 10

#define IRACTIONGROUP_LEFT    18
#define IRACTIONGROUP_CENTER  17
#define IRACTIONGROUP_RIGHT   16


// Sound

#define RxPin 8   //Define soft serial port
#define TxPin 9
#define SOUND A0

#define MAXVOL 8

uint8_t result;
uint8_t volume;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  //Inicia Touch
  pinMode(LED, OUTPUT);
  pinMode(TOUCH, INPUT);
  digitalWrite(LED, LOW);

  //color
  if(!apds.begin()){
    Serial.println("failed to initialize device! Please check your wiring.");
  }
  else Serial.println("Device initialized!");

  //enable color sensign mode
  apds.enableColor(true);

  //Display logo
  u8g2.begin();
  u8g2.setDisplayRotation(U8G2_R2);
  u8g2.setFont(u8g2_font_fub20_tr);
  u8g2.firstPage();
  do {
    u8g2.setCursor(0, 38);
    u8g2.print(" HOLA");
  } while ( u8g2.nextPage() );

  //Set the functions of each IO port
  pinMode(IR1, INPUT);  // Senor 1 left
  pinMode(IR2, INPUT);  // Senor 2 center
  pinMode(IR3, INPUT);  // Senor 3 right
  dis='1';

  // Sound
  pinMode(LED, OUTPUT);
  pinMode(SOUND, INPUT);

  delay(3000);
}


//Check whether each sensor detects the object. If the object is detected, the robotic arm will run the corresponding action group
String presenceDetect(bool imp)
{
  static uint32_t timer;
  String d="0,0,0";
    if (digitalRead(IR1) == LOW)
    {
      timer = millis() + 500;
      d[0]='1'; // left sensor
    }
    if (digitalRead(IR2) == LOW)
    {
      timer = millis() + 500;
      d[2]='1'; //center sensor
    }
    if (digitalRead(IR3) == LOW)
    {
      timer = millis() + 500;
      d[4]= '1'; //right sensor
    }
  if(imp) Serial.print(d);
  return d;
}


void drawPresence() {
  static uint32_t timer;
  if (timer < millis())
  {
    timer = millis() + 50;
    u8g2.clearBuffer();  //About clearBuffer https://github.com/olikraus/u8g2/wiki/u8g2reference#clearbuffer
    u8g2.firstPage();
    do {
      u8g2.drawEllipse(15, 20, 15, 20, U8G2_DRAW_ALL); 
      u8g2.drawEllipse(63, 20, 15, 20, U8G2_DRAW_ALL);
      u8g2.drawEllipse(112, 20, 15, 20, U8G2_DRAW_ALL);
      if (digitalRead(IR1) == LOW)
      {
        u8g2.drawFilledEllipse(15, 20, 10, 15, U8G2_DRAW_ALL); 
      }
      if (digitalRead(IR2) == LOW)
      {
        u8g2.drawFilledEllipse(63, 20, 10, 15, U8G2_DRAW_ALL);
      }
      if (digitalRead(IR3) == LOW)
      {
        u8g2.drawFilledEllipse(112, 20, 10, 15, U8G2_DRAW_ALL);
      }
    } while ( u8g2.nextPage());
  }
}


int colorDetect(bool imp)
{
  uint16_t r, g, b, c;
  int t;
  //wait for color data to be ready
  while(!apds.colorDataReady()){
    delay(5);
  }
  apds.getColorData(&r, &g, &b, &c);

  r = map(r, r_f, R_F, 0, 255);  
  g = map(g, g_f, G_F, 0, 255);
  b = map(b, b_f, B_F, 0, 255);
  //Serial.print(r); Serial.print(" ");  Serial.print(g); Serial.print(" ");  Serial.print(b); Serial.println(" ");
  
  //Find the largest value in R, G, B. For example, the maximum is R means that the object is Red
  if (r > g)
    t = RED;
  else
    t = GREEN;
  if (t == GREEN && g < b)
    t = BLUE;
  if (t == RED && r < b)
    t = BLUE;
  if(imp){
    Serial.print(r); Serial.print(",");   //Serial print and detects rgb value
    Serial.print(g); Serial.print(",");
    Serial.print(b);
    Serial.print("@");
  }

  //Returns the color only if the RGB value is greater than 30, otherwise returns 0
  if(t == BLUE && b > 80)
    return t;
  else if(t == GREEN && g > 80)
    return t;
  else if(t == RED && r > 80)         //If the robot color is recognized as red, set the judgment value of "r"in this line to be slightly larger than the r value printed by the serial port above
    return t;
  else 
    return 0;
  return 0;
}

//Draw screen image
void drawColor(int t)
{
  u8g2.firstPage();
  do
  {
    u8g2.setFont(u8g2_font_courB24_tf);
    u8g2.setCursor(0, 38);
    //Display color
    if (t == RED){
      u8g2.print(" RED");
    }
    if (t == BLUE){
      u8g2.print(" BLUE");
    }
    if (t == GREEN){
      u8g2.print(" GREEN");
    }
  } while ( u8g2.nextPage());
}

//Touch
void touchDetect(bool imp){
  if (!digitalRead(TOUCH))
  {//Detection touch sensor
    digitalWrite(LED, HIGH);
    delay(80);
    if (digitalRead(TOUCH))
    {//If it is short press once
      digitalWrite(LED, LOW);
      if(imp) Serial.print("1@");
    }
    else{
      delay(420);
      digitalWrite(LED, LOW);
      if(imp) Serial.print("2@");
    }
  }
  else{
    if(imp) Serial.print("0@");
  }
}

//Distance
void getDistance(bool imp) 
 {
    distance = ((float)ultrasound.GetDistance())/10;
    if(imp){
      Serial.print(distance);
      Serial.print('@');
    }
  }

void rainbow_color()          //Gradient rainbow light
{ 
  static uint32_t color_timer;
  if(color_timer < millis())
  {  
      color_timer = millis()+120;
      if(i<33&&i>=0){
          R=255;
          G=7.65*i;
          B=0;
      }else if(i<50&&i>=33){
          R=750-15*i;
          G=255;
          B=0;
      }else if(i<=66&&i>=50){
          R=0;
          G=255;
          B=15*i-750;
      }else if(i<=83&&i>66){
          R=0;
          G=1250-15*i;
          B=255;
      }else if(i<=100&&i>83){
          R=9*i-750;
          G=0;
          B=255;
      }else{
          R=5*i-350;
          G=0;
          B=1500-12.5*i;
        }
      i++;
      if(i>120)
      i=0;
      ultrasound.Color(R, G, B, R, G, B);
     }    
 }
  
void drawDistance() {
  static uint32_t timer;
  if (timer < millis())
  {
    timer = millis() + 500;
    u8g2.firstPage();
    do {
      if(distance>0)
        {
          u8g2.setFont(u8g2_font_courB24_tf);
          u8g2.setCursor(0, 38);
          if(distance >= 0 && distance < 10)
            u8g2.print(" ");
          if(distance < 100)
            u8g2.print(distance, 1); 
          else
           {
            int dis=distance;
            u8g2.print(" ");
            u8g2.print(dis, 1);
           }
          u8g2.setCursor(90, 38);
          u8g2.setFont(u8g2_font_fub17_tr);
          u8g2.println("cm");
        }
       else
        {
          u8g2.setFont(u8g2_font_fub17_tr);
          u8g2.setCursor(5, 38);
          u8g2.println("over range");
        }
    } while ( u8g2.nextPage());
  }
}

void runDistance()
{
  static uint32_t timer;
  if (timer < millis())
  {
      if (distance > 12 && distance < 14)
        ultrasound.Color(0, 255, 0, 0, 255, 0); //Green
      else if (distance > 5 && distance < 7)
        ultrasound.Color(255, 0, 0, 255, 0, 0); //Red
      else if (distance > 19 && distance < 21)
        ultrasound.Color(0, 0, 255, 0, 0, 255); //Blue
      else
      {
      }
      timer = millis() + 250;
    }
    
}


uint8_t AdcChange(uint16_t x)
{
  volume = map(x, 0, 1023, 0, 100);   //The maxi volume is 100, the min is 0, and the middle one corresponds to each other
  return volume;
}

void SoundDetect(bool imp)
{
  static uint32_t timer;
  static uint8_t step;
  static uint16_t count;

    /*switch (step)
    {
      case 0:
        if (AdcChange(analogRead(SOUND)) > MAXVOL)    //Sound is detected and counting starts
        {
          result++;
          count = 0;
          step = 1;   //Turn to step 1 next time, that is,check again
          timer = millis() + 200;   //Truning step 1, 200ms delay
        }
        break;

      case 1:
        if (AdcChange(analogRead(SOUND)) > MAXVOL)    //If sound is detected again after 200ms,add 1 to the original count
        {                                         //If no sound is detected within 500ms, the count will not increase, and will return to 0 after a period of time
          result++;
          count = 0;
          timer = millis() + 200;
        }
        else
        {
          count++;
          if (count > 500)
          {
            //step = 2;
            // RETURN ==================
            count = 0;
            result=0;
            // RETURN ==================
          }
          else
          {
            timer = millis() + 1;
            
          }
        }
        break;
      default:
        result = 0;
        count = 0;
        step = 0;
        break;
    }*/
    if (AdcChange(analogRead(SOUND)) > MAXVOL)    //Sound is detected and counting starts
        {
          result++;
        }
  //Serial.print(AdcChange(analogRead(SOUND)));
  if(imp){
    Serial.print(result);
    Serial.print("@");
  }
  result=0;
}

void flash()
{
   if(AdcChange(analogRead(SOUND)) > MAXVOL)
     digitalWrite(LED, HIGH);
   else
     digitalWrite(LED, LOW);
}



void loop() {
  int trb=Serial.read();
  if(trb!=-1){
    int incoming=Serial.read();
    if(incoming!=-1) dis=incoming;
    int t=colorDetect(true);
    SoundDetect(true);
    flash(); 
    touchDetect(true);  
    getDistance(true);
    runDistance();
    String activeSensor = presenceDetect(true);
    if(distance<5||(distance>7&&distance<12)||(distance>14&&distance<19)||distance>21)
      rainbow_color();
    if(dis=='1') drawColor(t);
    else if(dis=='4') drawDistance();
    else if(dis=='5') drawPresence();
    Serial.println("");
    //Serial.println(dis);
    //Serial.println(incoming);
  }
  else{
    int incoming=Serial.read();
    if(incoming!=-1 && incoming!='0') dis=incoming;
    int t=colorDetect(false);
    SoundDetect(false);
    flash(); 
    touchDetect(false);  
    getDistance(false);
    runDistance();
    String activeSensor = presenceDetect(false);
    if(distance<5||(distance>7&&distance<12)||(distance>14&&distance<19)||distance>21)
      rainbow_color();
    //Serial.println(t);
    //Serial.println(dis);
    if(dis=='1') drawColor(t);
    else if(dis=='4') drawDistance();
    else if(dis=='5') drawPresence();
    //Serial.println("");
    //Serial.println(dis);
    //Serial.println(incoming);
  }
  delay(200);
}
