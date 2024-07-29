# 樹莓派筆記

## 認識基本項目

> 認識 GPIO

- GPIO（General Purpose Input/Output）｜引腳
  - 我使用的是有 40 個引腳（或 26 個，取決於您的 Pi 型號）
  - 引腳是所謂的『GPIO 介面』的一部分
    - 在這些介面中，有四種主要的引腳:
      • 電源: 提供 3.3V 和 5V 的直流電源
      • 接地（GND）: 連接到地端，以閉合電路
      • DNC: 代表“不連接”，所以可以忽略
      • GPIO: 可以設置為發送(output)或接收(input)控制電壓

![GPIO](images/gpio.png)

- GPIO 代表“通用輸入/輸出”，正是這些引腳讓 Raspberry Pi 發揮了其功效。因為這些引腳沒有特定的功能，所以可以設置為某個專用功能，例如控制信號

> 麵包板 的通電範例

- 紅電軌 ＝> 正極
- 黑/藍電軌 ＝> 負極
- ![麵包板](images/breadboard_01.png)

- 中間橫向排序的 5 孔是通電的，有以 ABCDE 為一組，FGHIJ 為一組
- ![麵包板](images/breadboard_02.png)
- 五孔為一組，線路一樣燈泡都亮：
- ![麵包板](images/breadboard_03.png)
- 也可以這樣插電：
- ![麵包板](images/breadboard_04.png)

## 用程式控制你的 LED 燈的明滅

> 使用設備

- Raspberry Pi
- LED
- 電阻 220 Ω 或其他適合阻值
- 麵包板
- 杜邦線

> 成品

> 程式
