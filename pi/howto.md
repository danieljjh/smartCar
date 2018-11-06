# how to run

## project folder
`/home/pi/project/`

## python env
cv3py3  python3 with opencv3.4

if you can not run workon:
`source ~/.profile`


## libs

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

