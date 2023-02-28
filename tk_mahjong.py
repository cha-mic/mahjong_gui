from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

# 手牌の枚数
tehai_count = 0

# 手牌の中のそれぞれの牌の枚数
m_num = [0] * 10
p_num = [0] * 10
s_num = [0] * 10
j_num = [0] * 10

# 点数計算用
def tehai_culc(m_num, p_num, s_num, j_num):

    fu  = 30 #翻
    han = 0  #符

    # 役満判定

    ##　国士無双
    kokusi = 1
    for i in range(7):
        kokusi = kokusi * j_num[i]

    kokusi = kokusi * m_num[0] * m_num[8] * s_num[0] * s_num[8] * p_num[0] * p_num[8]
    if(  kokusi == 2 ):
            han = 13
            return han, fu
    
    ## ちゅーれん
    flag = 1
    for i in range(8):
        if( m_num[i] == 0 ):
            flag = 0
    if( flag == 1 ):
        if( (m_num[0] >= 3) & (m_num[8] >= 3) ):
            han = 13
            return han, fu

    flag = 1
    for i in range(8):
        if( p_num[i] == 0 ):
            flag = 0
    if( flag == 1 ):
        if( (p_num[0] >= 3) & (p_num[8] >= 3) ):
            han = 13
            return han, fu 

    flag = 1
    for i in range(8):
        if( s_num[i] == 0 ):
            flag = 0
    if( flag == 1 ):
        if( (s_num[0] >= 3) & (s_num[8] >= 3) ):
            han = 13
            return han, fu   
    
    ## 大三元
    if( (j_num[4] >= 3) &  (j_num[5] >= 3) & (j_num[6] >= 3)):
        han = 13
        return han, fu
    
    ## 大四喜
    if( (j_num[0] >= 3) &  (j_num[1] >= 3) & (j_num[2] >= 3) & (j_num[3] >= 3)):
        han = 13
        return han, fu  
     
    ## 小四喜
    if( (j_num[0] >= 2) &  (j_num[1] >= 2) & (j_num[2] >= 2) & (j_num[3] >= 2)):
        han = 13
        return han, fu  

    

    return han, fu

def display_result( m_num, p_num, s_num, j_num ):

    han, fu = tehai_culc(m_num, p_num, s_num, j_num)

    root2 = Tk()
    root2.title("result")

    frame2 = ttk.Frame(root2, padding = 3)
    # label2 = ttk.Label(frame2, text= "役満")

    if( han >= 13):
        label2 = ttk.Label(frame2, text= "役満")
    
    frame2.pack()
    label2.pack(side = TOP)


# ボタンが押されたら牌を表示する
def display_hai( type, num):

    global tehai_count
    global img_m, img_p, img_s
    global m_num, p_num, s_num, j_num

    if( tehai_button["variable"].get() == True ):
        if( tehai_count < 13 ):
            if( type == "m" ):
                tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_m[num], anchor = NW)
                m_num[num] = m_num[num] + 1
                # print(m_num)

            elif( type == "p" ):
                tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_p[num], anchor = NW)
                p_num[num] = p_num[num] + 1

            elif( type == "s" ):
                tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_s[num], anchor = NW)
                s_num[num] = s_num[num] + 1

            elif( type == "j" ):
                tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_j[num], anchor = NW)
                j_num[num] = j_num[num] + 1

        elif( tehai_count == 13 ):
            if( type == "m" ):
                tsumo_canvas.create_image(4, 4, image = img_m[num], anchor = NW)
                m_num[num] = m_num[num] + 1
                # print(m_num)

            elif( type == "p" ):
                tsumo_canvas.create_image(4, 4, image = img_p[num], anchor = NW)
                p_num[num] = p_num[num] + 1

            elif( type == "s" ):
                tsumo_canvas.create_image(4, 4, image = img_s[num], anchor = NW)
                s_num[num] = s_num[num] + 1

            elif( type == "j" ):
                tsumo_canvas.create_image(4, 4, image = img_j[num], anchor = NW)
                j_num[num] = j_num[num] + 1
        
        else:
            print("can't display")

    tehai_count = tehai_count + 1

    if( tehai_count == 14 ):
        culc_button["state"] = NORMAL
    elif( tehai_count > 14 ):
        culc_button["state"] = DISABLED


if __name__ == '__main__':

    root = Tk()
    root.title("my first app")

    # 画像の読み込み
    img_m = []
    for mans in range(9):
        img_m.append(ImageTk.PhotoImage(Image.open('./img/_'+ str(mans + 1) +'m.png')))
    img_m.append(ImageTk.PhotoImage(Image.open('./img/_5m_aka.png')))

    img_p = []
    for pins in range(9):
        img_p.append(ImageTk.PhotoImage(Image.open('./img/_'+ str(pins + 1) +'p.png')))
    img_p.append(ImageTk.PhotoImage(Image.open('./img/_5p_aka.png')))

    img_s = []
    for sous in range(9):
        img_s.append(ImageTk.PhotoImage(Image.open('./img/_'+ str(sous + 1) +'s.png')))
    img_s.append(ImageTk.PhotoImage(Image.open('./img/_5s_aka.png')))

    img_j = []
    for ji in range(7):
        img_j.append(ImageTk.PhotoImage(Image.open('./img/_ji'+ str(ji + 1) +'.png')))
    

    frame1 = ttk.Frame(root, padding = 16)
    tehai_canvas_width = 17
    tehai_canvas = Canvas(frame1, bg = "green", width = 40 * tehai_canvas_width , height = 48)
    tsumo_canvas = Canvas(frame1, bg = "green", width = 40,                       height = 48)
    label1 = ttk.Label(frame1, text = '牌をクリックして入力')

    frame1.grid(row = 0, column = 0)
    label1.grid(row = 0, column = 0, columnspan = tehai_canvas_width)

    # 風牌，ドラの入力場所
    row_setting = 3
    column_setting = 0

    kaze_button = []
    kaze_canvas = []

    kaze_button.append( Checkbutton(frame1, text = "場風") )
    kaze_button.append( Checkbutton(frame1, text = "自風") )

    kaze_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )
    kaze_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )

    kaze_button[0].grid(row = row_setting - 2, column = column_setting,     columnspan  =2)
    kaze_button[1].grid(row = row_setting - 2, column = column_setting + 2, columnspan  =2)

    kaze_canvas[0].grid(row = row_setting - 1, column = column_setting,     columnspan  =2)
    kaze_canvas[1].grid(row = row_setting - 1, column = column_setting + 2, columnspan  =2)

    dora_button = []
    dora_canvas = []
    uradora_button = []
    uradora_canvas = []

    dora_button.append( Checkbutton(frame1, text = "ドラ") )
    dora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )

    uradora_button.append( Checkbutton(frame1, text = "裏ドラ") )
    uradora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )

    for i in range(4):
        dora_button.append( Checkbutton(frame1, text = "カンドラ" + str(i + 1)) )
        dora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )
        uradora_button.append( Checkbutton(frame1, text = "裏ドラ" + str(i + 2)) )
        uradora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )
    
    for i in range(5):
        dora_button[i].grid(row = row_setting,     column = i * 2, columnspan = 2)
        dora_canvas[i].grid(row = row_setting + 1, column = i * 2, columnspan = 2)
        uradora_button[i].grid(row = row_setting + 2, column = i * 2, columnspan = 2)
        uradora_canvas[i].grid(row = row_setting + 3, column = i * 2, columnspan = 2)

    # ここまで


    # 入力ボタンの生成
    row_input = row_setting + 7

    # マンズの入力        
    for mans in range(10):
        ttk.Button(
            frame1,
            image = img_m[mans],
            command = lambda num = mans: display_hai('m', num)
        ).grid(row = row_input + 1, column = mans, padx = 0)

    # ピンズの入力  
    for pins in range(10):
        ttk.Button(
            frame1,
            image = img_p[pins],
            command = lambda num = pins: display_hai('p', num)
        ).grid(row = row_input + 2, column = pins, padx = 0)

    # ソウズの入力  
    for sous in range(10):
        ttk.Button(
            frame1,
            image = img_s[sous],
            command = lambda num = sous: display_hai('s', num)
        ).grid(row = row_input + 3, column = sous, padx = 0)
    
    # 字牌の入力        
    for ji in range(7):
        ttk.Button(
            frame1,
            image = img_j[ji],
            command = lambda num = ji: display_hai('j', num)
        ).grid(row = row_input + 4, column = ji, padx = 0)

    # ここまで

    # 計算ボタンの配置
    culc_button = ttk.Button(
        frame1, 
        text = "計算", 
        command = lambda : display_result(m_num, p_num, s_num, j_num),
        state = DISABLED
        )
    culc_button.grid(row = row_input, column = tehai_canvas_width + 2)

    tehai_button = Checkbutton(frame1, text = "手牌")
    tehai_button.grid(row = row_input - 1, column = 0, columnspan = tehai_canvas_width)
    tehai_canvas.grid(row = row_input, column = 0, columnspan = tehai_canvas_width)
    tsumo_canvas.grid(row = row_input, column = tehai_canvas_width + 1)

    root.mainloop()
