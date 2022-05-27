from socket import*
import time
import random
import threading


serverName='127.0.0.1'
serverPort=12003
clientSocket=socket(AF_INET,SOCK_DGRAM)

modimessage,serverAddress=bytes(0),bytes(0)
seq,count,end,start=0,0,0,0
count,delay=0,0
errorp=['false']*1+['true']*999


def resend():
    global start,choice,count,message,seq,modimessage,serverAddress,thnum,iffalse,delay,timeover
    count=0

    choice=random.choice(errorp)
    start=time.time()

    if (timeover==1):
        changeseq()
    message=str(seq)+'데이터'

    if choice=='false':
        iffalse=1 #손실이일어남
    else:
        clientSocket.sendto((str(seq)+','+message).encode(),(serverName,serverPort))
        iffalse=0 #손실이 일어나지 않음

    print('pck',seq,'을 보냈습니다. //',seq,message)
    changeseq()

    if delay==1:
        changeseq()
        modimessage,serverAddress=clientSocket.recvfrom(2048)
        print('지연된 ack',seq,'를 받았습니다.')
        changeseq()
    threading.Thread(target=iftimeout).start()
        
def changeseq():
    global seq
    if seq==0:
        seq=1
    else:
        seq=0   
        
def iftimeout():
    global end,start,seq,count,modimessage,serverAddress,delay,timeover
    while True:
        end=time.time()
        if end-start>0.01:
            print('시간초과!')
            if iffalse==0: #지연발생
                delay=1
            else: #패킷손실발생
                print('패킷손실됨!')
            timeover=1
            resend()
            break
        else: #시간안에 도착
            timeover=0
            if iffalse==0: #손실아니면
                delay=0 
                modimessage,serverAddress=clientSocket.recvfrom(2048) 
                count=1 #ack를 받았다.
                break


def full():
    global count,seq
    time.sleep(1)
    while count==0:
        resend()

while True:
    thnum,iffalse,delay,timeover=0,0,0,0
    resend()
    full()
    finallymessage=modimessage.decode()
    if (((seq==1)and(finallymessage.split(',')[0]=='0'))or((seq==0)and('1'==finallymessage.split(',')[0]))): 
        print('ack',finallymessage.split(',')[0],'를 받았습니다. //')
    else:
        print('ack',finallymessage.split(',')[0],'를 받았습니다. //')

    print('----------------')

clientSocket.close()
