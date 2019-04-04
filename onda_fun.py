#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:29:21 2019

@author: james
"""
import requests
#a5b72e26f74b956c0768edf23b8064e5-5ebe088b151f7beea5b258a086222662


auth_token='a5b72e26f74b956c0768edf23b8064e5-5ebe088b151f7beea5b258a086222662'
hed = {'Authorization': 'Bearer ' + auth_token}

url = 'https://api-fxtrade.oanda.com/v1/accounts'

response = requests.post(url, headers=hed)