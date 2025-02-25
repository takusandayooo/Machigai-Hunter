from flask import Flask, request, render_template, redirect, url_for
import os
import time
from feature_matching_and_diff import feature_matching

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

@app.route('/')
def root_func_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def root_func_post():
    print("POST")
    
    if 'text' in request.form:
        print("has text in form") # textはここにある

    if 'img_name' in request.form:
        print("has img_name in form") # img_nameはここには無い
    
    if 'img_name' in request.files: # ここにある
        #フォルダーの中身を削除
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        files = os.listdir(UPLOAD_FOLDER)
        for file in files:
            os.remove(os.path.join(UPLOAD_FOLDER, file))
        files = request.files.getlist('img_name')

        for file in files:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    feature_matching()
    time.sleep(2)  # 2秒待つ
    return redirect(url_for('result_get'))

@app.route('/result')
def result_get():
    # feature_matching()
    return render_template('result.html')


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True,host="0.0.0.0",port=4000)