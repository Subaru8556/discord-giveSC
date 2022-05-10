#ライブラリインポート
import datetime
import discord
from discord.ext import commands
import os
from PIL import Image,ImageFilter,ImageDraw,ImageFont
import random
import requests
import textwrap
import tkinter

#以下GUI処理
#トークンの保存
def button_save():
    text = textbox.get()
    file = open('token.txt','w')
    file.write(text)
    file.close()

#GUIの終了
def button_quit():
    window.destroy()

#トークンが設定済みか確認
if os.path.isfile('token.txt') != True:
    #トークン未設定
    #GUIの設定
    window = tkinter.Tk()
    window.geometry('670x220')
    window.title('トークンの設定')
    label_1 = tkinter.Label(text='Discord Botのトークンをここに入力')
    label_1.place(x=30,y=10)
    textbox = tkinter.Entry(width=100)
    textbox.place(x=30,y=50)
    button_1 = tkinter.Button(window, text='トークンを保存する', command=button_save)
    button_1.place (x=30,y=90)
    label_2 = tkinter.Label(justify="left", text='トークンを一度設定すると再度このGUIは開きません\nトークンを再設定したい場合は「token.txt」を一度削除してから再びこのプログラムを実行してください')
    label_2.place(x=30,y=130)
    button_2 = tkinter.Button(window, text='Botを起動する', command=button_quit)
    button_2.place(x=30,y=180)
    #GUIの開始
    window.mainloop()

#トークンの読み込み
file = open('token.txt','r')
text = file.read()
file.close()
#トークンの設定
TOKEN = text

# 接続に必要なオブジェクトを生成
discord.http.API_VERSION = 9
bot = commands.Bot(command_prefix='!')

# 以下bot処理
#アイコン保存
def save_avater(url,name):
    responce = requests.get(url).content
    os.makedirs('tmp',exist_ok=True)
    with open(os.path.join('tmp',name + '.png'),mode='wb') as f:
        f.write(responce)
    img = Image.open('tmp/' + name + '.png')
    img_resize = img.resize((256,256))
    img_resize.save('tmp/' + name + '.png')

#金額の設定
def set_value(val):
    value = random.randint(100,50000)
    if len(val) != 0:
        value_str = val[0]
        do = False
        try:
            value = int(value_str)
        except ValueError:
            if len(val) != 1:
                do = True
            else:
                value = random.randint(100,50000)
        if do:
            value_str = val[1]
            try:
                value = int(value_str)
            except ValueError:
                value = random.randint(100,50000)
    return value

#テキストの設定
def set_text(val):
    is_first = False
    do = False
    value = val[0]
    try:
        i = int(value)
    except ValueError:
        do = True
    if do:
        value = val[1]
        try:
            i = int(val)
        except ValueError:
            do = False
        if do:
            is_first = True
    if is_first:
        text = val[0]
    else:
        if len(val) == 1:
            text = val[1]
        else:
            num = len(val)
            text = ""
            for i in range(num):
                if i != 0:
                    text = text + val[i]
                i = i + 1
    return text

#金額部分の画像生成
def make_sc_value(name,value,user_name):
    #金額テキストの生成
    value_text = '¥' + format(value,',')
    #色の決定
    if value < 200:
        img_path = "asset/blue.png"
        color = True
    elif value < 500:
        img_path = "asset/light_blue.png"
        color = False
    elif value < 1000:
        img_path = "asset/green.png"
        color = False
    elif value < 2000:
        img_path = "asset/yellow.png"
        color = False
    elif value < 5000:
        img_path = "asset/orange.png"
        color = True
    elif value < 10000:
        img_path = "asset/magenta.png"
        color = True
    else:
        img_path = "asset/red.png"
        color = True

    #背景色+アイコンの画像生成
    img_bg = Image.open(img_path)
    img_sc = img_bg.copy()
    img_avater = Image.open('tmp/' + name + '.png')
    img_alpha = Image.open('asset/avater_mask.png').convert('L')
    img_alpha_blur = img_alpha.filter(ImageFilter.GaussianBlur(1))
    img_sc.paste(img_avater,(30,22),img_alpha_blur)

    #テキスト追加
    draw = ImageDraw.Draw(img_sc)
    font_text = ImageFont.truetype('asset/meiryo.ttc',90)
    font_num = ImageFont.truetype('asset/Roboto-Regular.ttf',90)
    if color:
        draw.text((350,30),user_name,font=font_text,fill='#ffffff')
        draw.text((350,150),value_text,font=font_num,fill='#ffffff')
    else:
        draw.text((350,30),user_name,font=font_text,fill='#2b2b2b')
        draw.text((350,150),value_text,font=font_num,fill='#2b2b2b')
    img_sc.save('tmp/' + name + '_sc_title.png')

#テキスト部分の画像生成
def make_sc_text(name,value,text):
    #色の決定
    if value < 500:
        img_path = "asset/light_blue_comment.png"
        color = False
    elif value < 1000:
        img_path = "asset/green_comment.png"
        color = False
    elif value < 2000:
        img_path = "asset/yellow_comment.png"
        color = False
    elif value < 5000:
        img_path = "asset/orange_comment.png"
        color = True
    elif value < 10000:
        img_path = "asset/magenta_comment.png"
        color = True
    else:
        img_path = "asset/red_comment.png"
        color = True

    #テキスト量に応じた画像生成
    img_bg = Image.open(img_path)
    img_sc = img_bg.copy()
    warp_list = textwrap.wrap(text,20)
    num = len(warp_list) * 70 + 70
    img_sc = img_sc.resize((1500,num))

    #テキスト追加
    draw = ImageDraw.Draw(img_sc)
    font_text = ImageFont.truetype('asset/meiryo.ttc',70)
    line_counter = 0
    for line in warp_list:
        y = line_counter * 70 + 25
        if color:
            draw.multiline_text((55,y),line,font=font_text,fill='#ffffff')
        else:
            draw.multiline_text((55,y),line,font=font_text,fill='#2b2b2b')
        line_counter = line_counter + 1
    img_sc.save('tmp/' + name + '_sc_text.png')

#金額+テキストの画像生成
def make_sc(name):
    img_title = Image.open('tmp/' + name + '_sc_title.png')
    img_text = Image.open('tmp/' + name + '_sc_text.png')
    tmp = Image.new('RGB',(img_title.width, img_title.height + img_text.height))
    tmp.paste(img_title, (0,0))
    tmp.paste(img_text, (0,img_title.height))
    tmp.save('tmp/' + name + '_sc.png')

    #不要になったファイルの削除
    os.remove('tmp/' + name + '_sc_title.png')
    os.remove('tmp/' + name + '_sc_text.png')

# 以下botイベント
# 起動時に動作する処理
@bot.event
async def on_ready():
    print(f'{bot.user}としてログインしました')

#SC画像の生成
@bot.command()
async def sc(ctx,*val):
    #ユーザー名・アイコンURLの取得
    id = ctx.author.id
    user = await bot.fetch_user(id)
    avater_url = user.display_avatar
    user_name = user.display_name

    #ファイル名を決定するための日時を取得
    d = datetime.datetime.now()
    date = d.strftime('%Y%m%d%H%M%S')

    #アイコンを保存
    save_avater(avater_url,date)

    #金額の変数を取得
    value = set_value(val)

    #SC上部画像の生成
    make_sc_value(date,value,user_name)

    if(len(val) > 1):
        if(value > 199):
            #テキストの変数を取得
            text = set_text(val)

            #SC下部の画像を生成
            make_sc_text(date,value,text)

            #2枚の画像を1枚に
            make_sc(date)
        else:
            #ファイルのリネーム
            os.rename('tmp/' + date + '_sc_title.png','tmp/' + date + '_sc.png')
    else:
        #ファイルのリネーム
        os.rename('tmp/' + date + '_sc_title.png','tmp/' + date + '_sc.png')
    #生成した画像の送信
    await ctx.send(file=discord.File('tmp/' + date + '_sc.png'))

    #不要になったファイルの削除
    os.remove('tmp/' + date + '.png')
    os.remove('tmp/' + date + '_sc.png')

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)