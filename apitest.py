# -*- coding: utf-8 -*-



def error_handler(msg):
    """Handles the capturing of error messages"""
    print ("Server Error: %s" % msg)

def reply_handler(msg):
    """Handles of server replies"""
    print ("Server Response: %s, %s" % (msg.typeName, msg))
    
    
def create_contract(symbol, sec_type, exch, prim_exch, curr):
    """Create a Contract object defining what will
    be purchased, at which exchange and in which currency.

    symbol - The ticker symbol for the contract
    sec_type - The security type for the contract ('STK' is 'stock')
    exch - The exchange to carry out the contract on
    prim_exch - The primary exchange to carry out the contract on
    curr - The currency in which to purchase the contract"""
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def create_order(order_type, quantity, action):
    """Create an Order object (Market/Limit) to go long/short.

    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    return order

class TestWrapper(ib.ext.EWrapper):
    pass

class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        
class TestApp(TestWrpper, TestClient):
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)


if __name__ == "__main__":
    # Connect to the Trader Workstation (TWS) running on the
    # usual port of 7496, with a clientId of 100
    # (The clientId is chosen by us and we will need 
    # separate IDs for both the execution connection and
    # market data connection)
    conn = Connection.create(port=4002, clientId=100)
    conn.connect()

    # Assign the error handling function defined above
    # to the TWS connection
    conn.register(error_handler, 'Error')

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    conn.registerAll(reply_handler)

    # Create an order ID which is 'global' for this session. This
    # will need incrementing once new orders are submitted.
    order_id = 1889

    # Create a contract in GOOG stock via SMART order routing

    
    contract = create_contract('EUR', 'CASH', 'IDEALPRO', 'IDEALPRO', 'USD')
    

    # Go long 100 shares of Google
    order = create_order('MKT', 100000, 'SELL')

    # Use the connection to the send the order to IB
    tws.placeOrder(order_id, contract, order)

    # Disconnect from TWS
    conn.disconnect()



from IBWrapper import IBWrapper, contract
accountName = "asd781820"
callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 4002
clientId = 8

tws.eConnect(host, port, clientId)

create = contract()
callback.initiate_variables()
tws.reqAccountUpdates(1,accountName)




acc = pd.DataFrame(callback.update_AccountValue,
             columns= ['key','value','currency','accountName'])[:3]


accport = pd.DataFrame(callback.update_Portfolio, 
             columns=['Contract ID','Currency',
                      'Expiry','Include Expired',
                      'Local Symbol','Multiplier',
                      'Primary Exchange','Right',
                      'Security Type','Strike',
                      'Symbol','Trading Class',
                      'Position','Market Price','Market Value',
                      'Average Cost', 'Unrealised PnL', 'Realised PnL', 
                      'Account Name'])[:3]
    
dat = pd.DataFrame(callback.position, 
                   columns=['Account','Contract ID','Currency','Exchange','Expiry',
                            'Include Expired','Local Symbol','Multiplier','Right',
                            'Security Type','Strike','Symbol','Trading Class',
                            'Position','Average Cost'])

    dat[dat["Account"] == accountName]
    


tws.reqIds(1)
order_id = callback.next_ValidId + 1
contract_info = create.create_contract("GOOG", "STK", "SMART", "USD")
order_info = create.create_order(accountName, "MKT", 250, "BUY")

tws.placeOrder(order_id, contract_info, order_info)
orders = pd.DataFrame(callback.order_Status,
             columns = ['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
                        'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])
    
    
callback.open_Order[:1]

tws.cancelOrder(order_id)





contract_info = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
tickedId = 1002
tws.reqMktData(tickedId, contract_info, "", False)

tick_data = pd.DataFrame(callback.tick_Price, 
                         columns = ['tickerId', 'field', 'price', 'canAutoExecute'])
tick_type = {0 : "BID SIZE",
             1 : "BID PRICE",
             2 : "ASK PRICE",
             3 : "ASK SIZE",
             4 : "LAST PRICE",
             5 : "LAST SIZE",
             6 : "HIGH",
             7 : "LOW",
             8 : "VOLUME",
             9 : "CLOSE PRICE",
             10 : "BID OPTION COMPUTATION",
             11 : "ASK OPTION COMPUTATION",
             12 : "LAST OPTION COMPUTATION",
             13 : "MODEL OPTION COMPUTATION",
             14 : "OPEN_TICK",
             15 : "LOW 13 WEEK",
             16 : "HIGH 13 WEEK",
             17 : "LOW 26 WEEK",
             18 : "HIGH 26 WEEK",
             19 : "LOW 52 WEEK",
             20 : "HIGH 52 WEEK",
             21 : "AVG VOLUME",
             22 : "OPEN INTEREST",
             23 : "OPTION HISTORICAL VOL",
             24 : "OPTION IMPLIED VOL",
             27 : "OPTION CALL OPEN INTEREST",
             28 : "OPTION PUT OPEN INTEREST",
             29 : "OPTION CALL VOLUME"}
tick_data["Type"] = tick_data["field"].map(tick_type)
tick_data[-10:]




from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
from ib.ext.EClientSocket import EClientSocket
import ib.ext.EWrapper # receiving msg
import ib.ext.EClientSocket # send msg
from ib.ext.ScannerSubscription import ScannerSubscription

from datetime import datetime
import time

import threading

import datadecoder
dd = datadecoder.DataDecoder()
import numpy as np


from IBWrapper import IBWrapper, contract
accountName = "asd781820"
callback = IBWrapper()
tws = EClientSocket(callback)
host = ""
port = 4002
clientId = 9

tws.eConnect(host, port, clientId)

create = contract()
callback.initiate_variables()
tws.reqAccountSummary(8,'All','TotalCashValue')
callback.accountSummary()
globalid = 138756199

def buy(globalid,contract_Details):
    oid = globalid
    order = create_order('MKT', 100000, 'BUY')
    tws.placeOrder(oid, contract_Details, order)
    time.sleep(2)
    print('--------Account value before buy------')
    print(callback.account_Summary[-1][3])
    time.sleep(300)
    oid += 1
    order = create_order('MKT', 100000, 'SELL')
    tws.placeOrder(oid, contract_Details, order)
    print('buy order finished')
    time.sleep(2)
    print('-------Account value after buy--------')
    print(callback.account_Summary[-1][3])
    oid += 1
    globalid = oid
    
def sell(globalid,contract_Details):
    oid = globalid
    order = create_order('MKT', 100000, 'SELL')
    tws.placeOrder(oid, contract_Details, order)
    time.sleep(2)
    print('--------Account value before sell------')
    print(callback.account_Summary[-1][3])
    time.sleep(300)
    oid += 1
    order = create_order('MKT', 100000, 'BUY')
    tws.placeOrder(oid, contract_Details, order)
    print('sell order finished')
    time.sleep(2)
    print('-------Account value after sell--------')
    print(callback.account_Summary[-1][3])
    oid += 1
    globalid = oid
    
while(1):
    contract_Details = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    tws.reqCurrentTime()
    time.sleep(1)
    ts = callback.current_Time
    data_endtime = datetime.utcfromtimestamp(ts).strftime('%Y%m%d  %H:%M:%S')
    
    tickerId = 9010
    tws.reqHistoricalData(tickerId = tickerId, 
                      contract = contract_Details, 
                      endDateTime = data_endtime,
                      durationStr="1 D",
                      barSizeSetting = "1 min", 
                      whatToShow = "BID", 
                      useRTH = 0, 
                      formatDate = 1)

    time.sleep(3)

    data= pd.DataFrame(callback.historical_Data, 
                   columns = ["reqId", "date", "open",
                              "high", "low", "close", 
                              "volume", "count", "WAP", 
                              "hasGaps"])[-500:-1]
    dd.findMatch(data)
    for b in dd.reversedBucket:
        print('b is %s'%b)
        if(filedf.index.contains(b)):
            tempdf = filedf.loc[b]
            globalid += 2
            print(tempdf)
            if(tempdf['r5mean'] > 0):
                threading.Thread(target=buy,args = [globalid,contract_Details]).start()
                print('buy order executed')
            else:
                threading.Thread(target=sell,args = [globalid,contract_Details]).start()
                print('sell order executed')
    
    
    time.sleep(60)
    
    
    
    

contract_Details = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
tws.reqCurrentTime()
time.sleep(1)
ts = callback.current_Time
data_endtime = datetime.utcfromtimestamp(ts).strftime('%Y%m%d  %H:%M:%S')
    
tickerId = 9009
tws.reqHistoricalData(tickerId = tickerId, 
                      contract = contract_Details, 
                      endDateTime = data_endtime,
                      durationStr="1 D",
                      barSizeSetting = "1 min", 
                      whatToShow = "BID", 
                      useRTH = 0, 
                      formatDate = 1)

time.sleep(3)

data= pd.DataFrame(callback.historical_Data, 
                   columns = ["reqId", "date", "open",
                              "high", "low", "close", 
                              "volume", "count", "WAP", 
                              "hasGaps"])[-500:-1]