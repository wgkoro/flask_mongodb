#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from logging import Formatter, FileHandler
from logging.handlers import RotatingFileHandler
from mongodb import MongoDB
import logging
import socket
import re
import os

SAKELIST = ('sake', 'beer', 'vocka', 'whisky')

app = Flask(__name__)

""" logging config """
handler = RotatingFileHandler(os.path.join(app.root_path, 'syslog/system.log'), mode='a', maxBytes=100000, backupCount=10)
handler.setFormatter(Formatter("%(levelname)s [%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    db = MongoDB(app)
    if request.method == 'POST':
        sake_data = check_request_set(request)
        if not sake_data:
            message = 'Error'
        else:
            db.set_sake(sake_data)
            message = 'Success!'

    return render_template('index.html', message=message)


@app.route('/search', methods=['GET', 'POST'])
def regist():
    message = None
    db = MongoDB(app)
    sake_list = []
    if request.method == 'POST':
        sake_name = check_request_get(request)
        if not sake_name:
            message = 'Error'
        else:
            sake_list = db.get_sake(sake_name)
            message = '%s people found' % len(sake_list)

    return render_template('search.html', message=message, sake_list=sake_list)


def check_request_set(request):
    data = {
        'name'  : '',
        'sake'  : [],
    }
    name = request.form.get('name', '')
    if not name:
        return False
    else:
        data['name'] = name

    sake_list = []
    sake_list.append(request.form.get('sake', ''))
    sake_list.append(request.form.get('beer', ''))
    sake_list.append(request.form.get('vocka', ''))
    sake_list.append(request.form.get('whisky', ''))

    for sake in sake_list:
        if sake:
            data['sake'].append(sake)

    if not data['sake']:
        return False
    else:
        return data


def check_request_get(request):
    sake_name = request.form.get('request', '')
    if sake_name in SAKELIST:
        return sake_name
    else:
        return False





if __name__ == '__main__':
    host = socket.gethostname()
    p = re.compile('.+\.local$')
    if p.match(host):
        print 'Now Debugging...'
        app.debug = True

    app.run()
