// gear slop is about 25 pos ticks
// 5ms pulse moves about 50 pos ticks

int setPoint = 512;
int powerMax = 255;
float Kp = -3;
float Kd = -10;
float Ki = -0.005;
float E = 0;
float I = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    int input = Serial.parseInt();
    Serial.read();
    if (input >= 10) {
      setPoint = constrain(input,10,1013);
    }
  }

  if ((millis() % 2000) < 2000) {
    runPID();
  }
  else {
    stopMotor();
  }
}

void runPID() {
  int pos = readPos();
  float error = setPoint - pos;

  if (abs(error) < 20)
    error = 0;
    
  I += error;

  float D = (D*2 + (error - E))/3;
  E = error;
  float control = Kp * error + Ki * I + Kd * D;
  int out = constrain(control, -powerMax, powerMax);
  int dir = out >= 0;
  int outabs = abs(out);

  if (outabs < 80) {
    outabs = 0;
  }

  analogWrite(dir ? 6 : 5, 0);
  analogWrite(dir ? 5 : 6, outabs);

  if (error != 0) {
  Serial.print(setPoint);
  Serial.print(",");
  Serial.print(pos);
  Serial.print(",");
  Serial.print(E*Kp);
  Serial.print(",");
  Serial.print(I*Ki);
  Serial.print(",");
  Serial.print(D*Kd);
  Serial.print(",");
  Serial.println(out);
  }
}

void stopMotor() {
  analogWrite(5, 0);
  analogWrite(6, 0);
}

int readPos() {
  return analogRead(A0);
}
