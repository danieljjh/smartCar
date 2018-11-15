
int SensorPin = 12;     // 触摸模块输入端口

int hand_start=0;

  int Sensor_L=A0;  //前左红外避障器
  int Sensor_R=A5;  //前右红外避障器

void loop()
{
  int f; 

  Blue_Str();
    hand_start=digitalRead(SensorPin);

   if (hand_start==0)
   {;}

    while (blue_start>0 )
    {
 //    Serial.println(blue_start);
      if (digitalRead(Sensor_L) && digitalRead(Sensor_R))    //前方无障碍blue_start>0) 
      {
        Blue_Str();
// Serial.println("LR");
      }
      else 
      {
        stop();
//         Serial.println("L>>>>>R");
//       Blue_Str();
      }
    }

     
      while (hand_start==1)
      {
        blue_start=LOW;

        if (digitalRead(Sensor_L) && digitalRead(Sensor_R))    //前方无障碍
        {
          CJ();             //超声波测距
          JL_Panduan();     //距离判断并动作
          L_R();
        }
        else 
        {
            GoGo_back();
            delay(300);
            stop();
            LR_panduan();
            L_R();
        }
      }

}