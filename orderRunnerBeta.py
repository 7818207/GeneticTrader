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
import beta_quickEngine as bqe

from datetime import datetime
import time
import pandas as pd
import threading

import numpy as np
import schedule
import ast
from IBWrapper import IBWrapper, contract

import beta_quickEngine as bqe


class orderRunnerBeta:
    
    def __init__(self,datadecoder):
        self.accountName = "asd781820"
        self.callback = IBWrapper()
        self.tws = EClientSocket(self.callback)
        self.host = ""
        self.port = 4002
        self.clientId = 8
        self.tws.eConnect(self.host, self.port, self.clientId)
        self.dd = datadecoder
        self.create = contract()
        self.callback.initiate_variables()
        self.callback.initiate_variables()
        self.tws.reqAccountSummary(8,'All','TotalCashValue')
        self.filedf =datadecoder.usabledf
        self.datadecoder = datadecoder
        contract_Details = self.create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
        tickerId = 10000
        self.tws.reqRealTimeBars(tickerId,contract_Details,5,"MIDPOINT",0)
        self.tickerId = 9010
        self.df = pd.read_csv('df.csv')
        self.RbinDict = bqe.makeRDf(self.df)
        self.column_index_value_dict,self.binDict = bqe.makeDf(self.df)
        
        
        
        
    def create_trailing_order(self,action,quantity,trailingPercent = 0.006):
        order = Order()
        order.m_orderType = "TRAIL"
        order.m_totalQuantity = quantity
        order.m_trailingPercent = trailingPercent
        order.m_action = action
        return order
    
    def create_order(self,order_type,quantity, action):
        """Create an Order object (Market/Limit) to go long/short.
        
        order_type - 'MKT', 'LMT' for Market or Limit orders
        quantity - Integral number of assets to order
        action - 'BUY' or 'SELL'"""
        order = Order()
        order.m_orderType = order_type
        order.m_totalQuantity = quantity
        order.m_action = action
        return order

    def buy(self,contract_Details,limit,stop):

        
        self.tws.reqIds(-1)
        time.sleep(0.5)
        oid = self.callback.next_ValidId
        parent = Order()
        parent.orderId = oid
        parent.m_action = "BUY"
        parent.m_orderType = "MKT"
        parent.m_totalQuantity = 300000
        parent.m_transmit = False
        print('|==========执行触发=================|')
        print('|执行时期:%s|'%datetime.now())
        print('|操作: BUY                        |')
        print('|执行前总额:%s'%self.callback.account_Summary[-1][3])
        print('|===================================|')
        self.tws.reqIds(-1)
        takeProfit = Order()
        takeProfit.orderId = parent.orderId + 1
        takeProfit.m_action = "SELL"
        takeProfit.m_orderType = "LMT"
        takeProfit.m_totalQuantity = 300000
        takeProfit.m_lmtPrice = limit
        takeProfit.m_parentId = oid
        takeProfit.m_transmit = False
        
        stopLoss = Order()
        stopLoss.orderId = parent.orderId + 2
        stopLoss.m_action = "SELL"
        stopLoss.m_orderType = "STP"
        #Stop trigger price
        stopLoss.m_auxPrice = stop
        stopLoss.m_totalQuantity = 300000
        stopLoss.m_parentId = oid
        stopLoss.m_transmit = True
        
        bracketOrder = [parent, takeProfit, stopLoss]
        
        for o in bracketOrder:
            self.tws.placeOrder(o.orderId, contract_Details, o)
            self.tws.reqIds(-1)
        time.sleep(1)
        time.sleep(2)

        

    
    def sell(self,contract_Details,limit,stop):
        self.tws.reqIds(-1)
        time.sleep(0.5)
        oid = self.callback.next_ValidId
        parent = Order()
        parent.orderId = oid
        parent.m_action = "SELL"
        parent.m_orderType = "MKT"
        parent.m_totalQuantity = 300000
        parent.m_transmit = False
        print('|==========执行触发=================|')
        print('|执行时期:%s|'%datetime.now())
        print('|操作: BUY                        |')
        print('|执行前总额:%s'%self.callback.account_Summary[-1][3])
        print('|===================================|')
        self.tws.reqIds(-1)
        takeProfit = Order()
        takeProfit.orderId = parent.orderId + 1
        takeProfit.m_action = "BUY"
        takeProfit.m_orderType = "LMT"
        takeProfit.m_totalQuantity = 300000
        takeProfit.m_lmtPrice = limit
        takeProfit.m_parentId = oid
        takeProfit.m_transmit = False
        
        stopLoss = Order()
        stopLoss.orderId = parent.orderId + 2
        stopLoss.m_action = "BUY"
        stopLoss.m_orderType = "STP"
        #Stop trigger price
        stopLoss.m_auxPrice = stop
        stopLoss.m_totalQuantity = 300000
        stopLoss.m_parentId = oid
        stopLoss.m_transmit = True
        
        bracketOrder = [parent, takeProfit, stopLoss]
        
        for o in bracketOrder:
            self.tws.placeOrder(o.orderId, contract_Details, o)
            self.tws.reqIds(-1)
        time.sleep(1)
        time.sleep(2)
        
    def job(self):
        contract_Details = self.create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
            #self.tws.reqCurrentTime()
            #time.sleep(1)
            #ts = self.callback.current_Time
            #data_endtime = datetime.utcfromtimestamp(ts).strftime('%Y%m%d  %H:%M:%S')
    
        self.tws.reqHistoricalData(tickerId = self.tickerId, 
                      contract = contract_Details, 
                      endDateTime = '',
                      durationStr="1 D",
                      barSizeSetting = "1 min", 
                      whatToShow = "BID", 
                      useRTH = 0, 
                      formatDate = 1)

        time.sleep(2)
        
        data= pd.DataFrame(self.callback.historical_Data, 
                   columns = ["reqId", "date", "open",
                              "high", "low", "close", 
                              "volume", "count", "WAP", 
                              "hasGaps"])[-500:-1]
        self.dd.findMatch(data)
        print(data)
        print(datetime.now())
            
        for b in self.dd.reversedBucket:
            print('|=============================================|')
            print('|检测到基因:%s|'%b)
            print('|=============================================|')
            if(self.filedf.index.contains(b)):
                stra = bqe.get_sharpe_stra(b)
                
                if(stra > 0):
                    threading.Thread(target=self.buy,args = [contract_Details,stra+1]).start()
                elif(stra < 0):
                    threading.Thread(target=self.sell,args = [contract_Details,abs(stra-1)]).start()
    
        self.tws.reqIds(-1)
        print('|===================================|')
        print('|总额:%s               |'%self.callback.account_Summary[-1][3])
        print('|===================================|')
        
    def run(self):
        print('|===========================================|')
        print('|=======欢迎使用beta版本，祝您好运==========|')
        print('|====新特性：1。止损定单 2。智能订单执行====|')
        print('|===========================================|')
        print('|===========================================|')
        self.tickerId = 9010
        
        
        while(1):
            now = datetime.now()
            if(now.second == 5):
                contract_Details = self.create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
            #self.tws.reqCurrentTime()
            #time.sleep(1)
            #ts = self.callback.current_Time
            #data_endtime = datetime.utcfromtimestamp(ts).strftime('%Y%m%d  %H:%M:%S')
    
                self.tws.reqHistoricalData(tickerId = self.tickerId, 
                      contract = contract_Details, 
                      endDateTime = '',
                      durationStr="1 D",
                      barSizeSetting = "1 min", 
                      whatToShow = "BID", 
                      useRTH = 0, 
                      formatDate = 1)

                time.sleep(2)
        
                data= pd.DataFrame(self.callback.historical_Data, 
                   columns = ["reqId", "date", "open",
                              "high", "low", "close", 
                              "volume", "count", "WAP", 
                              "hasGaps"])[-500:-1]
                self.dd.findMatch(data)
            
                last_close = data.iloc[-1].close
                for b in self.dd.reversedBucket:
                    if(self.filedf.index.contains(b)):
                        print('usable gene: %s'%b)
                        limit,stop,action = bqe.get_monte_carlo_stra(ast.literal_eval(b),self.column_index_value_dict,self.binDict,self.df,self.RbinDict)
                        
                        
                        if(action > 0):
                            limit_price = last_close + limit
                            stop_price = last_close - stop
                            threading.Thread(target=self.buy,args = [contract_Details,limit_price,stop_price]).start()
                            
                        elif(action < 0):
                            limit_price = last_close - limit
                            stop_price = last_close + stop
                            threading.Thread(target=self.sell,args = [contract_Details,limit,stop]).start()
    
                self.tws.reqIds(-1)
                print('|===================================|')
                print('|总额:%s               |'%self.callback.account_Summary[-1][3])
                print('|===================================|')
    def dc(self):
        self.tws.eDisconnect()