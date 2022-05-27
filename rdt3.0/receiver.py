from socket import*
import random
serverPort=12003
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))


seq=0
print('서버 받을 준비 됨')

errorp=['false']*0+['true']*999

print('-------------------')
while True:
    compare=2
    choice=random.choice(errorp)
    message,senderAddress=serverSocket.recvfrom(2048)
    modimessage=message.decode()
    print('pck',modimessage.split(',')[0],'를 받았습니다.')

    if choice=='false':

        print('ack',modimessage.split(',')[0],'를 보냈습니다.')
        print('***ack손실***')
        
    else:
        if modimessage.split(',')[0]==str(seq):
            serverSocket.sendto(modimessage.encode(),senderAddress)
            print('ack',modimessage.split(',')[0],'를 보냈습니다.')
            compare=0
        else: 
            serverSocket.sendto(modimessage.encode(),senderAddress)
            print('ack',modimessage.split(',')[0],'를 보냈습니다.')
            compare=1

    if compare==0:
        if seq==0:
           seq=1
        else:
          seq=0      
    #print('pck',seq,'를 기다립니다.')
    print('-------------------')
