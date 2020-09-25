from flask import Flask
from datetime import datetime, timedelta

import azure.functions as func
import logging

import requests
import json

app = Flask(__name__)

@app.route('/')
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    r = requests.get('https://api.bitcointrade.com.br/v3/public/BRLBTC/ticker')
    btc_cotacao = ""
    btc_cotacao_data = ""
    if r.status_code == 200:
        json = r.json()
        btc_cotacao = json['data']['buy']
        data = datetime.strptime(json['data']['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data -= timedelta(hours=3)
        btc_cotacao_data = data.strftime("%d/%m/%Y %H:%M:%S")

    r = requests.get('https://api.bitcointrade.com.br/v3/public/BRLETH/ticker')
    eth_cotacao = ""
    eth_cotacao_data = ""
    if r.status_code == 200:
        json = r.json()
        eth_cotacao = json['data']['buy']
        data = datetime.strptime(json['data']['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data -= timedelta(hours=3)
        eth_cotacao_data = data.strftime("%d/%m/%Y %H:%M:%S")

    r = requests.get('https://api.bitcointrade.com.br/v3/public/BRLBCH/ticker')
    bch_cotacao = ""
    bch_cotacao_data = ""
    if r.status_code == 200:
        json = r.json()
        bch_cotacao = json['data']['buy']
        data = datetime.strptime(json['data']['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data -= timedelta(hours=3)
        bch_cotacao_data = data.strftime("%d/%m/%Y %H:%M:%S")

    html = "<div style='position:relative'>\
        <div style='float:left; width: 33%; border: 1px solid black; height:100px; text-align: center;'><br>BTC<br>{}<br>{}\
        </div>\
        <div style='float:left; width: 33%; border: 1px solid black; height:100px; text-align: center;'><br>BCH<br>{}<br>{}\
        </div>\
        <div style='float:left; width: 33%; border: 1px solid black;height:100px; text-align: center;'><br>ETH<br>{}<br>{}\
        </div>\
    </div>".format(btc_cotacao_data, btc_cotacao,
    bch_cotacao_data, bch_cotacao,
    eth_cotacao_data, eth_cotacao)

    return func.HttpResponse(body=html, mimetype='text/html')