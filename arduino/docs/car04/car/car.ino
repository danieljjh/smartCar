/*小车运动代码*/
int INA = 4;      //电机A正反转控制端
int PWMA = 5;     //电机A调速端
int INB = 7;      //电机B正反转控制端
int PWMB = 6;     //电机B调速端

int value_L,value_R;
int L_run,  R_run;    //驱动运行值

String inString = "";  //串口输入字符串
int blue_start=0;      //蓝牙启动标志

//===========  电机动作  ===============//
//高速前进
void Gogo()
{
  value_L = L_run ;
  value_R = R_run ;
  Go_run();
//  Serial.println("Gogo");  
}

//低速前进
void Go()
{
  value_L = L_run ;
  value_R = R_run ;
  Go_run();
//  Serial.println("Go");
}

//高速后退
void GoGo_back()
{
  value_L = 200 ;
  value_R = 200 ;
  digitalWrite(INA,LOW);          //反转
  digitalWrite(INB,LOW);
  analogWrite(PWMA,value_L);      //PWM调速
  analogWrite(PWMB,value_R);
//  Serial.println("back");
  // tone(PEER, 800,100); 
  delay(80);
}

//大左转
void Da_left()
{
  value_L = L_run ;
  value_R = R_run ;
  Go_run();
//  Serial.println("Da_left");  
  delay(100);
}

//大右转
void Da_right()
{
  value_L = L_run ;
  value_R = R_run ;
  Go_run();
//  Serial.println("Da_right");
  delay(100);

}

//90°左转弯
void left()
{
  value_L = 0 ;
  value_R = 250 ;
  Go_run();
//  Serial.println("left");
  delay(800);
}

//90°右转弯
void right()
{
  value_L = 250 ;
  value_R = 0 ;
  Go_run();
//  Serial.println("right");
  delay(800);
}

//左转弯掉头
void Diaotou_left()
{
  value_L = 0 ;
  value_R = 250 ;
  Go_run();
//  Serial.println("Diaotu_left");
  delay(1700);
}


//右转弯掉头
void Diaotou_right()
{
  value_L = 250 ;
  value_R = 0 ;
  Go_run();
//  Serial.println("Diaotu_right");
  delay(1700);
}

//停止
void stop()
{
  value_L = 0 ;
  value_R = 0 ;
  analogWrite(PWMA,value_L);      //PWM调速
  analogWrite(PWMB,value_R);
  Serial.println("stop");
  blue_start=0;
  //  tone(PEER, 800,100);     //蜂鸣器叫
}

//前进驱动
void Go_run()
{
  digitalWrite(INA,HIGH);
  digitalWrite(INB,HIGH);
  analogWrite(PWMA,value_L);      //PWM调速
  analogWrite(PWMB,value_R);
  //  digitalWrite(PEER,0);
}

//===========  蓝牙  ==============//
void Blue_Str()
{
  while (Serial.available() > 0)
  {
    int inChar = Serial.read();
    inString += (char)inChar; 
  }

  if (inString=="go")  
  {
    L_run=160;  
    R_run=160;
 //       Serial.println("Go");
    Go();
    inString = "";
    blue_start=1;
  }

  if (inString=="gogo")  
  {
    L_run=250;  
    R_run=250;
//        Serial.println("Gogo");
    Gogo();
    inString = "";
    blue_start=1;
  }


  if (inString=="stop")
  {
//    Serial.println("stop1");
    stop();
    inString = "";
    blue_start=0;
  }

  if (inString=="left")
  {
//        Serial.println("left1");
    left();
    inString = "";
     blue_start=1;
  }

  if (inString=="right")
  {
 //       Serial.println("right1");
    right();
    inString = "";
     blue_start=1;
  } 

  if (inString=="back")
  {
    //    Serial.println("back1");
    GoGo_back();
    inString = "";
     blue_start=1;
  } 

  // if (inString=="D-left")
  // {
  //   L_run=0;  
  //   R_run=200;
  //   Diaotou_left();
  //   inString = "";
  // } 

  // if (inString=="D-right")
  // {
  //   L_run=200;  
  //   R_run=0;
  //   Diaotou_right();
  //   inString = "";
  // }

  if (inString=="D-left1")
  {
    L_run=200;  
    R_run=0;
    digitalWrite(INA,LOW);          //反转
    digitalWrite(INB,LOW);
    analogWrite(PWMA,value_L);      //PWM调速
    analogWrite(PWMB,value_R);
    inString = "";

  if (inString=="D-right1")
  {
    L_run=0;  
    R_run=200;
    digitalWrite(INA,LOW);          //反转
    digitalWrite(INB,LOW);
    analogWrite(PWMA,value_L);      //PWM调速
    analogWrite(PWMB,value_R);
    inString = "";
  }  
  }
}

