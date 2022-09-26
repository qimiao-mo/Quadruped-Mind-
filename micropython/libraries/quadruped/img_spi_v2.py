# Untitled - By: hong - 周四 8月 18 2022


from machine import SPI
from fpioa_manager import fm
from Maix import GPIO
import time
import sensor, image
import ujson
import struct

SPI_data_len = 1022
data_read = bytearray(1024)

def Init():
    global mosi,miso,cs,clk,signal,RedPIn,spi1
    print("开启spi初始化")
    mosi=23 #4
    miso=22 #3
    cs=24   #5
    clk=21  #2
    signal = 15 #7
    #引脚映射
    fm.register(cs,fm.fpioa.GPIOHS10)#cs
    cs = GPIO(GPIO.GPIOHS10, GPIO.OUT)
    fm.register(mosi,fm.fpioa.SPI1_D0)#mosi
    fm.register(miso,fm.fpioa.SPI1_D1)#miso
    fm.register(clk,fm.fpioa.SPI1_SCLK)#sclk
    #握手信号引脚映射
    fm.register(signal,fm.fpioa.GPIOHS11)
    RedPIn = GPIO(GPIO.GPIOHS11,GPIO.IN)
    #创建SPi对象
    spi1 = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=8000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)#10000000

#bytearray
#等待握手
def Delay_H():
    global SPI_data_len,cs,RedPIn,spi1
    i=0
    while(1):
        if RedPIn.value() == 1:
            break

#等待握手
def Delay_L():
    global SPI_data_len,cs,RedPIn,spi1
    i=0
    while(1):
        if RedPIn.value() == 0:
            break

#spi发送字节
def spi_send(data):
    global SPI_data_len,cs,RedPIn,spi1,data_read
    if  len(data) == 0:
        return
    #print(data)
    cs.value(0)
    Delay_H()
    #spi1.write(data)
    spi1.write_readinto(data,data_read)
    cs.value(1)
    Delay_L()

#spi发送字节
def spi_send_json(data):
    global SPI_data_len,cs,RedPIn,spi1

    if  len(data) == 0:
        return
    cs.value(0)
    Delay_H()
    spi1.write(data)
    cs.value(1)
    Delay_L()

#spi发送字符
def spi_send_process(data):
    global SPI_data_len,cs,RedPIn,spi1,data_send,data_read
    length = len(data)
    if length == 0 or length > SPI_data_len:
        return
    if length == SPI_data_len:
        datas = b''
        datas = datas + data
        data_len = length.to_bytes(2,'big')
        datas = datas + data_len
        cs.value(0)
        Delay_H()
        #spi1.write(datas)
        spi1.write_readinto(datas,data_read)
        cs.value(1)
        Delay_L()
        return data_read
    else:
        datas = b''
        datas = datas + data
        data_len = length.to_bytes(2,'big')
        data_Replenish = 0
        data_Replenish = data_Replenish.to_bytes(SPI_data_len - length,'big')
        datas = datas + data_Replenish
        datas = datas + data_len
        cs.value(0)
        Delay_H()
        spi1.write_readinto(datas,data_read)
        cs.value(1)
        Delay_L()
        return data_read

#启动处理
def spi_send_Start(data):
    length = len(data)
    datas = b''
    datas = datas + data
    data_len = length.to_bytes(2,'big')
    data_Replenish = 0
    data_Replenish = data_Replenish.to_bytes(SPI_data_len - length,'big')
    datas = datas + data_Replenish
    datas = datas + data_len
    return datas

#def spi_read()


#################################################图传###############################################
#启动数据处理
Start = b'ok'
Start = spi_send_Start(Start)#启动处理
def img_app(imgs,size):
    global SPI_data_len,cs,RedPIn,spi1,Start
    imgs = imgs.compress(quality=size)  #压缩图片提升传输速率，想要图像更清晰将quality调大一些（quality范围在0~100）
    img_bytes = imgs.to_bytes(1,'little')      #将图片转成字节数组
    block = int(len(img_bytes)/SPI_data_len)

    spi_send(Start)#"ok“启动
    #print(spi_send_process(str(imgs.size()))) #图像大小
    spi_send_process(str(imgs.size()))

    for i in range(block):
        spi_send_process(img_bytes[i*SPI_data_len:(i+1)*SPI_data_len])
    spi_send_process(img_bytes[block*SPI_data_len:])



#################################################基础控制############################################
Mode = 0x00
Action_sta = 0x00
Action_id = 0x00
X_speed = 0.00
Y_speed = 0.00
Z_speed = 0.00
X_angle = 0.00
Y_angle = 0.00
Z_angle = 0.00
High = 0x00

#float转4字节十六进制
def send_float(tx_Buf,data):
    temp_B= struct.pack('f',float(data))
    tx_Buf.append(temp_B[0])
    tx_Buf.append(temp_B[1])
    tx_Buf.append(temp_B[2])
    tx_Buf.append(temp_B[3])
#int转4字节十六进制
def send_int(tx_Buf,data):
    temp_B= struct.pack('i',int(data))
    tx_Buf.append(temp_B[0])
    tx_Buf.append(temp_B[1])
    tx_Buf.append(temp_B[2])
    tx_Buf.append(temp_B[3])
#char转4字节十六进制
def send_char(tx_Buf,data):
    tx_Buf.append(int(data))
#运动数据发送
tx_data =  bytearray(1024)
def sport_control_send():
    global Mode,Action_sta,Action_id,X_speed,Y_speed,Z_speed ,X_angle,Y_angle,Z_angle,High,tx_data

    data_to_send  =  []
    data_to_send.append(0xAA)
    data_to_send.append(0xAF)
    #data_to_send.append(0x01)
    send_char(data_to_send,Mode)#Mode
    send_char(data_to_send,Action_sta)#Action_sta
    send_char(data_to_send,Action_id)#Action_id
    send_float(data_to_send,X_speed)#Robot_X_speed
    send_float(data_to_send,Y_speed)#Robot_Y_speed
    send_float(data_to_send,Z_speed)
    send_float(data_to_send,X_angle)
    send_float(data_to_send,Y_angle)
    send_float(data_to_send,Z_angle)
    send_char(data_to_send,High)#High
    data_to_send.append(0x00)
    data_to_send.append(0x00)
    data_to_send.append(0x00)
    data_to_send.append(0x00)
    for i in range(0,len(data_to_send)):
        tx_data[i] = data_to_send[i]
    tx_data[1022] = 0x00
    tx_data[1023] =  len(data_to_send)
    spi_send(tx_data)
    #print(tx_data[0:len(data_to_send)])



#模式
def Robots_mode(mode):
    global Mode
    Mode = mode
    sport_control_send()

#动作组
def Robots_Action(sta,ids):
    global Action_sta,Action_id
    Action_sta = sta
    Action_id = ids
    sport_control_send()

#前进速度（-1.4~1.4）
def Robots_Xspeed(speed):
    global X_speed
    X_speed = speed
    sport_control_send()

#左右移动速度（-1.4~1.4）
def Robots_Yspeed(speed):
    global Y_speed
    Y_speed = speed
    sport_control_send()

#右转转动速度（-1.4~1.4）
def Robots_Zspeed(speed):
    global Z_speed
    Z_speed = speed
    sport_control_send()

#俯仰角度（-1.4~1.4）
def Robots_Xangle(angle):
    global X_angle
    X_angle = angle
    sport_control_send()

#左右倾斜角度（-1.4~1.4）
def Robots_Yangle(angle):
    global Y_angle
    Y_angle = angle
    sport_control_send()

#左右扭动角度（-1.4~1.4）
def Robots_Zangle(angle):
    global Z_angle
    Z_angle = angle
    sport_control_send()

#高度（0~10）
def Robots_High(high):
    global High
    High = high
    sport_control_send()

#机器人状态、k210控制功能数据（机器人状态、动作组状态、功能控制1、功能控制2）
def Robots_Sta():
    global data_read
    data_send = bytearray(1024)
    data_send[0] = 0xCA
    data_send[1] = 0xCF
    data_send[1022] = 0x00
    data_send[1023] = 0x0A
    spi_send(data_send)
    sums = 0
    lens = 0
    if(data_read[0] == 0xBA and data_read[1] == 0xBF):
        lens = data_read[2] + 2
        for i in range(0,lens+1):
            sums += data_read[i]
        sums = sums&0xff #取低位
        if(sums == data_read[lens+1]):
            return data_read[3:lens+1]
    data_read[0] = 255;    
    data_read[1] = 255;     
    return data_read[3:5]

###############################################测试#################################################
#Init()
#sport_control_send()
#Init()
#Robots_mode(2)
#Robots_High(10)
#print(Robots_Sta())
#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)
#if __name__=='__main__':
    #clock = time.clock()
    #while(1):
        #clock.tick()

        ##Robots_High(10)
        #img = sensor.snapshot()
        #img_app(img,80)
        ##sport_control_send()
        ##Robots_mode(2)
        #print(clock.fps())


