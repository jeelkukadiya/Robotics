#include<CytronMotorDriver.h>
#include<Servo.h>

//////////////////
#define lidarSerial Serial2


/////////////
int resetPin1 = 25;
int resetPin2 = 23;
int resetPin3 = 27;
int resetPin4 = 20;
int resetCondition1;
int resetCondition2;
int resetCondition3;
int resetCondition4; 

int distanceSilo[5] = {21, 96, 170, 240, 298};

int targetPosition = 90;

///////////////////////
const int trigPin = 38;
const int echoPin = 40;
const int trigPinR = 42;
const int echoPinR = 44;
const int trigPinS = 46;
const int echoPinS = 48;
// const int trigPinL = 50;       // Ultrasonic Backup
// const int echoPinL = 52;

/////////////////////
#define S0 22
#define S1 24
#define S2 26
#define S3 28
#define OUT 30

int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;

int ccwc=0;

struct RGB 
{
  int R;
  int G;
  int B;
};

float duration, distance;

long durR;
float distR;
long durL;
float distL;
long durS;
float distS;

int dR=0;
int dL=0;
int dS=0;

////////////////////
#define sovel 0.034

//////////////////////
#define PWM1 6
#define PWM2 7
#define PWM3 4
#define PWM4 5
#define MA1 29
#define MA2 31
#define MA3 33  
#define MA4 35

//////////////////
#define outputA1 2
#define outputB1 3

String sig;
int  a;
int i=0;
int STOP = 0;
int FORWARD = 130;
int BACKWARD = -130;
volatile int pos1 = 0;
volatile int pos2 = 0;
volatile int pos3 = 0;
volatile int pos4 = 0;

////////////////////////
CytronMD motor1(PWM_DIR, PWM1, MA1);
CytronMD motor2(PWM_DIR, PWM2, MA2);
CytronMD motor3(PWM_DIR, PWM3, MA3);
CytronMD motor4(PWM_DIR, PWM4, MA4);

///////////////////////
#define PWMball 43  
#define PWMinside 39
#define DIRball 41
#define DIRinside 37
///////////////////////////
CytronMD PickUpmotor(PWM_DIR, PWMball, DIRball);
CytronMD insidemotor(PWM_DIR, PWMinside, DIRinside);

int PickUpspeed = 255;

////////////////////////
#define IN1 45
#define IN2 47
#define IN3 49
#define IN4 51


int dis=30;
int coordX = 0;
int angleZ=0;
unsigned long timer = 0;
int flag=1;

//////////////////////////
#define  MAX_RANG (520)
#define  ADC_SOLUTION (1023.0)
int URM09Pin = A1;
float dist_t, URM_sense_t;

/////////////////
Servo Myservo;
// int Servopos = 0;


int c=0;
int h=0;
int siloW[5] = {0,0,0,0,0};
int q = 0;
int flagSilo = 0;

int kr=0;
int kp=0;


String lv;
int lc;
int lcl;
int lrv;

void setup() 
{
  Serial.begin(9600);
  
  lidarSerial.begin(115200);

  Myservo.attach(A0);
  Myservo.write(80);

  pinMode(trigPinR, OUTPUT); 
  pinMode(echoPinR, INPUT);
  // pinMode(trigPinL, OUTPUT); 
  // pinMode(echoPinL, INPUT);        // Ultrasonic Backup
  pinMode(trigPinS, OUTPUT); 
  pinMode(echoPinS, INPUT);
  pinMode(outputA1, INPUT);
  pinMode(outputB1, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(OUT, INPUT);

  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(resetPin1, INPUT_PULLUP);
  pinMode(resetPin2, INPUT_PULLUP);
  pinMode(resetPin3, INPUT_PULLUP);
  pinMode(resetPin4, INPUT_PULLUP);

  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN4,LOW);
  digitalWrite(IN3,LOW);
  attachInterrupt(digitalPinToInterrupt(outputA1), readencoder1, RISING);


  PickUpmotor.setSpeed(-PickUpspeed);

  //insidemotor.setSpeed(PickUpspeed);
  delay(2000);

  condition();

   if(resetCondition1 == 0)
  {
    // First Zone to third zone
       
      hardcode1();
       drop();
    PickUpmotor.setSpeed(PickUpspeed);
    insidemotor.setSpeed(PickUpspeed);
    
  }
  else if(resetCondition2 == 0 )
  {
     
            // First Zone to third zone
      hardcode2();
     
        drop();
       PickUpmotor.setSpeed(PickUpspeed);
       insidemotor.setSpeed(PickUpspeed);
        
  
  }
}

void condition()
{
  
  resetCondition1 = digitalRead(resetPin1);
  resetCondition2 = digitalRead(resetPin2);
  resetCondition3 = digitalRead(resetPin3);
  resetCondition4 = digitalRead(resetPin4);
}

void loop() 
{  

  flagSilo=0;

  dis=getDistance();
  //Serial.println(dis);
  if(dis < 15)
  {
    stop();
    delay(900);
    PickUpmotor.setSpeed(-PickUpspeed);
    MoveReverse(100);
    flag=1;
    delay(1000);
      
        //color_detect();
     ccwc=2;
    if(ccwc==2)
    {
      flag=0;
      PickUpmotor.setSpeed(-PickUpspeed);
    }
    else if(ccwc!=2)
    { 
      flag = 1;
      ServoOpen();
      PickUpmotor.setSpeed(PickUpspeed);
    } 
  }
     if (Serial.available() > 0) 
     {
        String data = Serial.readStringUntil('\n');
        int separatorIndex = data.indexOf(',');
        if (separatorIndex != -1) 
        {
            coordX = data.substring(0, separatorIndex).toInt();
            angleZ = data.substring(separatorIndex + 1).toInt();
        }
      if(flag==1)
      {
         Ball_tracking(coordX);
      }else if(flag==0)
      {
         placing_ball();
      }
     
    }
    
  
  siloDrop();// for silo border
  stop();
  delay(200);
  fillSilos();


  distLeft();
  // delay(120);
}


void hardcode1()
{
  MoveForward(2650);
  drop();
  delay(500);

  Rotaion(-90);
  delay(200);
  MoveForward(3740);
  delay(500);
  Rotaion(85);
  delay(200);
  MoveForward(3550);
  delay(500);
  Rotaion(90);
  delay(200);
  MoveForward(2800);
  delay(500);
  MoveReverse(800);
  stop();
  delay(500);
  PickUpmotor.setSpeed(PickUpspeed);
  insidemotor.setSpeed(PickUpspeed);
  delay(10);
}

void hardcode2()
{
  MoveLeft(200);
  drop();
  delay(500);
  MoveForward(720);
  delay(500);
  Rotaion(-90);
  delay(200);
  MoveForward(3740);
  delay(500);
  Rotaion(85);
  delay(200);
  MoveForward(3550);
  delay(500);
  Rotaion(90);
  delay(200);
  MoveForward(2800);
 
  
  stop();
  delay(500);
  PickUpmotor.setSpeed(PickUpspeed);
  insidemotor.setSpeed(PickUpspeed);
  delay(10);
}

int color_detect()
{
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);
  redFrequency = pulseIn(OUT, LOW);

  // Set sensor to read green
  digitalWrite(S2, HIGH);
  digitalWrite(S3, HIGH);
  greenFrequency = pulseIn(OUT, LOW);

  // Set sensor to read blue
  digitalWrite(S2, LOW);
  digitalWrite(S3, HIGH);
  blueFrequency = pulseIn(OUT, LOW);

  // Convert frequency to RGB values
  RGB color = { map(redFrequency, 0, 255, 0, 255), map(greenFrequency, 0, 255, 0, 255), map(blueFrequency, 0, 255, 0, 255) };

  if(color.R>90 && color.B<50 && color.G<110)        // Blue
  {
    return 2;
  }
  else if(color.R < 85)                                 // Red
  {
    return 3;
  }
  else if((color.R>70 && color.R<100) && color.B<100)  // Purple
  {
    return 1;
  }
  else
  {
    return 1;
  }
}

void Ball_tracking(int x) 
{
  int centerXMin = 280;
    int centerXMax = 360;
    int errorX = x - (centerXMin + centerXMax) / 2;
    float Kp = 0.5;  
    int speedX = Kp * abs(errorX);
    int maxSpeed = 50;
    speedX = min(speedX, maxSpeed);
    if (x > centerXMax && flag==1) {
         right(speedX);
    } else if (x < centerXMin && flag==1) {
       left(speedX);
    }else if(x < centerXMax && x > centerXMin && flag==1)
    {
        Forward(80); 
    }
    else
    {
    stop();
    }
}

int findNearestAvailableSilo(int dist) 
{
  int nearestIndex;
  int minDifference = INT8_MAX; // Initialize with a large value

  for (int i = 0; i < 5; i++) 
  {
    Serial.print("Checking Silo ");
    Serial.print(i);
    Serial.print(" - Status: ");
    Serial.print(siloW[i]);
    Serial.print(", Distance: ");
    Serial.println(distanceSilo[i]);

    if (siloW[i] == 0) // Only consider empty silos
    {
      int currentDifference = abs(dist - distanceSilo[i]);
      Serial.print("Silo ");
      Serial.print(i);
      Serial.print(" Distance: ");
      Serial.print(distanceSilo[i]);
      Serial.print(" Difference: ");
      Serial.println(currentDifference);

      if (currentDifference < minDifference) 
      {
        minDifference = currentDifference;
        nearestIndex = i;
      }
      Serial.print("new nearest index: ");
      Serial.println(nearestIndex);
    }
  }

  Serial.print("Nearest Available Silo: ");
  Serial.println(nearestIndex);
  return nearestIndex;
}

void fillSilos()
{
  while (flagSilo < 1)
  {
    int currentDist = distLeft();
    if (currentDist == -1)
    {
      Serial.println("No ball detected");
      delay(100);
      continue;
    }
    // Serial.println(currentDist);
    int nearestIndex = findNearestAvailableSilo(currentDist);
    if (nearestIndex == -1)
    {
      Serial.println("All silos are full.");
      break;
    }
    
    Serial.print("Aligning to Silo: ");
    Serial.println(nearestIndex);

    if (siloW[nearestIndex] == 0) 
    {
      allign(distanceSilo[nearestIndex]);
      siloDrop();
      delay(500);
        float UltrasonicDistance = Ultrasilo();
        Serial.println(UltrasonicDistance);
      if (UltrasonicDistance < 25) 
      {
        Serial.print("Silo ");
        Serial.print(nearestIndex);
        Serial.println(" is now full.");
        siloW[nearestIndex] = 1; // Mark the silo as filled
        MoveForward(160);
      } 
      else 
      {
        flagSilo = 1;
      }
    }
    delay(100);
  }

  siloDrop();
  bakward();
  delay(200);

  ServoOpen();
  delay(200);
  stop();

  MoveForward(400);
  stop();
  delay(4000);
  PickUpmotor.setSpeed(PickUpspeed);
}

// int findNearestAvailableSilo(int dist) 
// {
//   int nearestIndex = -1;
//   //int minDifference = INT8_MAX; 

//   // for (int i = 0; i < 5; ++i) 
//   // {
//     if (siloW[0] == 0 && 55>=dist && dist>=10) 
//     { nearestIndex =0;
//       // int currentDifference = abs(dist - distanceSilo[i]);
//       // if (currentDifference < minDifference) 
//       // {
//       //   minDifference = currentDifference;
//       //   nearestIndex = i;
//       // }
//     }else if(siloW[1] == 0 && 110>=dist && dist>=56)
//     {
//       nearestIndex =1;
//     }else if (siloW[2]==0 && 190>=dist && dist>=111)
//     {
//       nearestIndex =2;
//     }else if(siloW[3]==0 && 270>=dist && dist>=190)
//     {
//        nearestIndex =3;
//     }else if(siloW[4]==0 && 320>=dist && dist>=270)
//     {
//         nearestIndex =4;
//     }else{
//       nearestIndex =-1;
//     }
//   //}

//   return nearestIndex;
// }

// void fillSilos()
// {
//   // int nearestIndex;
//   while (flagSilo < 1)
//   {
//     int nearestIndex = findNearestAvailableSilo(distLeft());
//     if (nearestIndex == -1)
//     {
//       // Serial.println("All silos are full.");
//       break;
//     }
    
//     if (siloW[nearestIndex] == 0) 
//     {
//       allign(distanceSilo[nearestIndex]);
//       siloDrop();
//       delay(500);

//       if (Ultrasilo() < 25) 
//       {
//         siloW[nearestIndex] = 1;//Mark the silo as filled
//         MoveForward(160);
//       } 
//       else 
//       {
//         flagSilo = 1;
//       }
//     }
//   }

//   siloDrop();
//   bakward();
//   delay(200);

//   ServoOpen();
//   delay(200);
//   stop();

//   // if(nearestIndex==0)
//   // {
//   //   MoveRight(1400);
//   // }
//   // else if(nearestIndex==4)
//   // {
//   //   MoveLeft(1400);
//   // }

//   MoveForward(400);
//   stop();
//   delay(4000);
//   PickUpmotor.setSpeed(PickUpspeed);
// }


// int findNearestAvailableSilo(int dist) {
//     int nearestIndex = -1;
//     int minDifference = 1000; // a large enough number

//     for (int i = 0; i < 5; ++i) {
//         if (siloW[i] == 0) { // only consider empty silos
//             int currentDifference = abs(dist - distanceSilo[i]);
//             if (currentDifference < minDifference) {
//                 minDifference = currentDifference;
//                 nearestIndex = i;
//             }
//         }
//     }

//     return nearestIndex;
// }

// void fillSilos() {
//     while (flagSilo < 1) {
//         int nearestIndex = findNearestAvailableSilo(distLeft()); // Find the nearest available silo
//         if (nearestIndex == -1) {
//             // No available silos
//             Serial.println("All silos are full.");
//             break;
//         }
      
//         // Check if the nearest silo is not filled
//         if (siloW[nearestIndex] == 0) {
//             allign(distanceSilo[nearestIndex]); // Align to the nearest silo
//             siloDrop();
//             delay(500);

//             // Check if the silo is now full
//             if (Ultrasilo() < 25) {
//                 siloW[nearestIndex] = 1; // Mark the silo as filled
//                 MoveForward(160);
//             } else {
//                 flagSilo = 1;
//             }
//         } 
//     }

//     // Additional actions after filling the silos
//     siloDrop();
//     bakward();
//     delay(200);

//     ServoOpen();
//     delay(200);
//     stop();

//     MoveForward(400);
//     PickUpmotor.setSpeed(PickUpspeed);
// }


void siloDrop()
{
  while(distSilo()>10)
  {
    
    Backward(60);
    delay(20);
  }
  stop();
}


void silo()
{
  while(distSilo()>30)
  {
   
    Backward(60);
    delay(20);
  }
  stop(); 
}

void siloleft()
{
  while(distLeft()>28)
  {
    
    Leftsideway();
    delay(20);
  }
  stop(); 
}

void allign(int distAllign)
{
  while (true) 
  {
    int currentDist = distLeft();
    Serial.println(currentDist); 
    if (distAllign < currentDist) 
    {
      while (distLeft() > distAllign) 
      {
        
        Leftsideway();
        delay(10);
      }
      stop();
    } 
    else if (distAllign > currentDist) 
    {
      while (distLeft() < distAllign) 
      {
        
        rightsideway();
        delay(10);
      }
      stop();
    } 
    else 
    {
      stop();
    }

    currentDist = distLeft();
    if (abs(currentDist - distAllign) <= 3) 
    {
      break;
    }
  }
}


void placing_ball()
{
  flagSilo = 0;
  delay(300);
  Rotaion((angleZ+90)%360);//mpu rotation
  flag=2;
  delay(300);
  MoveReverse(3000);

  siloDrop();// for silo border
  stop();
  delay(200);
  fillSilos();
  
  flag=1;
}

// int distLeft()
// {
//   digitalWrite(trigPinL, LOW);
//   delayMicroseconds(2);
//   digitalWrite(trigPinL, HIGH);
//   delayMicroseconds(10);
//   digitalWrite(trigPinL, LOW);
//   durL=pulseIn(echoPinL, HIGH);
//   distL=durL*sovel/2;
//   return distL;
// }

int distLeft()
{
  // lidarSerial.flush();
  if(lidarSerial.available())
  {
    lrv=lidarSerial.parseInt();
    lv=String(lrv);
    lc=lv.toInt();
    // Serial.println(lc);
    if(lc<500 && lc>0)
    {
      lcl=lc;
    }
    // Serial.println(lcl);
    Serial.println("Current Distance (distance left)");
    Serial.println(lcl);
    return lcl;
  }
  return -1;
}

float Ultrasilo()
{
  URM_sense_t = analogRead(URM09Pin);

  dist_t = URM_sense_t * MAX_RANG  / ADC_SOLUTION;
  Serial.println("Current Distance (Ultrasilo)");
  Serial.println(dist_t);
  return dist_t;
}

// int Ultrasilo()
// {
//   digitalWrite(trigPinR, LOW);
//   delayMicroseconds(2);
//   digitalWrite(trigPinR, HIGH);
//   delayMicroseconds(10);
//   digitalWrite(trigPinR, LOW);
//   durR=pulseIn(echoPinR, HIGH);
//   distR=durR*sovel/2;
//   return distR;
// }

int distSilo()
{
  digitalWrite(trigPinS, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinS, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinS, LOW);
  durS=pulseIn(echoPinS, HIGH);
  distS=durS*sovel/2;
  return distS;
}

int getDistance()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration*.0343)/2;
  delay(100);
  return distance;
}

void stop() 
{
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);
}

void bakward()
{
  motor1.setSpeed(40);
  motor2.setSpeed(40);
  motor3.setSpeed(-40);
  motor4.setSpeed(-40);
}

void Bakward()
{
  motor1.setSpeed(FORWARD);
  motor2.setSpeed(FORWARD);
  motor3.setSpeed(BACKWARD);
  motor4.setSpeed(BACKWARD);
}

void Backward(int speed) 
{
  motor1.setSpeed(speed);
  motor2.setSpeed(speed);
  motor3.setSpeed(-speed);
  motor4.setSpeed(-speed);
}

void Left(int t)
{
  motor1.setSpeed(t);
  motor2.setSpeed(t);
  motor3.setSpeed(t);
  motor4.setSpeed(t);
}

void Right(int t)
{
  motor1.setSpeed(-t);
  motor2.setSpeed(-t);
  motor3.setSpeed(-t);
  motor4.setSpeed(-t);
}

void Forward(int speed) 
{
  motor1.setSpeed(-speed);
  motor2.setSpeed(-speed);
  motor3.setSpeed(speed);
  motor4.setSpeed(speed);
}

void left(int speed) 
{
  motor1.setSpeed(speed);
  motor2.setSpeed(speed);
  motor3.setSpeed(speed);
  motor4.setSpeed(speed);
}

void right(int speed) 
{
  motor1.setSpeed(-speed);
  motor2.setSpeed(-speed);
  motor3.setSpeed(-speed);
  motor4.setSpeed(-speed);
}

void Leftsideway()
{
  motor1.setSpeed(70);
  motor2.setSpeed(-70);
  motor3.setSpeed(70);
  motor4.setSpeed(-72);
}

void rightsideway()
{
  motor1.setSpeed(-70);
  motor2.setSpeed(70);
  motor3.setSpeed(-70);
  motor4.setSpeed(72);
}

void ServoOpen()
{
  Myservo.write(0);              

  delay(1800);

  Myservo.write(80);              
}

void Rotaion(int degree)
{
  if(degree>0)
  {
    int dr=(degree) * 2.9;
    int target=pos1+dr;

    while (pos1<=target) 
    {
      
      Right(80);
    }
  }
  else if((degree)<0)
  {
    int dl=degree * 2.9;
    int target=pos1+dl;

    while (pos1>=target) 
    {
      
      Left(80);
    }
  }
  i=pos1;

  stop();
  delay(1000);
}

void MoveForward(int dis)
{
  int di=(dis*133)/399;
  i=pos1+di;

  while (pos1<=i)
  {
   
    if(pos1>=i-250 && pos1<=i)
    {
      Forward(40);
    }
   Forward(120);
  }
  stop();
  delay(1000);  
}

void MoveReverse(int dis)
{
  int di=(dis*133)/399;
  i=pos1-di;

  while (pos1>=i)
  {
    
    Bakward();
  }
  stop();
  delay(1000);
}

void MoveRight(int dr)
{
  int di=(dr*133)/399;
  i=pos1+di;

  while(pos1<=i)
  {
    
    rightsideway();
  }
 
  stop();
  delay(1000); 
}

void MoveLeft(int dl)
{
  int di=(dl*133)/399;
  i=pos1-di;
  
  while (pos1>=i)
  {
     Leftsideway();
  }

  stop();
  delay(1000);
}

void drop()
{
  digitalWrite(IN1,HIGH);
  digitalWrite(IN3,HIGH);
  delay(2000);
  digitalWrite(IN1,LOW);
  digitalWrite(IN3,LOW);
  delay(200);  
}

void readencoder1()
{
  int a = digitalRead(outputB1);

  if (a > 0)
  {
    pos1++;
  }
  else
  {
    pos1--;
  }
}