/**
* @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
* @file         infrared_avoid.c
* @author       Danny
* @version      V1.0
* @date         2017.07.25
* @brief        红外避障实验
* @details
* @par History  见如下说明
*
*/

#define ON 1     //使能LED
#define OFF 0    //禁止LED
//定义引脚
int LED_R = 11;  //LED_R接在arduino上的数字11口
int LED_G = 10;  //LED_G接在arduino上的数字10口
int LED_B =  9;  //LED_B接在arduino上的数字9口

int Left_motor_go = 8;        //左电机前进 AIN1
int Left_motor_back = 7;      //左电机后退 AIN2

int Right_motor_go = 2;       //右电机前进 BIN1
int Right_motor_back = 4;     //右电机后退 BIN2

int Left_motor_pwm = 6;       //左电机控速 PWMA
int Right_motor_pwm = 5;      //右电机控速 PWMB

int key = 2;                 //定义按键为arduino的模拟口 2

const int AvoidSensorLeft =  A2;   //定义左边避障的红外传感器引脚为A2
const int AvoidSensorRight = A1;   //定义右边避障的红外传感器引脚为A1

int LeftSensorValue ;              //定义变量来保存红外传感器采集的数据大小
int RightSensorValue ;


int Echo = 12;  // 定义超声波输入脚
int Trig = 13;  // 定义超声波输出脚

int Distance = 0;

boolean start = false;

/**
* Function       setup
* @author        Danny
* @date          2017.07.25
* @brief         初始化配置
* @param[in]     void
* @retval        void
* @par History   无
*/
void setup()
{
  //初始化RGB三色LED的IO口为输出方式
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  
  //初始化电机驱动IO口为输出方式
  pinMode(Left_motor_go, OUTPUT);
  pinMode(Left_motor_back, OUTPUT);
  pinMode(Right_motor_go, OUTPUT);
  pinMode(Right_motor_back, OUTPUT);

  //定义按键接口为输入接口
//  pinMode(key, INPUT);

  //定义左右传感器为输入接口
  pinMode(AvoidSensorLeft, INPUT);
  pinMode(AvoidSensorRight, INPUT);



  //左右传感器初始化为高电平
  digitalWrite(AvoidSensorLeft, HIGH);
  digitalWrite(AvoidSensorRight, HIGH);

  //初始化超声波引脚
  pinMode(Echo, INPUT);    // 定义超声波输入脚
  pinMode(Trig, OUTPUT);   // 

  //按键初始化为高电平
  digitalWrite(key, LOW);

  attachInterrupt(digitalPinToInterrupt(key), key_scan2, CHANGE);
  //调用按键扫描函数
//  key_scan();
//  color_led(ON, OFF, OFF); 
//  delay(2000);
    Serial.begin(9600);
    
    Serial.println("key..init");
    Serial.println(digitalRead(key));
    
    Serial.println("start");
    get_serial();
}
/**
* Function       run
* @author        Danny
* @date          2017.07.25
* @brief         小车前进
* @param[in]     void
* @param[out]    void
* @retval        void
* @par History   无
*/
void run()
{
  //左电机前进
  digitalWrite(Left_motor_go, HIGH);   //左电机前进使能
  digitalWrite(Left_motor_back, LOW);  //左电机后退禁止
  analogWrite(Left_motor_pwm, 150);

  //右电机前进
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 150);
}

/**
* Function       brake
* @author        Danny
* @date          2017.07.25
* @brief         小车刹车
* @param[in]     time:延时时间
* @param[out]    void
* @retval        void
* @par History   无
*/
void brake(int time)
{
  digitalWrite(Left_motor_go, LOW);
  digitalWrite(Left_motor_back, LOW);
  digitalWrite(Right_motor_go, LOW);
  digitalWrite(Right_motor_back, LOW);
  delay(time * 100);
}

/**
* Function       left
* @author        Danny
* @date          2017.07.25
* @brief         小车左转(左轮不动，右轮前进)
* @param[in]     void
* @param[out]    void
* @retval        void
* @par History   无
*/
void left()
{
  //左电机停止
  digitalWrite(Left_motor_go, LOW);    //左电机前进禁止
  digitalWrite(Left_motor_back, LOW);  //左电机后退禁止
  analogWrite(Left_motor_pwm, 0);

  //右电机前进
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 80);
}

/**
* Function       right
* @author        Danny
* @date          2017.07.25
* @brief         小车右转(右轮不动，左轮前进)
* @param[in]     void
* @param[out]    void
* @retval        void
* @par History   无
*/
void right()
{
  //左电机前进
  digitalWrite(Left_motor_go, HIGH);   //左电机前进使能
  digitalWrite(Left_motor_back, LOW);  //左电机后退禁止
  analogWrite(Left_motor_pwm, 80);

  //右电机停止
  digitalWrite(Right_motor_go, LOW);   //右电机前进禁止
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 0);
}

/**
* Function       spin_left
* @author        Danny
* @date          2017.07.25
* @brief         小车原地左转(左轮后退，右轮前进)
* @param[in]     time：延时时间
* @param[out]    void
* @retval        void
* @par History   无
*/
void spin_left(int time)
{
  //左电机后退
  digitalWrite(Left_motor_go, LOW);     //左电机前进禁止
  digitalWrite(Left_motor_back, HIGH);  //左电机后退使能
  analogWrite(Left_motor_pwm, 150);

  //右电机前进
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 150);

  delay(time * 100);
}

/**
* Function       spin_right
* @author        Danny
* @date          2017.07.25
* @brief         小车原地右转(右轮后退，左轮前进)
* @param[in]     time：延时时间
* @param[out]    void
* @retval        void
* @par History   无
*/
void spin_right(int time)
{
  //左电机前进
  digitalWrite(Left_motor_go, HIGH);    //左电机前进使能
  digitalWrite(Left_motor_back, LOW);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 150);

  //右电机后退
  digitalWrite(Right_motor_go, LOW);    //右电机前进禁止
  digitalWrite(Right_motor_back, HIGH); //右电机后退使能
  analogWrite(Right_motor_pwm, 150);

  delay(time * 100);
}

/**
* Function       back
* @author        Danny
* @date          2017.07.25
* @brief         小车后退
* @param[in]     time：延时时间
* @param[out]    void
* @retval        void
* @par History   无
*/
void back(int time)
{
  //左电机后退
  digitalWrite(Left_motor_go, LOW);       //左电机前进禁止
  digitalWrite(Left_motor_back, HIGH);    //左电机后退使能
  analogWrite(Left_motor_pwm, 150);

  //右电机后退
  digitalWrite(Right_motor_go, LOW);     //右电机前进禁止
  digitalWrite(Right_motor_back, HIGH);  //右电机后退使能
  analogWrite(Right_motor_pwm, 150);

  delay(time * 100);
}

/**
* Function       key_scan
* @author        Danny
* @date          2017.07.25
* @brief         按键检测(包含软件按键去抖)
* @param[in]     void
* @param[out]    void
* @retval        void
* @par History   无
*/


void color_led(int v_iRed, int v_iGreen, int v_iBlue)
{
  //红色LED
  if (v_iRed == ON)
  {
    digitalWrite(LED_R, HIGH);
  }
  else
  {
    digitalWrite(LED_R, LOW);
  }
  //绿色LED
  if (v_iGreen == ON)
  {
    digitalWrite(LED_G, HIGH);
  }
  else
  {
    digitalWrite(LED_G, LOW);
  }
  //蓝色LED
  if (v_iBlue == ON)
  {
    digitalWrite(LED_B, HIGH);
  }
  else
  {
    digitalWrite(LED_B, LOW);
  }
}

void key_scan()
{
  while (digitalRead(key));       //当按键没有被按下一直循环
      color_led(OFF, OFF, ON);
      delay(1000);
    while (!digitalRead(key))       //当按键被按下时
    {
      delay(10);                    //延时10ms
      color_led(ON, OFF, OFF);
      if (digitalRead(key)  ==  LOW)//第二次判断按键是否被按下
      {
        delay(1000);
        while (!digitalRead(key));  //判断按键是否被松开
      }
  }
}

void key_scan2()
{
  if (digitalRead(key)  ==  HIGH)
  {
      color_led(OFF, OFF, ON);
      start = !start;
      Serial.print("start ");
      Serial.println(start);
      color_led(OFF, OFF, OFF);
  }
}
void Distance_test()   // 量出前方距离 
{
  digitalWrite(Trig, LOW);   // 给触发脚低电平2μs
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);  // 给触发脚高电平10μs，这里至少是10μs
  delayMicroseconds(15);
  digitalWrite(Trig, LOW);    // 持续给触发脚低电
  float Fdistance = pulseIn(Echo, HIGH);  // 读取高电平时间(单位：微秒)
  Fdistance= Fdistance/58;       //为什么除以58等于厘米，  Y米=（X秒*344）/2
  // X秒=（ 2*Y米）/344 ==》X秒=0.0058*Y米 ==》厘米=微秒/58
  Distance = Fdistance;
  Serial.print("Distance:"); 
  Serial.println(Distance); 
}

/**
* Function       loop
* @author        Danny
* @date          2017.07.25
* @brief         先调用setup初始化配置里面的按键扫描函数，接着红外避障模式开启
* @param[in]     void
* @retval        void
* @par History   无
*/
void loop()
{ 
  while (1)
  {
    
    while (start)
    {
        color_led(ON, OFF, ON);
         Distance_test();
         delay(2000);
    }
  }
}

/*
 * routes
 * set up routes
 * 
 */
void routes()
{
  
}
void backup_loop()
{
  //    delay(2000);
    //遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
    //未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
    LeftSensorValue  = digitalRead(AvoidSensorLeft);
    RightSensorValue = digitalRead(AvoidSensorRight);
    
    if (LeftSensorValue == HIGH && RightSensorValue == HIGH)
    {
      run();        //当两侧均未检测到障碍物时调用前进函数
//      Serial.println("run");
    }
    else if (LeftSensorValue == HIGH && RightSensorValue == LOW)
    {
//      Serial.println("RightSensorValue low");
//      Serial.println(RightSensorValue);
      spin_left(2); //右边探测到有障碍物，有信号返回，原地向左转
    }
    else if (RightSensorValue == HIGH && LeftSensorValue == LOW)
    {
//      Serial.println("LeftSensorValue low");
//      Serial.println(LeftSensorValue);
      spin_right(2);//左边探测到有障碍物，有信号返回，原地向右转
    }
    else
    {
      spin_right(2);//当两侧均检测到障碍物时调用固定方向的避障(原地右转)
    }
}

