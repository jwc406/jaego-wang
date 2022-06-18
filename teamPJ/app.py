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
global urlNewB
global urlVans
global dataSet
dataSet=[]

@app.route('/info', methods=['POST'])
def home_html():
    if request.method == 'POST':
        nikeCrwal(dataSet)
        newBCrawl(dataSet)
        vansCrawl(dataSet)
        return render_template("parsedInfo.html", parsed_page=dataSet)


def nikeCrwal(dataSet):
        try:
            urlNike = request.form[u'urlNike']
        except:
            return;
        
        
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
        e = []
        e.append(itemName)
        e.append(itemImg)
        e.append(itemStock)

        if e in dataSet:
            return
        
        dataSet.append(e)
        #dataSet.append(itemStockSize)  

def newBCrawl(dataSet):
        try:
            urlNewB = request.form[u'urlNewB']
        except:
            return ;

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

        e = []
        e.append(itemName)
        e.append(itemImg)
        e.append(itemStock)
       
        if e in dataSet:
            return
        
        dataSet.append(e)
        #dataSet.append(itemStockSize)  

def vansCrawl(dataSet):
        try:
            urlVans = request.form[u'urlVans']
        except:
            return ;
        print("Crawling initiating")
        session = HTMLSession()
        r = session.get(urlVans)
        #r.html.render(sleep=1, keep_page=True)

        itemName = r.html.find('div.product-summary > h1')[0].text
        itemImg = r.html.find('ul.thumb-wrap>li>a>img')[0]
        itemImg = itemImg.attrs['src']
        itemImg = itemImg[0 : -10]
        itemStock = r.html.find('#wrapper > main > section > div.pdp-container > div.pdp-main.row.flex-no-gutters > div:nth-child(2) > div > div.fixit-element.pdp-info > form > div.product-variations-action > div > div > span')
        
        if len(itemStock)>0:
            itemStock = False
        else:
             itemStock = True

        e = []
        e.append(itemName)
        e.append(itemImg)
        e.append(itemStock)
       
        if e in dataSet:
            return
        
        dataSet.append(e)
        #dataSet.append(itemStockSize)  

@app.route('/')
def inputURL_html():
    return render_template('inputURL.html')

if __name__=='__main__':
    try:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument('--listen-port', type=str, required=True, help='REST service listen port')
        args = parser.parse_args()
        listen_port = args.listen_port
    except Exception as e:
        print('Error: %s' % str(e))
