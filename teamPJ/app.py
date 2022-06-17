#!/usr/bin/python

import argparse
import subprocess
import requests
import lxml
import time
from requests_html import HTMLSession
from flask import Flask, jsonify, request
from flask import render_template

app = Flask(__name__)

global urlNike
global urlAdidas
global urlNewB



@app.route('/info', methods=['POST'])
def home_html():
    if request.method == 'POST':
        dataSet=[]
        #nikeCrwal(dataSet)
        NewBCrawl(dataSet)
        return render_template("home.html", parsed_page=dataSet)


def nikeCrwal(dataSet):
        urlNike = request.form[u'urlNike']

        print("Crawling initiating")
        session = HTMLSession()
        r = session.get(urlNike)
        #r.html.render(sleep=1, keep_page=True)

        itemName = r.html.find('span.tit')[0].text
        itemImg = r.html.find('div.prd-gutter>img')[4]
        itemImg = itemImg.attrs['src']
        itemStock = r.html.find('span.comming')[0].text
        
        if(itemStock=="상품이 품절되었습니다."):    #품절되면 False
            itemStock=False
        else:
            itemStock=True

        #itemStockSize = r.html.find('span.input-radio')   #사이즈별로 재고 불러오기 구현 X          

        dataSet.append(itemName)
        dataSet.append(itemImg)
        dataSet.append(itemStock)
        #dataSet.append(itemStockSize)  

def NewBCrawl(dataSet):
        urlNewB = request.form[u'urlNewB']

        print("Crawling initiating")
        session = HTMLSession()
        r = session.get(urlNewB)
        #r.html.render(sleep=1, keep_page=True)

        itemName = r.html.find('h2.title')[0].text
        itemImg = r.html.find('div.inner>img')[0]
        itemImg = itemImg.attrs['src']
        itemStock = r.html.find('#optSizeSection > ul > li > input')

        cnt=0
        for stock in itemStock:
            if 'disabled' in stock.attrs:
                cnt+=1
        
        if cnt == len(itemStock):
            itemStock = False
        else:
            itemStock = True

        dataSet.append(itemName)
        dataSet.append(itemImg)
        dataSet.append(itemStock)
       
        #dataSet.append(itemStockSize)  

@app.route('/')
def infoParsed_html():
    return render_template('infoParsed.html')

if __name__=='__main__':
    try:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument('--listen-port', type=str, required=True, help='REST service listen port')
        args = parser.parse_args()
        listen_port = args.listen_port
    except Exception as e:
        print('Error: %s' % str(e))
