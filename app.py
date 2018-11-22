# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Markup
import os
import json
import re
from numpy.random import choice, seed
import hashlib
import datetime

app = Flask(__name__)

DEBUG = False

def pick_up_message():
    welcome_messages = [
        'こんにちは、あなたの名前を入力してください',
        'やあ！お名前は何ですか？',
        'あなたの名前を教えてね'
    ]
    # NumPy の choice でランダムにメッセージ出力する
    return choice(welcome_messages)

def select_tank(tank_seed):
    tanks = {
        'hoge1':'1',
        'hoge2':'2',
        'hoge3':'3',
        'hoge4':'4',
        'hoge5':'5',
        'hoge6':'6',
        'hoge7':'7',
        'hoge8':'8',
        'hoge9':'9',
        'hoge10':'10',
        'hoge11':'11',
        'hoge12':'12'
    }

    seed(tank_seed)

    tanks_list = list(tanks.items())

    tank_name, tank_num = tanks_list[choice(len(tanks_list))]

    return tank_name, tank_num

def select_charactor(chara_seed, need_number):
    charactors = [
        'fuga1',
        'fuga2',
        'fuga3',
        'fuga4',
        'fuga5',
        'fuga6',
        'fuga7',
        'fuga8',
        'fuga9',
        'fuga10',
        'fuga11',
        'fuga12',
        'fuga13',
        'fuga14',
        'fuga15',
        'fuga16',
        'fuga17',
        'fuga18',
        'fuga19',
        'fuga20',
        'fuga21',
        'fuga22'
    ]

    seed(chara_seed)

    return choice(charactors,need_number,replace=False)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', welcome_message=pick_up_message())

@app.route('/search')
def search():

    # 入力された名前を取得
    inputed_username = request.args.get('username')

    # 当日の日時を取得
    dt_now = datetime.datetime.now()
    # 取得した日時を文字列に変換
    # daytime = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    daytime = dt_now.strftime('%Y%m%d%H')

    # 取得した名前と日時からハッシュ値を生成
    prehashed = inputed_username + daytime
    sha1 = hashlib.sha1(prehashed.encode()).hexdigest()
 
    print(sha1)

    seed_str = re.sub(r'\D', '', sha1)

    if len(seed_str) == 0:
        seed = 0
    elif len(seed_str) >= 1 and len(seed_str) <= 5:
        seed = int(seed_str)
    else:
        seed = int(seed_str[0:5])

    print(seed)

    tank_name, tank_num = select_tank(seed)

    chara = select_charactor(seed,int(tank_num))

    response = tank_name + ' ho: ' + ','.join(map(str, chara))

    if 'ブラック注意' in response:
        backcolor = 'black'
        textcolor = 'red'
    else:
        backcolor = 'white'
        textcolor = 'black'

    htmlsrc = Markup('<div class=\'row\'><div class=\'col s12 \'><div class=\'card ' + backcolor + ' darken-1\'><div class=\'card-content ' + textcolor + '-text\'><span class=\'card-title\'>' + inputed_username + '</span><p>' + response + '</p></div></div></div></div>')

    return render_template('search.html', message=htmlsrc)

if os.getenv('VCAP_APP_PORT'):
    host = '0.0.0.0'
    port = int(os.getenv('VCAP_APP_PORT'))
else:
    # ローカル用の設定
    host = '127.0.0.1'
    port = 5000

if __name__ == '__main__':
    if DEBUG:
        app.run(host=host, port=port, threaded=False, debug=True)
    else :
        app.run(host=host, port=port, threaded=True)