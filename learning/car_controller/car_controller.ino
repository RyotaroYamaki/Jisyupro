#include <Servo.h>

#define AIN1 7
#define AIN2 9
#define PWMA 6
#define BIN1 3
#define BIN2 4
#define PWMB 5
#define STBY 2

#define MAX_ANGLE 32

Servo servo;
char key = 'c';
int offset = 102;
int angle = 0;

void setup(){
  servo.attach(8);
  
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(STBY, OUTPUT);
  
  Serial.begin(9600);
  servo.write(offset + angle);
}

void loop(){
  if(Serial.available() > 0){
    key = Serial.read();
  }
  if(key == 'a'){
    angle -= 2;
    if(angle < -MAX_ANGLE){
      angle = -MAX_ANGLE;
    }
    key = 'c';
  }else if(key == 's'){
    angle -= 1;
    if(angle < -MAX_ANGLE){
      angle = -MAX_ANGLE;
    }
    key = 'c';
  }else if(key == 'd'){
    angle += 1;
    if(angle > MAX_ANGLE){
      angle = MAX_ANGLE;
    }
    key = 'c';
  }else if(key == 'f'){
    angle += 2;
    if(angle > MAX_ANGLE){
      angle = MAX_ANGLE;
    }
    key = 'c';
  }
  delay(40);
  servo.write(offset + angle);

  analogWrite(PWMA, 15);
  analogWrite(PWMB, 15);
  
  digitalWrite(AIN1, LOW);
  //digitalWrite(AIN2, HIGH);
  digitalWrite(BIN1, LOW);
  //digitalWrite(BIN2, HIGH);
  digitalWrite(STBY, HIGH);
  if(key == 'p'){
      digitalWrite(AIN2, LOW);
      digitalWrite(BIN2, LOW);
  }else{
      digitalWrite(AIN2, HIGH);
      digitalWrite(BIN2, HIGH);
  }
}
