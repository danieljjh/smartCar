# how to run

## project folder
`/home/pi/project/`

## python env
cv3py3  python3 with opencv3.4

if you can not run workon:
`source ~/.profile`


## libs

[gpio doc](http://shumeipai.nxez.com/2014/12/27/rpio-document-rpio-py.html)

### picamera

Use Picamera to capture image and video
[Picamera Doc](https://picamera.readthedocs.io/en/latest/quickstart.html)


### opencv python
For object detect 
[Opencv Python](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html)

[Opencv tutorial](https://pythonprogramming.net/loading-images-python-opencv-tutorial/)


### mac 上查看 pi camera 视频流

pi 安装 vlc server 
`sudo apt-get insall vlc`

启动视频流
`raspivid -o - -w 320 -h 240 -t 9999999 |cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264`

w: 宽度，h 高 , 8554  端口  h264 视频编码

mac, 安装 vlc 播放器
播放地址 rtsp://192.168.0.5:8554/


### pi  webcam  视频流
https://pimylifeup.com/raspberry-pi-webcam-server/


### 设置 pi 自启动服务

https://www.jianshu.com/p/86adb6d5347b

python 脚本 自启动
https://www.embbnux.com/2015/04/12/raspberry_pi_setting_python_script_start_on_boot/

### PWM
[pwm](http://shumeipai.nxez.com/2016/09/28/rpi-gpio-module-basics.html)

### uart 外接串口
https://zhuanlan.zhihu.com/p/38853178

https://blog.csdn.net/qq_32384313/article/details/77745907

https://blog.blahgeek.com/raspberry-pi-uartzong-xian-chuan-kou-lan-ya-mo-kuai-shi-yong-xiao-ji.html

http://shumeipai.nxez.com/2016/08/08/solution-raspberry-pi3-serial-uart-use-issues.html

byte 转 string
https://techtutorialsx.com/2018/02/04/python-converting-string-to-bytes-object/


### 在树莓派上轻松实现深度学习目标检测
http://shumeipai.nxez.com/2018/10/05/how-to-easily-detect-objects-with-deep-learning-on-raspberry-pi.html


### pi car example

https://zhengludwig.wordpress.com/projects/self-driving-rc-car/

https://www.hackster.io/bestd25/pi-car-016e66


## system

free  命令  查看内存
sudo swapon -s 查看 swap 空间