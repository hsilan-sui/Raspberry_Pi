'''
目的：創建了一個GUI應用程序，用於控制RGB LED的顏色，並實現了閃爍效果。用戶可以通過滑桿調節紅、綠、藍三種顏色的亮度，並可以看到實時更新的RGB顏色值。閃爍效果在背景線程中運行，確保主窗口流暢響應用戶操作
'''
import RPi.GPIO as GPIO
import tkinter as tk
from time import sleep
import threading


GPIO.setwarnings(False) #關閉GPIO警告信息
GPIO.setmode(GPIO.BCM) #設置GPIO編號方式為BCM模式，按照BCM編號來控制GPIO pin腳

# GPIO 引腳
RED_PIN = 5
GREEN_PIN = 6
BLUE_PIN = 13

#將這些針腳設置為輸出模式，用於控制PWM信號
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# 初始化PWM #在紅綠藍 針腳上初始化PWM信號，頻率為1000 Hz
r = GPIO.PWM(RED_PIN, 1000)  
g = GPIO.PWM(GREEN_PIN, 1000)
b = GPIO.PWM(BLUE_PIN, 1000)

#啟動PWM信號，初始佔空比為0，即LED最初是關閉的
r.start(0) #close
g.start(0) #close
b.start(0) #close

# 更新RGB值函式
def update_rgb(value):
    """透過滑桿的數值 來決定 RGB燈泡的光色"""
    red_value = scale_red.get() # 獲取紅色滑桿的當前值
    green_value = scale_green.get() # 獲取綠色滑桿的當前值
    blue_value = scale_blue.get() # 獲取藍色滑桿的當前值

    # 將滑桿值轉換為佔空比並更新PWM信號，從而調整LED亮度
    r.ChangeDutyCycle(red_value * 100 / 255)
    g.ChangeDutyCycle(green_value * 100 / 255)
    b.ChangeDutyCycle(blue_value * 100 / 255)
    
    # 更新顯示RGB值的標籤
    rgb_display.set(f'RGB: ({red_value}, {green_value}, {blue_value})')

# 想要有閃爍效果 => 設定閃爍效果函式
def flash_effect():
    """閃爍函式設定"""
    global flashing, flash_on # 全域變數
    if flashing: # 是否有這個值
        red_value = scale_red.get() #取的紅色的值
        green_value = scale_green.get()  #取的綠色的值
        blue_value = scale_blue.get() #取的藍色的值

       
        if flash_on:  #根據flash_on狀態切換LED的開關狀態
            r.ChangeDutyCycle(0)
            g.ChangeDutyCycle(0)
            b.ChangeDutyCycle(0)
        else:
            r.ChangeDutyCycle(red_value * 100 / 255)
            g.ChangeDutyCycle(green_value * 100 / 255)
            b.ChangeDutyCycle(blue_value * 100 / 255)
        
        # Toggle the flash_on state
        flash_on = not flash_on
        
        # 設置定時器.timer來定期呼叫flash_effect函數，實現閃爍效果
        threading.Timer(flash_interval, flash_effect).start()

# 閃爍效果的參數設定
flash_interval = 0.5  # 閃爍間隔時間設為0.5秒
flashing = True  # 閃爍效果啟用
flash_on = True  # LED當前狀態為開啟

# 設置主Tkinter窗口
root = tk.Tk() #初始化Tkinter主窗口
root.title('RGB Control') #設置窗口標題
root.geometry('400x400') #設置窗口尺寸

# 創建RGB控制滑桿
scale_red = tk.Scale(root, from_=0, to=255, orient='horizontal', resolution=1, label='Red', command=update_rgb) #創建水平滑塊，用於調節RGB顏色的紅、綠、藍分量 #每當滑塊值改變時，調用update_rgb函數更新顏色
scale_red.pack(pady=10)

scale_green = tk.Scale(root, from_=0, to=255, orient='horizontal', resolution=1, label='Green', command=update_rgb)
scale_green.pack(pady=10)

scale_blue = tk.Scale(root, from_=0, to=255, orient='horizontal', resolution=1, label='Blue', command=update_rgb)
scale_blue.pack(pady=10)

# 顯示RGB顏色值的標籤
rgb_display = tk.StringVar() #創建一個StringVar對象，用於顯示RGB值
rgb_display.set('RGB:(0,0,0)')
label = tk.Label(root, textvariable=rgb_display) #創建一個標籤，顯示RGB顏色值
label.pack(pady=10) #將標籤添加到窗口中，並設置垂直間距

# 啟動Tkinter事件循環
try:
    # 啟動一個新線程來處理閃爍效果，設置為守護線程，這樣主程序退出時該線程也會自動退出
    threading.Thread(target=flash_effect, daemon=True).start()

    # 啟動Tkinter主事件循環，處理用戶輸入和其他事件
    root.mainloop()

except KeyboardInterrupt: #捕獲用戶中斷程序的情況，並打印消息
    print("Program interrupted by user")

finally:
    # 塊中的代碼確保無論如何都會執行，停止PWM信號並清理GPIO設置
    r.stop()
    g.stop()
    b.stop()
    GPIO.cleanup()
