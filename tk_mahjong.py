# 計算
from mahjong.hand_calculating.hand import HandCalculator
# 麻雀牌
from mahjong.tile import TilesConverter
# 役, オプションルール
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
# 鳴き
from mahjong.meld import Meld
# 風(場&自)
from mahjong.constants import EAST, SOUTH, WEST, NORTH

# tkinter
from tkinter import *
from tkinter import ttk

# 画像の取り込み用
from PIL import ImageTk, Image

# 手牌の枚数
tehai_count = 0

# 赤ドラの枚数
aka_count = False

# 結果計算用
dora_indicators = []
config = HandConfig(is_riichi=False, player_wind=NONE, round_wind=NONE, options=OptionalRules(has_open_tanyao = True, has_aka_dora = aka_count))

# 手牌
tiles_m = ""
tiles_p = ""
tiles_s = ""
tiles_j = ""

# アガリ牌
wintile = {}

# 結果の表示
def display_result( result ):

    root2 = Tk()
    root2.title("Result")

    frame2 = ttk.Frame(root2, padding = 10)
    frame2.pack()

    if( result.yaku == None ):
        ttk.Label(frame2, text = "役なし", font=( "Helvetica", 14, "bold")).pack( side = TOP )
    else:
        ttk.Label(frame2, text= str(result.han) + "翻" + str(result.fu) + "符", font=( "Helvetica", 10, "bold")).pack( side = TOP )
        ttk.Label(frame2, text = str(result.cost['main']) + "-" + str(result.cost['additional']), font=( "Helvetica", 10, "bold")).pack( side = TOP )
        ttk.Label(frame2, text = str( result.yaku ), font=( "Helvetica", 10, "bold")).pack( side = TOP )

# 点数計算
def culc_result():

    global dora_indicators,config
    # print(dora_indicators)
    # print(config)

    global tiles_m, tiles_p, tiles_s, tiles_j, aka_count
    global wintile

    print(wintile)
    
    if( ('m' in wintile) == True ):
        tiles_m = tiles_m + str( wintile['m'] )
        win_tile = TilesConverter.string_to_136_array(man = str( wintile['m'] ))[0] 
    elif( ('p' in wintile) == True ):
        tiles_p = tiles_p + str( wintile['p'] )
        win_tile = TilesConverter.string_to_136_array(pin = str( wintile['p'] ))[0] 
    elif( ('s' in wintile) == True ):
        tiles_s = tiles_s + str( wintile['s'] )
        win_tile = TilesConverter.string_to_136_array(sou = str( wintile['s'] ))[0]
    elif( ('j' in wintile) == True ):
        tiles_j = tiles_j + str( wintile['j'] + 1 )
        win_tile = TilesConverter.string_to_136_array(honors = str( wintile['j']  + 1 ))[0]  

    print(tiles_m)
    print(tiles_p)
    print(tiles_s)
    print(tiles_j)
    
    tiles = TilesConverter.string_to_136_array(man = tiles_m, pin = tiles_p, sou = tiles_s, honors = tiles_j, has_aka_dora = aka_count)

    if( aka_count == True ):
        config.options.has_aka_dora = True

    melds = []

    calculator = HandCalculator()
    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

    print(result.yaku)
    print(result)

    display_result(result)

# チェックボックスの状態を取得
def check():

    check_state = 0

    for i in range(2):
        if( kaze_checkvar[i].get() == True ):
            check_state = check_state + 1

    for i in range(5):
        if( dora_checkvar[i].get() == True ):
            check_state = check_state + 1

    for i in range(5):
        if( uradora_checkvar[i].get() == True ):
            check_state = check_state + 1

    if( tehai_check.get() == True ):
        check_state = check_state + 1

    if( wintile_check.get() == True ):
        check_state = check_state + 1
    
    return check_state

# 牌が押された時の処理
def bottun_processing( type, num):

    global tehai_count
    global img_m, img_p, img_s

    wind = {0:EAST, 1:SOUTH, 2:WEST, 3:NORTH}

    if( check() != 1 ):
        print("error")
        return 0
    
    flag = 0

    # 風牌の記録
    for i in range(2):
        if( kaze_checkvar[i].get() == True ):
            place = kaze_canvas[i]
            flag = 1
            break

    if( flag == 1 ):
        place.create_image(4, 4, image = img_j[num], anchor = NW)
        if( i == 0 ):
            config.round_wind = wind[num]  
        elif( i == 1 ):
            config.player_wind = wind[num] 
        return 1

    flag = 0  

    # ドラ（表示牌）の記録
    for i in range(5):
        if( dora_checkvar[i].get() == True ):
            place = dora_canvas[i]
            flag = 1
            break  

    if( flag == 1 ):

        if( type == 'm' ):
            place.create_image(4, 4, image = img_m[num], anchor = NW)
        elif( type == 'p' ):
            place.create_image(4, 4, image = img_p[num], anchor = NW)
        elif( type == 's' ):
            place.create_image(4, 4, image = img_s[num], anchor = NW)
        elif( type == 'j'):
            place.create_image(4, 4, image = img_j[num], anchor = NW)

        if( type == 'm' ):
            dora_indicators.append( TilesConverter.string_to_136_array(man = str(num))[0] )
        elif( type == 'p' ):
            dora_indicators.append( TilesConverter.string_to_136_array(pin = str(num))[0] )
        elif( type == 's' ):
            dora_indicators.append( TilesConverter.string_to_136_array(sou = str(num))[0] )
        elif( type == 'j'):
            dora_indicators.append( TilesConverter.string_to_136_array(honors = str(num) + 1 )[0] )
        
        return 1

    # 裏ドラ（表示牌）の記録
    flag = 0

    for i in range(5):
        if( dora_checkvar[i].get() == True ):
            place = uradora_canvas[i]
            flag = 1
            break   
    
    if( flag == 1 ):

        if( type == 'm' ):
            place.create_image(4, 4, image = img_m[num], anchor = NW)
            dora_indicators.append( TilesConverter.string_to_136_array(man = str(num))[0] )
        elif( type == 'p' ):
            place.create_image(4, 4, image = img_p[num], anchor = NW)
            dora_indicators.append( TilesConverter.string_to_136_array(pin = str(num))[0] )
        elif( type == 's' ):
            place.create_image(4, 4, image = img_s[num], anchor = NW)
            dora_indicators.append( TilesConverter.string_to_136_array(sou = str(num))[0] )
        elif( type == 'j'):
            place.create_image(4, 4, image = img_j[num], anchor = NW)
            dora_indicators.append( TilesConverter.string_to_136_array(honors = str(num) + 1 )[0] )
        
        return 1

    # 手牌の記録
    flag = 0

    global tiles_m, tiles_p, tiles_s, tiles_j
    global aka_count

    if(tehai_check.get() == True):

        if( type == "m" ):
            tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_m[num], anchor = NW)
            tiles_m = tiles_m + str(num)
        elif( type == "p" ):
            tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_p[num], anchor = NW)
            tiles_p = tiles_p + str(num)
        elif( type == "s" ):
            tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_s[num], anchor = NW)
            tiles_s = tiles_s + str(num)
        elif( type == "j" ):
            tehai_canvas.create_image(tehai_count * 40 + 4 , 4, image = img_j[num], anchor = NW)
            tiles_j = tiles_j + str(num + 1)
        
        if( num == 0 ):
            aka_count = True

        flag = 1
        tehai_count = tehai_count + 1

        if( tehai_count >= 13 ):
            culc_button["state"] = NORMAL

        return 1
    
    # アガリ牌の記録
    flag = 0
    global wintile

    if( wintile_check.get() == True ):
        flag = 1

    if( flag == 1 ):

        if( type == 'm' ):
            agari_canvas.create_image(4, 4, image = img_m[num], anchor = NW)
        elif( type == 'p' ):
            agari_canvas.create_image(4, 4, image = img_p[num], anchor = NW)
        elif( type == 's' ):
            agari_canvas.create_image(4, 4, image = img_s[num], anchor = NW)
        elif( type == 'j'):
            agari_canvas.create_image(4, 4, image = img_j[num], anchor = NW)
        print(wintile)
        if( ('m' in wintile) == True ):
            tiles_m = tiles_m.replace(str( wintile['m'] ),'')
        elif( ('p' in wintile) == True ):
            tiles_p = tiles_p.replace(str( wintile['p'] ),'')
        elif( ('s' in wintile) == True ):
            tiles_s = tiles_s.replace(str( wintile['s'] ),'')
        elif( ('j' in wintile) == True ):
            tiles_j = tiles_j.replace(str( wintile['j'] ),'')
 
        if( num == 0 ):
            aka_count = True   
        
        # 辞書型で格納
        wintile = {type : num}

        # tehai_count = tehai_count + 1

        # if( tehai_count >= 14 ):
        #     culc_button["state"] = NORMAL

        return 1

# 牌の入力ボタンの生成
def make_inputbutton(row_input):

    # マンズの入力        
    for mans in range(10):
        ttk.Button(
            frame1,
            image = img_m[mans],
            command = lambda num = mans: bottun_processing('m', num)
        ).grid(row = row_input + 1, column = mans, padx = 0)

    # ピンズの入力  
    for pins in range(10):
        ttk.Button(
            frame1,
            image = img_p[pins],
            command = lambda num = pins: bottun_processing('p', num)
        ).grid(row = row_input + 2, column = pins, padx = 0)

    # ソウズの入力  
    for sous in range(10):
        ttk.Button(
            frame1,
            image = img_s[sous],
            command = lambda num = sous: bottun_processing('s', num)
        ).grid(row = row_input + 3, column = sous, padx = 0)
    
    # 字牌の入力        
    for ji in range(7):
        ttk.Button(
            frame1,
            image = img_j[ji],
            command = lambda num = ji: bottun_processing('j', num)
        ).grid(row = row_input + 4, column = ji, padx = 0)

    # ここまで

# 手牌のリセット
def reset_hand():

    global tiles_m, tiles_p, tiles_s, tiles_j, wintile
    global tehai_count, aka_count

    # 手牌
    tiles_m = ""
    tiles_p = ""
    tiles_s = ""
    tiles_j = ""
    tehai_count = 0
    aka_count = 0

    # アガリ牌
    wintile = {}

    # 設定のリセット
    config.is_riichi = False
    config.is_tsumo = False
    config.is_daburu_riichi = False
    config.is_ippatsu = False

    # GUIのリセット
    tehai_canvas.delete("all")
    agari_canvas.delete("all")
    culc_button['state'] = False

# オプションの設定
def set_option(option):
    global config

    if( option == 'riichi' ):
        config.is_riichi = True
    elif( option == 'tsumo' ):
        config.is_tsumo = True
    elif( option == 'daburii' ):
        config.is_daburu_riichi == True
    elif( option == 'ippatu' ):
        config.is_ippatsu == True

if __name__ == '__main__':

    root = Tk()
    root.title("my first app")

    # 画像の読み込み
    img_m = []
    img_m.append(ImageTk.PhotoImage(Image.open('./img/_5m_aka.png')))
    for mans in range(9):
        img_m.append(ImageTk.PhotoImage(Image.open('./img/_'+ str(mans + 1) +'m.png')))

    img_p = []
    img_p.append(ImageTk.PhotoImage(Image.open('./img/_5p_aka.png')))
    for pins in range(9):
        img_p.append(ImageTk.PhotoImage(Image.open('./img/_'+ str(pins + 1) +'p.png')))

    img_s = []
    img_s.append(ImageTk.PhotoImage(Image.open('./img/_5s_aka.png')))
    for sous in range(9):
        img_s.append(ImageTk.PhotoImage(Image.open('./img/_'+ str(sous + 1) +'s.png')))

    img_j = []
    for ji in range(7):
        img_j.append(ImageTk.PhotoImage(Image.open('./img/_ji'+ str(ji + 1) +'.png')))
    

    frame1 = ttk.Frame(root, padding = 16)
    tehai_canvas_width = 17
    tehai_canvas = Canvas(frame1, bg = "green", width = 40 * tehai_canvas_width , height = 48)
    agari_canvas = Canvas(frame1, bg = "green", width = 40,                       height = 48)
    label1 = ttk.Label(frame1, text = '牌の入力', font=( "Helvetica" ,14 ,"bold"))

    config_label_1 = ttk.Label(
        frame1,
        text = '入力方法：チェックボックスにチェック　→　牌をクリック （入力したい場所のみにチェック）',
        font=( "Helvetica" ,10))
    config_label_2 = ttk.Label(
        frame1, 
        text = 'ドラ，裏ドラ：表示牌を入力',
        font=( "Helvetica" ,10))

    frame1.grid(row = 0, column = 0)
    label1.grid(row = 0, column = 0, columnspan = tehai_canvas_width + 2)
    config_label_1.grid(row = 1, column = 0, columnspan = tehai_canvas_width + 2)
    config_label_2.grid(row = 2, column = 0, columnspan = tehai_canvas_width + 2)

    # 風牌の入力場所
    row_setting = 5
    column_setting = 0

    kaze_button = []
    kaze_checkvar = []
    kaze_canvas = []

    kaze_checkvar.append(BooleanVar(value = False))
    kaze_checkvar.append(BooleanVar(value = False))

    kaze_button.append( Checkbutton(frame1, text = "場風", variable = kaze_checkvar[0]) )
    kaze_button.append( Checkbutton(frame1, text = "自風", variable = kaze_checkvar[1]) )

    kaze_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )
    kaze_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )

    kaze_button[0].grid(row = row_setting - 2, column = column_setting,     columnspan  =2)
    kaze_button[1].grid(row = row_setting - 2, column = column_setting + 2, columnspan  =2)

    kaze_canvas[0].grid(row = row_setting - 1, column = column_setting,     columnspan  =2)
    kaze_canvas[1].grid(row = row_setting - 1, column = column_setting + 2, columnspan  =2)

    # ドラの入力場所
    dora_button = []
    dora_checkvar = []
    dora_canvas = []

    uradora_button = []
    uradora_checkvar = []
    uradora_canvas = []

    for i in range(5):
        dora_checkvar.append( BooleanVar(value = False) )
        uradora_checkvar.append( BooleanVar(value = False) )

    dora_button.append( Checkbutton(frame1, text = "ドラ", variable = dora_checkvar[0]) )
    dora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )

    uradora_button.append( Checkbutton(frame1, text = "裏ドラ", variable = uradora_checkvar[0]) )
    uradora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )

    for i in range(4):
        dora_button.append( Checkbutton(frame1, text = "カンドラ" + str(i + 1), variable = dora_checkvar[i + 1]) )
        dora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )
        uradora_button.append( Checkbutton(frame1, text = "裏ドラ" + str(i + 2), variable = uradora_checkvar[i + 1]) )
        uradora_canvas.append( Canvas(frame1, bg = "green", width = 40 , height = 48) )
    
    for i in range(5):
        dora_button[i].grid(row = row_setting,     column = i * 2, columnspan = 2)
        dora_canvas[i].grid(row = row_setting + 1, column = i * 2, columnspan = 2)
        uradora_button[i].grid(row = row_setting + 2, column = i * 2, columnspan = 2)
        uradora_canvas[i].grid(row = row_setting + 3, column = i * 2, columnspan = 2)

    # ここまで

    # 計算ボタンの配置
    culc_button = ttk.Button(
        frame1, 
        text = "計算", 
        command = lambda : culc_result(),
        state = DISABLED
        )
    culc_button.grid(row = row_setting + 5, column = tehai_canvas_width + 2)
    # ここまで

    tehai_check = BooleanVar(value = False)
    tehai_button = Checkbutton(frame1, text = "手牌", variable = tehai_check)
    tehai_button.grid(row = row_setting + 4, column = 0, columnspan = tehai_canvas_width)
    tehai_canvas.grid(row = row_setting + 5, column = 0, columnspan = tehai_canvas_width)

    wintile_check = BooleanVar(value = False)
    wintile_bottun = Checkbutton( frame1, text = "アガリ牌", variable = wintile_check)
    wintile_bottun.grid(row = row_setting + 4, column = tehai_canvas_width + 1)
    agari_canvas.grid(row = row_setting + 5, column = tehai_canvas_width + 1)

    # オプションを決定するボタン
    option_button_1 = ttk.Button(
        frame1,
        text = "立直",
        command = lambda : set_option('riichi'),
        ).grid(row = row_setting + 6, column = 0, columnspan = 2)
    
    option_button_2 = ttk.Button(
        frame1,
        text = "ダブル立直",
        command = lambda : set_option('daburii'),
        ).grid(row = row_setting + 6, column = 2, columnspan = 2)

    option_button_3 = ttk.Button(
        frame1,
        text = "ツモ",
        command = lambda : set_option('tsumo'),
        ).grid(row = row_setting + 6, column = 4, columnspan = 2)

    option_button_3 = ttk.Button(
        frame1,
        text = "一発",
        command = lambda : set_option('ippatu'),
        ).grid(row = row_setting + 6, column = 6, columnspan = 2)

    # 入力ボタンの生成
    row_input = row_setting + 8
    make_inputbutton( row_input )

    # リセットボタンの作成
    reset_button_1 = ttk.Button(
        frame1,
        text = "手牌reset",
        command = lambda : reset_hand(),
        ).grid(row = row_input + 5, column = 0, columnspan = 2)
    
    root.mainloop()
