//  yfrobot motor sheld demo code

int E1 = 5; // PWM A
int M1 = 4; // DIR A
int E2 = 6; // PWM B
int M2 = 7; // DIR B

int Val = 0 ;
int ChangeValue = 20;
void setup()
{
pinMode(M1, OUTPUT);
pinMode(M2, OUTPUT);
}

void forward()
{
  digitalWrite(M1, LOW);
  digitalWrite(E1, Val);
  
  digitalWrite(M2, LOW);
  digitalWrite(E2, Val);

  Val = Val + ChangeValue;
  if (Val == 0 || Val == 255) 
  {
    ChangeValue = -ChangeValue;  
  }

  delay(1000);
}


void backword()
{
  digitalWrite(M1, HIGH);
  digitalWrite(E1, Val); // PWM 调速

  digitalWrite(M2, HIGH);
  digitalWrite(E2, Val);
}

  
void loop()
{
  forward();
  delay(3000);
  backword();
  delay(3000);
}
