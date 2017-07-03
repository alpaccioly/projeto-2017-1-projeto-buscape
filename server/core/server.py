from flask import Flask, request, json, jsonify, send_from_directory
from data_set import DataSet
from analyser import Analyser
import json
import os

DATA_SET_PATH = os.environ['DATA_SET_PATH']
TRAIN_HEADER = os.environ['TRAIN_HEADER']

if DATA_SET_PATH is None:
    DATA_SET_PATH = 'resources/data.csv'
if TRAIN_HEADER is None:
    TRAIN_HEADER = 'preco'

app = Flask(__name__)

ds = DataSet.init_from_file(DATA_SET_PATH, TRAIN_HEADER)


@app.route('/categories', methods=['GET'])
def categories():
    categories = []
    ds.print_config()
    print("### DS CATEGORIES ###\n" + str(ds.categories))
    print("### categories size: " + str(len(ds.categories)))

    for k,v in ds.headers_map.items():
        cat = {}
        cat["name"] = k
        cat["id"] = v
        cat["groups"] = ds.categories[v]
        categories.append(cat)
    return str(categories)

@app.route('/', methods=['GET'])
def hello():
    return "Hello Analyser!"

@app.route('/analyse', methods=['POST'])
def analyse():
    input_json = request.get_json()
    filters_dict = input_json['filters']

    for k,v in filters_dict.items():
        del filters_dict[k]
        filters_dict[int(k)] = v

    category = input_json['category']
    print("filters_dict:\n" + str(filters_dict))
    print("category: "  + str(category))
    coefs = Analyser.analyse(filters_dict, category, ds)
    print("Coeficientes: " + str(coefs))
    print("coef type:" + str(type(coefs)))
    return json.dumps(coefs.tolist())


ds.print_config()













