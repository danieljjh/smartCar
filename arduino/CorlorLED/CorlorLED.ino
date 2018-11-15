/**
* @par Copyright (C): 2010-2019, Shenzhen Yahboom Tech
* @file         ColorLED.c
* @author       Danny
* @version      V1.0
* @date         2017.07.25
* @brief       七彩探照灯实验
* @details
* @par History  见如下说明
*/

#define ON 1     //使能LED
#define OFF 0    //禁止LED

//定义引脚
int LED_R = 11;  //LED_R接在arduino上的数字11口
int LED_G = 10;  //LED_G接在arduino上的数字10口
int LED_B =  9;  //LED_B接在arduino上的数字9口

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
}

//以下为LED的呼吸灯的代码
//void breath_LED(int LED_type)
// {
//	int i = 0;
//	for (i = 0; i < 20; i++)
//	{
//		digitalWrite(LED_type, HIGH);
//		delay(i);
//		digitalWrite(LED_type, LOW);
//		delay(20 - i);
//	}
//
//	for (i = 0; i < 20; i++)
//	{
//		digitalWrite(LED_type, LOW);
//		delay(i);
//		digitalWrite(LED_type, HIGH);
//		delay(20 - i);
//    }
//
//    //延时1s
//    delay(1000);
// }
//
// //以下是RGB三色闪光灯
// void light_LED()
// {
//	digitalWrite(LED_R, HIGH);   //点亮红色LED
//	delay(1000);                 //延时1s
//	digitalWrite(LED_R, LOW);    //灭红色LED
//	delay(1000);                 //延时1s
//
//	digitalWrite(LED_G, HIGH);   //点亮绿色LED
//	delay(1000);                 //延时1s
//	digitalWrite(LED_G, LOW);    //灭绿色LED
//	delay(1000);                 //延时1s
//
//	digitalWrite(LED_B, HIGH);   //点亮蓝色LED
//	delay(1000);                 //延时1s
//	digitalWrite(LED_B, LOW);    //灭蓝色LED
//	delay(1000);                 //延时1s
//}

/**
* Function       color_led
* @author        Danny
* @date          2017.07.25
* @brief         由R,G,B三色的不同组合形成7种不同的色彩
* @param[in1]    Red开关
* @param[in2]    Green开关
* @param[in3]    Blue开关
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

/**
* Function       loop
* @author        Danny
* @date          2017.07.25
* @brief         先延时2，再循环显7色LED
* @param[in]     void
* @retval        void
* @par History   无
*/
void loop()
{
  //        //呼吸灯闪烁5次
  //	int i;
  //        for (i = 0; i < 5; i++)
  //        {
  //           breath_LED(LED_B);
  //	}
  //        delay(2000);
  //
  //        //RGB三色闪光灯闪烁3次
  //        for (i = 0; i < 3; i++)
  //        {
  //	   light_LED();
  //        }
  //        delay(2000);
  //
  delay(2000);
  //循环显示7色LED
  while (1)
  {                          //LED_R    LED_G    LED_B
    color_led(ON, OFF, OFF); //   1        0        0
    delay(1000);
    color_led(OFF, ON, OFF); //   0        1        0
    delay(1000);
    color_led(OFF, OFF, ON); //   0        0        1
    delay(1000);
    color_led(ON, ON, OFF);  //   1        1        0
    delay(1000);
    color_led(ON, OFF, ON);  //   1        0        1
    delay(1000);
    color_led(OFF, ON, ON);  //   0        1        1
    delay(1000);
    color_led(ON, ON, ON);   //   1        1        1
  }
}



