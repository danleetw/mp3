# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:11:43 2020

@author: danle
"""


#https://daydaynews.cc/zh-tw/technology/243292.html

import os
import sys

#----Disable 笨訊息-----
import warnings
warnings.filterwarnings("ignore")

''' 一路試了好多函數才找到目前程式的位置
from pathlib import Path

path = Path(__file__).parent.absolute()
print(path)

mypath = Path().absolute()
print('Absolute path : {}'.format(mypath))

#if you want to go to any other file inside the subdirectories of the directory path got from above method
filePath = mypath/'data'/'fuel_econ.csv'
print('File path : {}'.format(filePath))

#To check if file present in that directory or Not
isfileExist = filePath.exists()
print('isfileExist : {}'.format(isfileExist))

#To check if the path is a directory or a File
isadirectory = filePath.is_dir()
print('isadirectory : {}'.format(isadirectory))

print(os.path.realpath(__file__))
print(os.path.dirname(sys.argv[0])  )
input("A")
'''


#pip install pydub
from pydub import AudioSegment
import pydub
#pydub.AudioSegment.converter = os.path.join(os.getcwd(),"ffmpeg.exe")
#-----原來的Util/Which函數寫得很笨，這邊指定就好
#----要在模組載入之後設定，其實這個AudioSegment模組只是Call ffmpeg工具，所以有些地方會不明當掉的原因在此
AudioSegment.converter = os.path.join(os.path.dirname(sys.argv[0]),"ffmpeg.exe")


#--------調整音量--------
def adj_vol(src,tar,db):
    sound = AudioSegment.from_file(src, "mp3")
    
    change_in_dBFS=db-sound.dBFS
    
    print(" DB:",str(sound.dBFS)[:6])
    #----正負差3才調整
    if abs(change_in_dBFS)>3:
       print("  Gain")
       print("  ","#"*40)
       normalized_sound=sound.apply_gain(change_in_dBFS)
       print("   adj to:",str(normalized_sound.dBFS)[:6])
       print("   Output to :",tar)
       normalized_sound.export(tar, format="mp3")
       #print("   Remove Source:",src)
       os.remove(src)
       #print("   Rename ",tar, " to ",src)
       os.rename(tar,src)
    else:
       print("  Pass") 
   
    return sound.dBFS



print("----Mp3 Gain----- Dan Lee 2020/04/25")



db_min=99
db_max=-100
db_cnt=0
db_sum=0

def adj_one_folder(src_path):
    global db_min
    global db_max
    global db_cnt
    global db_sum
    
    
    if os.path.isdir(src_path):
       files=os.listdir(src_path)
       
    else:
       files=(src_path,)
    #print(files)
    
    for file in files:
        
        if file.upper().endswith(".MP3"):
            
            db_cnt=db_cnt+1
            
            print("Convert Cnt=",db_cnt)
            
            src=os.path.join(src_path,file)
            
            trg=os.path.join(src_path,file[:-3]+"mp3_")
            
            print("Src MP3:",src)
            
            #----標準音量設-20
            ret=adj_vol(src,trg,-20)
            
            if ret<db_min:
                
                db_min=ret
               
            if ret>db_max:
                
                db_max=ret
                
            db_sum=db_sum+ret 
            
            print(" DB Statics info")
            print("  Min:",str(db_min)[:6],"Avg:",str(db_sum/db_cnt)[:6],"Max:",str(db_max)[:6])
            print("--------------")
            
def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


#--------Main Program--------------------------------------------------

file_paths = sys.argv[1:]  # the first argument is the script itself

if len(file_paths)>0:
    for src_path in file_paths:
        adj_one_folder(src_path)
    if db_cnt==0:
        print("No any mp3 files to adj!")
    else:
        print("Total process {} files".format(db_cnt))  
else:
    print("No given folders path!")
    print(" Please assing one or drog and drop some folder in icon!")
print("Press a key to exit....")    
wait_key()
        
  