import pyautogui as pg
import time
import pyperclip

# beautifulsoup爬的时候个人信息被隐藏起来了爬不到，如果有更好的方法可以考虑
# 发现不正常时合上笔记本进入休眠模式强制终止运行
# 请根据自己笔记本的像素配置来测试确保鼠标的位置基本正确，确定像素的方式可以用微信截图功能
# 浏览器中按照顺序打开三个页面，最好不要有多余页面：icsc members的directory页面（目前做到了第12页）， google sheets留出上次爬的最后一行，和一个空白的浏览器页面
# 点击运行代码之后切换到谷歌浏览器
# 代码的原理是鼠标移动到固定的像素坐标点击，非常机械。比如有些人没有公司名字，在directory页面就会少一行，程序滚动的距离就会出现错误，从而复制不到正确的信息
# 如果有检测页面信息的方法可以考虑代码实现来减少很多错误，如果不能实现就等只能爬完或者强制终止然后手动改

# 在主页滚动到名字，点开人名，等待页面加载
def click_name(x_loc, y_loc):
    pg.moveTo(x_loc, y_loc, duration=0.1)
    pg.click()
    time.sleep(4)

# 进入到一个人的信息页面之后，给定位置，拖动到位置，复制一条信息，在浏览器空白页上粘贴一下去掉字体和开头的换行，然后复制粘贴到google sheets
def copy(icsc_loc_x : int, icsc_loc_y : int, drag_x : int, drag_y : int, sheets_x : int, sheets_y : int):
    pg.moveTo(180, 20, duration=0.1)# icsc页面像素坐标
    pg.click()
    pg.moveTo(icsc_loc_x, icsc_loc_y, duration=0.1)# 给定位置
    pg.dragTo(drag_x, drag_y, duration=0.4)# 拖动到位置
    pg.hotkey('ctrl', 'c')# 复制一条信息
    pg.moveTo(580, 20, duration=0.1)# 空白页像素坐标
    pg.click()
    pg.moveTo(400, 50, duration=0.1)
    pg.click()
    pg.click()
    pg.hotkey('ctrl', 'a')
    pg.hotkey("backspace")
    pg.hotkey('ctrl', 'shift', 'v')# 浏览器空白页上粘贴一下
    pg.hotkey('ctrl', 'a')
    pg.hotkey('ctrl', 'c')# 复制
    content = pyperclip.paste() # 粘贴到python环境下面用
    pg.moveTo(380, 20, duration=0.1)# google sheets像素坐标
    pg.click()
    pg.click()
    pg.moveTo(sheets_x, sheets_y, duration=0.1)# 粘贴到google sheets
    pg.click()
    pg.click()
    pg.moveTo(200, 230, duration=0.1)
    pg.click()
    pg.hotkey('ctrl', 'shift', 'v')
    pg.hotkey('enter')
    return content

# 一个人的所有信息
def get_info():
    name = copy(200, 325, 700, 325, 100, 300)
    title = copy(235, 660, 670, 660, 200, 300)
    city = copy(235, 685, 670, 685, 300, 300)
    company = copy(235, 720, 670, 720, 400, 300)
    type = copy(235, 745, 670, 745, 500, 300)
    # 大多数学生没有电话
    if type == 'Academic Institution':
        pg.moveTo(180, 20, duration=0.1)
        pg.click()
        pg.moveTo(900, 435, duration=0.1)
        pg.click()
        time.sleep(5)
        email = copy(850, 430, 1130, 430, 700, 300)
    else:
        phone = copy(850, 430, 1000, 430, 600, 300)
        pg.moveTo(180, 20, duration=0.1)
        pg.click()
        pg.moveTo(900, 465, duration=0.1)
        pg.click()
        time.sleep(5)
        email = copy(850, 465, 1130, 465, 700, 300)
    pg.moveTo(800, 300, duration=0.1)
    pg.click()
    pg.vscroll(-50)

# 爬完回到directory页面
def return_to_directory():
    pg.moveTo(180, 20, duration=0.1)
    pg.click()
    pg.moveTo(20, 50, duration=0.1)
    pg.click()
    time.sleep(4)
    pg.hotkey('ctrl', 'home')


# 程序运行代码
time.sleep(5)
pg.moveTo(180, 20)
pg.click()
pg.hotkey('ctrl', 'home')

for n in range(1, 0, -1):
    # 596:1, 19*x+596=4244:20, x=192
    # from 1st to 21st person, increment by 192
    # 每一页前21个人从页面顶部往下scroll 596+192*i个像素第一个就是
    for i in range(0, 21):
        pg.moveTo(1750, 540)
        pg.vscroll(round(-596 - i * 192))
        click_name(740, 150)
        get_info()
        return_to_directory()

    # 解决页面底部scroll不到的问题
    for i in range(0, 3):
        pg.hotkey('ctrl', 'end')
        click_name(740, int(160 + i * 160))
        get_info()
        return_to_directory()
    
    # 如果一次爬很多页面可以到页面底部换页，现在基本不用，因为每页都停下来修改信息不完整的人
    if n > 1:
        pg.hotkey('ctrl', 'end')
        pg.moveTo(1210, 647)
        pg.click()
        time.sleep(4)
        pg.hotkey('ctrl', 'home')