#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 18:08:05 2019

@author: james
"""
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
from ib.ext.EClientSocket import EClientSocket
import ib.ext.EWrapper # receiving msg
import ib.ext.EClientSocket # send msg
from ib.ext.ScannerSubscription import ScannerSubscription

from datetime import datetime
import time
import pandas as pd
import threading

import numpy as np


from IBWrapper import IBWrapper, contract


class orderRunner():
    
    def __init__(self,datadecoder):
        self.accountName = "asd781821"
        self.callback = IBWrapper()
        self.tws = EClientSocket(self.callback)
        self.host = ""
        self.port = 4003
        self.clientId = 9
        self.tws.eConnect(self.host, self.port, self.clientId)
        self.dd = datadecoder
        self.create = contract()
        self.callback.initiate_variables()
        self.callback.initiate_variables()
        self.tws.reqAccountSummary(9,'All','TotalCashValue')
        self.filedf =datadecoder.usabledf
        self.datadecoder = datadecoder
        
        
    def create_order(self,order_type, quantity, action):
        """Create an Order object (Market/Limit) to go long/short.
        
        order_type - 'MKT', 'LMT' for Market or Limit orders
        quantity - Integral number of assets to order
        action - 'BUY' or 'SELL'"""
        order = Order()
        order.m_orderType = order_type
        order.m_totalQuantity = quantity
        order.m_action = action
        return order

    def buy(self,contract_Details):
        self.tws.reqIds(-1)
        oid = self.callback.next_ValidId
        order = self.create_order('MKT', 300000, 'BUY')
        self.tws.placeOrder(oid, contract_Details, order)
        time.sleep(2)
        print('|==========执行触发=================|')
        print('|执行时期:%s|'%datetime.now())
        print('|操作: BUY                        |')
        print('|执行前总额:%s'%self.callback.account_Summary[-1][3])
        print('|===================================|')
        self.tws.reqIds(-1)
        time.sleep(420)
        oid = self.callback.next_ValidId
        order = self.create_order('MKT', 300000, 'SELL')
        self.tws.placeOrder(oid, contract_Details, order)
        self.tws.reqIds(-1)
        time.sleep(2)
        print('|==========结束执行触发=============|')
        print('|执行时期:%s|'%datetime.now())
        print('|操作: BUY-FINISH                  |')
        print('|执行后总额:%s               |'%self.callback.account_Summary[-1][3])
        print('|===================================|')

    
    def sell(self,contract_Details):
        self.tws.reqIds(-1)
        oid = self.callback.next_ValidId
        order = self.create_order('MKT', 300000, 'SELL')
        self.tws.placeOrder(oid, contract_Details, order)
        time.sleep(2)
        print('|==========执行触发=================|')
        print('|执行时期:%s|'%datetime.now())
        print('|操作: SELL                         |')
        print('|执行前总额:%s               |'%self.callback.account_Summary[-1][3])
        print('|===================================|')
        self.tws.reqIds(-1)
        time.sleep(420)
        oid = self.callback.next_ValidId
        order = self.create_order('MKT', 300000, 'BUY')
        self.tws.placeOrder(oid, contract_Details, order)
        print('sell order finished')
        self.tws.reqIds(-1)
        time.sleep(2)
        print('|==========结束执行触发=============|')
        print('|执行时期:%s|'%datetime.now())
        print('|操作: SELL-FINISH                  |')
        print('|执行后总额:%s               |'%self.callback.account_Summary[-1][3])
        print('|===================================|')
        self.globalid = oid
        
        
    def run(self):
        tickerId = 9010
        while(1):
            contract_Details = self.create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
            '''self.tws.reqCurrentTime()
            time.sleep(1)
            ts = self.callback.current_Time
            data_endtime = datetime.utcfromtimestamp(ts).strftime('%Y%m%d  %H:%M:%S')'''
    
            tickerId += 1
            self.tws.reqHistoricalData(tickerId = tickerId, 
                      contract = contract_Details, 
                      endDateTime = '',
                      durationStr="1 D",
                      barSizeSetting = "1 min", 
                      whatToShow = "BID", 
                      useRTH = 0, 
                      formatDate = 1)

            time.sleep(3)

            data= pd.DataFrame(self.callback.historical_Data, 
                   columns = ["reqId", "date", "open",
                              "high", "low", "close", 
                              "volume", "count", "WAP", 
                              "hasGaps"])[-500:-1]
            self.dd.findMatch(data)
            
            
            for b in self.dd.reversedBucket:
                print('|=============================================|')
                print('|检测到基因:%s|'%b)
                print('|=============================================|')
                if(self.filedf.index.contains(b)):
                    tempdf = self.filedf.loc[b]
                    if(tempdf['r7mean'] > 0):
                        threading.Thread(target=self.buy,args = [contract_Details]).start()
                    else:
                        threading.Thread(target=self.sell,args = [contract_Details]).start()
    
            time.sleep(60)
    def dc(self):
        self.tws.eDisconnect()