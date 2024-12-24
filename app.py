# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 20:59:32 2024

@author: Javier
"""

from flask import Flask, render_template, request, redirect, url_for
import qrcode
import io
import base64
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_wifi_password():
    url = 'https://d7r770yselozr.cloudfront.net/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        pwd_element = soup.find(id='pwd')
        if pwd_element:
            return pwd_element.get_text()
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form['WLGUEST']
        security_type = request.form['WP2']
        wifi_password = get_wifi_password()
        
        if wifi_password:
            wifi_config = f"WIFI:T:{security_type};S:{ssid};P:{wifi_password};;"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(wifi_config)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return render_template('index.html', img_str=img_str)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
