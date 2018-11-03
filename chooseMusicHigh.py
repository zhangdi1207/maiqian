import pygame,time,os
import RPi.GPIO as GPIO

pinList=[4,17,27,22,5,6,13,19,26,20,21]
musicList=['/home/pi/myInitSetting/music'+str(i)+'.mp3' for i in range(10)]
orMusicList=['/home/pi/myInitSetting/'+str(i)+'.mp3' for i in range(10)]
usedChanle=10
oldChanle=10
lightPin=[18,23,24,25,12]



def musicInit():
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode([100,100])

def GPIOinit():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinList,GPIO.IN)
        GPIO.setup(lightPin,GPIO.OUT,initial=GPIO.LOW)


def change2Pin(a):
        global lightPin
        GPIO.setup(lightPin,GPIO.OUT,initial=GPIO.LOW)
        for i in range(3):
                a,tempPin=divmod(a,2)
                GPIO.output(lightPin[i],tempPin)
        if a==1:
                GPIO.setup(lightPin[4],GPIO.OUT,initial=GPIO.HIGH)
        else:
                GPIO.setup(lightPin[3],GPIO.OUT,initial=GPIO.HIGH)  

def play():
        global usedChanle
        global pinList
        global musicList
        global oldChanle
        
        for i in range(10):
                #print('aaa',i,usedChanle,GPIO.input(pinList[i]))
                if i!=usedChanle:
                        if GPIO.input(pinList[i])==1:
                                time.sleep(0.2)
                                if GPIO.input(pinList[i])==0:
                                        continue
                                #print('bbb',GPIO.input(pinList[i]),pinList[i])
                                while(GPIO.input(pinList[i])==1):
                                        a=1
                                GPIO.setup(pinList[usedChanle],GPIO.IN)
                                GPIO.setup(pinList[i],GPIO.OUT,initial=GPIO.HIGH)
                                try:
                                        pygame.mixer.music.load(musicList[i])
                                except:
                                        pygame.mixer.music.load(orMusicList[i])
                                pygame.mixer.music.play()
                                usedChanle=i
                else:
                        GPIO.setup(pinList[i],GPIO.OUT,initial=GPIO.LOW)
                        GPIO.setup(pinList[i],GPIO.IN)
                        if GPIO.input(pinList[i])==1:
                                time.sleep(0.05)
                                if GPIO.input(pinList[i])==1:
                                        while(GPIO.input(pinList[i])==1):
                                                a=1
                                        pygame.mixer.music.stop()
                                        GPIO.setup(pinList[i],GPIO.IN)
                                        usedChanle=10
                                        continue
                        GPIO.setup(pinList[i],GPIO.OUT,initial=GPIO.HIGH)
        if oldChanle!=usedChanle:
                change2Pin(usedChanle)
                oldChanle=usedChanle
        time.sleep(0.1)

def music():
        time.sleep(0.1)
        musicInit()
        GPIOinit()
        change2Pin(10)
        while (True):
                play()

music()
