import os
import sys

import json

import pandas as pd
from flask import Flask, escape, url_for, render_template, request


#skl is the short for skeleton
DOGS_FOLDER = os.path.join('static', 'dog-validation-images')
SKL_FOLDER = os.path.join('static', 'dog-validation-skeletons')

app = Flask(__name__)
app.config['DOGS_FOLDER'] = DOGS_FOLDER
app.config['SKL_FOLDER'] = SKL_FOLDER

IMPATH_FULL = '/Users/frappuccino/dev/Data annotator/static/dog-validataion-images/'
SKLPATH_FULL = '/Users/frappuccino/dev/Data annotator/static/dog-validation-skeletons/'

all_imgs = pd.Series([x.split('/')[-1].split('.')[0] for x in os.listdir(SKLPATH_FULL)])

def get_img_id():
    annotated_imgs = pd.read_csv("db.csv", sep=',')['IMAGEID']
    available_imgs = all_imgs[~all_imgs.isin(annotated_imgs)]
    return available_imgs.iloc[0]

@app.route('/annotate')
def annotator_render():
    img_id = get_img_id()
    img_url = os.path.join(app.config['DOGS_FOLDER'], f'{img_id}.jpg')
    skl_url = os.path.join(app.config['SKL_FOLDER'], f'{img_id}.png')
    return render_template('template.html', img_url=img_url, skl_url=skl_url, img_id=img_id)

@app.route('/store', methods=['POST'])
def store():
    obj = request.json
    img_id = obj['ImageID']
    result = obj['Result']
    comment = obj['Comment'] 
    with open("db.csv", "a") as fs:
        fs.write(f"\n{img_id},{result},{comment}")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    app.run('0.0.0.0', port=int(sys.argv[1]), debug=True)