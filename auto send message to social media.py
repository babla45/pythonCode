#this code will send message automatically to whatsapp, messenger etc
try:
    import pyautogui as pg
    import time
    
    time.sleep(5)
    txt=open("animals.txt",'r')
    
    n=1
    for i in txt:
        pg.write(i)
        pg.press('Enter')
        time.sleep(3)
        n=n+1
        if(n==5):
            txt.close()
            break
except KeyboardInterrupt:
    print("\n")
    txt.close()
