#define IR_SENSOR_FRONT 10
#define IR_SENSOR_LEFT 11
#define IR_SENSOR_RIGHT 12
#define IR_SENSOR_FAR_LEFT 7
#define IR_SENSOR_FAR_RIGHT 8
#define MOTOR_SPEED 150

//Left motor
int enableLeftMotor=6;
int leftMotorPin1=2;
int leftMotorPin2=3;

//Right motor
int enableRightMotor=9;
int rightMotorPin1=4;
int rightMotorPin2=5;

//Complete maze boolean flag
bool complete = false;

void setup()
{ 
  // put your setup code here, to run once:
  TCCR0B = TCCR0B & B11111000 | B00000010 ;

  pinMode(enableRightMotor, OUTPUT);
  pinMode(rightMotorPin1, OUTPUT);
  pinMode(rightMotorPin2, OUTPUT);
  
  pinMode(enableLeftMotor, OUTPUT);
  pinMode(leftMotorPin1, OUTPUT);
  pinMode(leftMotorPin2, OUTPUT);

  pinMode(IR_SENSOR_RIGHT, INPUT);
  pinMode(IR_SENSOR_LEFT, INPUT);
  pinMode(IR_SENSOR_FRONT, INPUT);
  pinMode(IR_SENSOR_FAR_LEFT, INPUT);
  pinMode(IR_SENSOR_FAR_RIGHT, INPUT);
  rotateMotor(0,0);  

  Serial.begin(9600);
  Serial.print("Hello World!");

  delay(100000); //wait 10 seconds
}


void loop()
{
  int leftIRSensorValue = digitalRead(IR_SENSOR_LEFT);
  int rightIRSensorValue = digitalRead(IR_SENSOR_RIGHT);
  int frontIRSensorValue = digitalRead(IR_SENSOR_FRONT);
  int farLeftIRSensorValue = digitalRead(IR_SENSOR_FAR_LEFT);
  int farRightIRSensorValue = digitalRead(IR_SENSOR_FAR_RIGHT);

  if (farLeftIRSensorValue == HIGH && farRightIRSensorValue == HIGH && leftIRSensorValue == HIGH && rightIRSensorValue == HIGH && frontIRSensorValue == HIGH) {
    checkEnd();
    Serial.print("End");
  }

  else if (farLeftIRSensorValue == LOW && farRightIRSensorValue == LOW & frontIRSensorValue == HIGH) 
  {
    goStraight();
  }



  else if ((farLeftIRSensorValue == HIGH || farRightIRSensorValue == HIGH) || (farLeftIRSensorValue == LOW && farRightIRSensorValue == LOW && frontIRSensorValue == LOW))
  {
    handleJunction();
  }

  else {
    rotateMotor(0,0);
    Serial.print("Stopped");
  }


}

bool checkEnd() {
  Serial.println(complete);
  if (complete == true) {
    rotateMotor(0,0);
    return;
  }
  else {
    rotateMotor(MOTOR_SPEED, MOTOR_SPEED);
    delay(1500);

    int frontIRSensorValue = digitalRead(IR_SENSOR_FRONT);

    if (frontIRSensorValue == LOW) {
      rotateMotor(-MOTOR_SPEED, -MOTOR_SPEED);
    }
    else {
      rotateMotor(0,0);
      complete = true;
    }
  }
}

void goStraight() {
  int leftIRSensorValue = digitalRead(IR_SENSOR_LEFT);
  int rightIRSensorValue = digitalRead(IR_SENSOR_RIGHT);
  int frontIRSensorValue = digitalRead(IR_SENSOR_FRONT);
  int farLeftIRSensorValue = digitalRead(IR_SENSOR_FAR_LEFT);
  int farRightIRSensorValue = digitalRead(IR_SENSOR_FAR_RIGHT);

  if (leftIRSensorValue == LOW && rightIRSensorValue == LOW && frontIRSensorValue == HIGH)
  {
    rotateMotor(MOTOR_SPEED, MOTOR_SPEED);
  }
  else if (leftIRSensorValue == LOW && rightIRSensorValue == HIGH && frontIRSensorValue == HIGH)
  {
    rotateMotor(MOTOR_SPEED, -MOTOR_SPEED);
  }
  else if (leftIRSensorValue == HIGH && rightIRSensorValue == LOW && frontIRSensorValue == HIGH) 
  {
    rotateMotor(-MOTOR_SPEED, MOTOR_SPEED);
  }
  else if (leftIRSensorValue == HIGH && rightIRSensorValue == HIGH && frontIRSensorValue == HIGH) {
    rotateMotor(0, 0);
    return;
  }
  else 
  {
    return;
  }
}

void handleJunction() {
  int leftIRSensorValue = digitalRead(IR_SENSOR_LEFT);
  int rightIRSensorValue = digitalRead(IR_SENSOR_RIGHT);
  int frontIRSensorValue = digitalRead(IR_SENSOR_FRONT);
  int farLeftIRSensorValue = digitalRead(IR_SENSOR_FAR_LEFT);
  int farRightIRSensorValue = digitalRead(IR_SENSOR_FAR_RIGHT);

  //T junction
  if(farLeftIRSensorValue == HIGH && farRightIRSensorValue == HIGH && frontIRSensorValue == LOW) {
      rotateMotor(0, MOTOR_SPEED); //Turn left
      Serial.print("T junction");
  }

  //Left turn
  else if(farLeftIRSensorValue == HIGH && farRightIRSensorValue == LOW && frontIRSensorValue == LOW) {
      rotateMotor(0, MOTOR_SPEED); //Turn left
      Serial.print("Left turn");
  }

  //Left t junction
  else if(farLeftIRSensorValue == HIGH && farRightIRSensorValue == LOW && frontIRSensorValue == HIGH) {
      rotateMotor(0, MOTOR_SPEED); //Turn left
      Serial.print("Left t junction");
  }

  //Right turn
  else if(farLeftIRSensorValue == LOW && farRightIRSensorValue == HIGH && frontIRSensorValue == LOW) {
      rotateMotor(MOTOR_SPEED, 0); //Turn right
      Serial.print("Right turn");
  }

  //Right t junction
  else if(farLeftIRSensorValue == LOW && farRightIRSensorValue == HIGH && frontIRSensorValue == HIGH) {
      rotateMotor(MOTOR_SPEED, 0); //Turn right
      Serial.print("Right t junction");
  }

  //U turn
  else if (farLeftIRSensorValue == LOW && farRightIRSensorValue == LOW && frontIRSensorValue == LOW) {
      rotateMotor(-MOTOR_SPEED, MOTOR_SPEED); //Turn left
  }

  else {
    return;
  }
}

void rotateMotor(int leftMotorSpeed, int rightMotorSpeed)
{
  
  if (rightMotorSpeed < 0)
  {
    digitalWrite(rightMotorPin1,HIGH);
    digitalWrite(rightMotorPin2,LOW);    
  }
  else if (rightMotorSpeed > 0)
  {
    digitalWrite(rightMotorPin1,LOW);
    digitalWrite(rightMotorPin2,HIGH);      
  }
  else
  {
    digitalWrite(rightMotorPin1,LOW);
    digitalWrite(rightMotorPin2,LOW);      
  }

  if (leftMotorSpeed < 0)
  {
    digitalWrite(leftMotorPin1,HIGH);
    digitalWrite(leftMotorPin2,LOW);    
  }
  else if (leftMotorSpeed > 0)
  {
    digitalWrite(leftMotorPin1,LOW);
    digitalWrite(leftMotorPin2,HIGH);      
  }
  else 
  {
    digitalWrite(leftMotorPin1,LOW);
    digitalWrite(leftMotorPin2,LOW);      
  }
  analogWrite(enableRightMotor, abs(rightMotorSpeed));
  analogWrite(enableLeftMotor, abs(leftMotorSpeed));    
}