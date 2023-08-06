import requests
from .auth import EncryptionClient
from .const import GENERIC_PAYLOAD, JWT_PAYLOAD, CUSTOMER_LOGIN_PAYLOAD, PARTNER_LOGIN_PAYLOAD, ORDER_PAYLOAD, HISTORICAL_CANDLE_HEADERS, HEADERS, NEXT_DAY_TIMESTAMP, TODAY_TIMESTAMP
from .conf import APP_SOURCE
from .order import Order, OrderType, OrderFor, OrderValidity, OrderFor, AHPlaced
from .logging import log_response
import datetime
import pandas as pd
import numpy as np
from typing import Union
import json


class IIFLClient:

    CUSTOMER_LOGIN_ROUTE = "https://dataservice.iifl.in/openapi/prod/LoginRequest"
    PARTNER_LOGIN_ROUTE = "https://dataservice.iifl.in/openapi/prod/LoginRequestMobileForVendor"
    JWT_VALIDATION_ROUTE = "https://dataservice.iifl.in/openapi/prod/JWTOpenApiValidation"
    CLIENT_PROFILE_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffClientProfile"

    MARGIN_ROUTE = "https://dataservice.iifl.in/openapi/prod/Margin"
    ORDER_BOOK_ROUTE = "https://dataservice.iifl.in/openapi/prod/OrderBookV2"
    TRADE_BOOK_ROUTE = "https://dataservice.iifl.in/openapi/prod/TradeBook"
    HOLDINGS_ROUTE = "https://dataservice.iifl.in/openapi/prod/Holding"
    DP_HOLDING_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffDPHolding"
    NET_POSITIONS_ROUTE = "https://dataservice.iifl.in/openapi/prod/NetPosition"
    NET_POSITION_NET_WISE_ROUTE = "https://dataservice.iifl.in/openapi/prod/NetPositionNetWise"

    ORDER_PLACEMENT_ROUTE = "https://dataservice.iifl.in/openapi/prod/OrderRequest"
    ORDER_STATUS_ROUTE = "https://dataservice.iifl.in/openapi/prod/OrderStatus"
    TRADE_INFO_ROUTE = "https://dataservice.iifl.in/openapi/prod/TradeInformation"
    
    MARKET_FEED_ROUTE="https://dataservice.iifl.in/openapi/prod/MarketFeed"
    HISTORICAL_CANDLE_ROUTE = "https://dataservice.iifl.in/openapi/prod/historical/"
    
    EQUITY_TRANSC_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffEquitytransaction"
    FUTURE_TRANSC_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffFutureTransaction"
    OPTION_TRANSC_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffoptionTransaction"
    MF_TRANSC_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffMutualFundTransaction"
    DP_TRANS_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffDPTransaction"
    LEDGER_ROUTE="https://dataservice.iifl.in/openapi/prod/BackoffLedger"

    CLIENT_PROFILE_REQUEST_CODE = "IIFLMarRQBackoffClientProfile"
    MARGIN_REQUEST_CODE = "IIFLMarRQMarginV3"
    ORDER_BOOK_REQUEST_CODE = "IIFLMarRQOrdBkV2"
    TRADE_BOOK_REQUEST_CODE = "IIFLMarRQTrdBkV1"
    HOLDINGS_REQUEST_CODE = "IIFLMarRQHoldingV2"
    DP_HOLDING_REQUEST_CODE = "IIFLMarRQBackoffDPHolding"
    NET_POSITIONS_REQUEST_CODE = "IIFLMarRQNetPositionV4"
    NET_POSITION_NETWISE_REQUEST_CODE = "IIFLMarRQNPNWV2"
    EQUITY_TRANSC_REQUEST_CODE = "IIFLMarRQBackoffEquitytransaction"
    FUTURE_TRANSC_REQUEST_CODE = "IIFLMarRQBackoffFutureTransaction"
    OPTION_TRANSC_REQUEST_CODE = "IIFLMarRQBackoffoptionTransaction"
    MF_TRANSC_REQUEST_CODE = "IIFLMarRQBackoffMutulFundTransaction"
    DP_TRANS_REQUEST_CODE = "IIFLMarRQBackoffDPTransaction"
    LEDGER_REQUEST_CODE = "IIFLMarRQBackoffLedger"

    def __init__(self, client_code=None, passwd=None, dob=None,email_id=None,contact_number=None,jwt=None):
        """
        Main constructor for client.
        Expects user's client code, password and date of birth in YYYYMMDD format.
        """
        self.client_code = client_code
        self.passwd = passwd
        self.dob = dob
        self.email_id = email_id
        self.contact_number = contact_number
        self.jwt = jwt
        self.payload = GENERIC_PAYLOAD
        self.order_payload = ORDER_PAYLOAD
        self.client_login_payload = CUSTOMER_LOGIN_PAYLOAD
        self.partner_login_payload = PARTNER_LOGIN_PAYLOAD
        self.ScripMaster = pd.read_csv('http://content.indiainfoline.com/IIFLTT/Scripmaster.csv')
        self.session = requests.Session()

    def client_login(self):
        encryption_client = EncryptionClient()
        secret_client_code = encryption_client.encrypt(self.client_code)
        secret_passwd = encryption_client.encrypt(self.passwd)
        secret_dob = encryption_client.encrypt(self.dob)
        self.client_login_payload["body"]["ClientCode"] = secret_client_code
        self.client_login_payload["body"]["Password"] = secret_passwd
        self.client_login_payload["body"]["My2PIN"] = secret_dob
        self.client_login_payload["head"]["requestCode"] = "IIFLMarRQLoginRequestV4"
        res = self._login_request_client(self.CUSTOMER_LOGIN_ROUTE)
        message = res["body"]["Msg"]
        self.jwt = res["body"]["Token"]
        if message == "":
            log_response("Logged in!!")
        else:
            log_response(message)

    def partner_login(self):
        self.partner_login_payload["body"]["Email_id"] = self.email_id
        self.partner_login_payload["body"]["ContactNumber"] = self.contact_number
        self.partner_login_payload["head"]["requestCode"] = "IIFLMarRQLoginForVendor"
        res = self._login_request_partner(self.PARTNER_LOGIN_ROUTE)
        message = res["body"]["Message"]
        if message == "Successfully LoggedIn":
            log_response("Logged in!!")
        else:
            log_response(message)

    def get_option_scripcode(self,symbol,expiry,strike_price,cp):
        symbol = symbol.upper() + ' ' + expiry + ' ' + cp + ' ' + strike_price
        symbols = self.ScripMaster['Name'].copy().to_numpy()
        ScripCodes = self.ScripMaster['Scripcode'].copy().to_numpy()
        for i in range(symbols.size):
            if symbol in symbols[i]:
                return ScripCodes[i]
        return "Not Found!"

    def get_option_exchange(self,symbol,expiry,strike_price,cp):
        symbol = symbol.upper() + ' ' + expiry + ' ' + cp + ' ' + strike_price
        symbols = self.ScripMaster['Name'].copy().to_numpy()
        Exchanges = self.ScripMaster['Exch'].copy().to_numpy()
        for i in range(symbols.size):
            if symbol in symbols[i]:
                return Exchanges[i]
        return "Not Found!"

    def get_option_exchangetype(self,symbol,expiry,strike_price,cp):
        symbol = symbol.upper() + ' ' + expiry + ' ' + cp + ' ' + strike_price
        symbols = self.ScripMaster['Name'].copy().to_numpy()
        ExchangeTypes = self.ScripMaster['ExchType'].copy().to_numpy()
        for i in range(symbols.size):
            if symbol in symbols[i]:
                return ExchangeTypes[i]
        return "Not Found!"

    def profile(self, client_id):
        return self._user_info_request("PROFILE", client_id)

    def holdings(self, client_id):
        return self._user_info_request("HOLDINGS", client_id)

    def dp_holdings(self, client_id):
        return self._user_info_request("DP_HOLDINGS", client_id)

    def margin(self, client_id):
        return self._user_info_request("MARGIN", client_id)

    def order_book(self, client_id):
        return self._user_info_request("ORDER_BOOK", client_id)

    def trade_book(self, client_id):
        return self._user_info_request("TRADE_BOOK", client_id)

    def net_positions(self, client_id):
        return self._user_info_request("NET_POSITIONS", client_id)

    def net_position_netwise(self, client_id):
        return self._user_info_request("NET_POSITION_NETWISE", client_id)

    def equity_transactions(self, client_id, from_date, to_date):
        return self._user_transc_info("EQUITY", client_id, from_date, to_date)

    def future_transactions(self, client_id, from_date, to_date):
        return self._user_transc_info("FUTURE", client_id, from_date, to_date)

    def option_transactions(self, client_id, from_date, to_date):
        return self._user_transc_info("OPTION", client_id, from_date, to_date)

    def mf_transactions(self, client_id, from_date, to_date):
        return self._user_transc_info("MF", client_id, from_date, to_date)

    def dp_transactions(self, client_id, from_date, to_date):
        return self._user_transc_info("DP_TRANSC", client_id, from_date, to_date)

    def ledger(self, client_id, from_date, to_date):
        return self._user_transc_info("LEDGER", client_id, from_date, to_date)

    def _login_request_client(self, route):
        res = self.session.post(route, json=self.client_login_payload, headers=HEADERS)
        session_cookies = res.cookies
        cookies_dictionary = session_cookies.get_dict()
        return res.json()

    def _login_request_partner(self, route):
        res = self.session.post(route, json=self.partner_login_payload, headers=HEADERS)
        session_cookies = res.cookies
        cookies_dictionary = session_cookies.get_dict()
        return res.json()

    def _user_info_request(self, data_type, client_id):
        payload = GENERIC_PAYLOAD
        payload["body"]["ClientCode"] = client_id
        return_type = ""
        if data_type == "MARGIN":
            request_code = self.MARGIN_REQUEST_CODE
            url = self.MARGIN_ROUTE
            return_type = "EquityMargin"
        elif data_type == "PROFILE":
            request_code = self.CLIENT_PROFILE_REQUEST_CODE
            url = self.CLIENT_PROFILE_ROUTE
        elif data_type == "ORDER_BOOK":
            request_code = self.ORDER_BOOK_REQUEST_CODE
            url = self.ORDER_BOOK_ROUTE
            return_type = "OrderBookDetail"
        elif data_type == "TRADE_BOOK":
            request_code = self.TRADE_BOOK_REQUEST_CODE
            url = self.TRADE_BOOK_ROUTE
            return_type = "TradeBookDetail"
        elif data_type == "HOLDINGS":
            request_code = self.HOLDINGS_REQUEST_CODE
            url = self.HOLDINGS_ROUTE
            return_type = "Data"
        elif data_type == "DP_HOLDINGS":
            request_code = self.DP_HOLDING_REQUEST_CODE
            url = self.DP_HOLDING_ROUTE
            return_type = "DPHolding"
        elif data_type == "NET_POSITIONS":
            request_code = self.NET_POSITIONS_REQUEST_CODE
            url = self.NET_POSITIONS_ROUTE
            return_type = "NetPositionDetail"
        elif data_type == "NET_POSITION_NETWISE":
            request_code = self.NET_POSITION_NETWISE_REQUEST_CODE
            url = self.NET_POSITION_NET_WISE_ROUTE
            return_type = "NetPositionDetail"
        else:
            raise Exception("Invalid data type requested")

        payload["head"]["requestCode"] = request_code
        response = self.session.post(url, json=payload, headers=HEADERS).json()
        if data_type == "PROFILE":
            return response
        else:
            data = response["body"][return_type]
            return data

    def _user_transc_info(self, data_type, client_id, from_date, to_date):
        payload = GENERIC_PAYLOAD
        payload["body"]["ClientCode"] = client_id
        payload["body"]["FromDate"] = from_date
        payload["body"]["ToDate"] = to_date
        return_type = ""
        if data_type == "EQUITY":
            request_code = self.EQUITY_TRANSC_REQUEST_CODE
            url = self.EQUITY_TRANSC_ROUTE
            return_type = "ackoffEquitytransaction"
        elif data_type == "FUTURE":
            request_code = self.FUTURE_TRANSC_REQUEST_CODE
            url = self.FUTURE_TRANSC_ROUTE
            return_type = "FutureTransaction"
        elif data_type == "OPTION":
            request_code = self.OPTION_TRANSC_REQUEST_CODE
            url = self.OPTION_TRANSC_ROUTE
            return_type = "OptionTransactionRes"
        elif data_type == "MF":
            request_code = self.MF_TRANSC_REQUEST_CODE
            url = self.MF_TRANSC_ROUTE
            return_type = "MutulFundTransactionRes"
        elif data_type == "LEDGER":
            request_code = self.LEDGER_REQUEST_CODE
            url = self.LEDGER_ROUTE
            return_type = "LedgerRes"
        elif data_type == "DP_TRANSC":
            request_code = self.DP_TRANS_REQUEST_CODE
            url = self.DP_TRANS_ROUTE
            return_type = "DPTransactionRes"
        else:
            raise Exception("Invalid data type requested")
            
        payload["head"]["requestCode"] = request_code
        response = self.session.post(url, json=payload, headers=HEADERS).json()
        data = response["body"][return_type]
        return data

    def order_request(self, req_type, client_id, order_requester_code) -> None:

        self.payload["body"]["ClientCode"] = client_id

        if req_type == "OP":
            url = self.ORDER_PLACEMENT_ROUTE
            self.order_payload["_ReqData"]["body"]["ClientCode"] = client_id
            self.order_payload["_ReqData"]["body"]["OrderRequesterCode"] = order_requester_code
            res = self.session.post(url, json=self.order_payload,
                                    headers=HEADERS).json()
            log_response(res["body"])
            return res["body"]
        elif req_type == "OS":
            url = self.ORDER_STATUS_ROUTE
            self.payload["head"]["requestCode"] = "IIFLMarRQOrdStatus"
            res = self.session.post(url, json=self.payload,
                                headers=HEADERS).json()
            log_response(res["body"])
            return res["body"]
        elif req_type == "TI":
            url = self.TRADE_INFO_ROUTE
            self.payload["head"]["requestCode"] = "IIFLMarRQTrdInfo"
            res = self.session.post(url, json=self.payload,
                                headers=HEADERS).json()
            log_response(res["body"])
            return res["body"]
        elif req_type == "MF":
            url = self.MARKET_FEED_ROUTE
            self.payload["head"]["requestCode"] = "IIFLMarRQMarketFeed"
            res = self.session.post(url, json=self.payload,
                                headers=HEADERS).json()
            log_response(res["body"])
            return res["body"]
        else:
            raise Exception("Invalid request type!")

        res = self.session.post(url, json=self.payload,
                                headers=HEADERS).json()
        log_response(res["body"])
        return res["body"]

    def fetch_order_status(self, req_list:list, client_id) :
        self.payload["body"]["OrdStatusReqList"] = req_list
        return self.order_request("OS", client_id, client_id)

    def fetch_trade_info(self, req_list:list, client_id) :
        self.payload["body"]["TradeInformationList"] = req_list
        return self.order_request("TI", client_id, client_id)
    
    def fetch_market_feed(self, req_list:list, count, client_id) :
        """
            market feed api
        """
        
        self.payload["body"]["MarketFeedData"] = req_list
        self.payload["body"]["Count"] = count
        self.payload["body"]["ClientLoginType"] = 0
        self.payload["body"]["LastRequestTime"] = f"/Date({TODAY_TIMESTAMP})/"
        self.payload["body"]["RefreshRate"] = "H"
        return self.order_request("MF", client_id, client_id)

    def jwt_validation(self,client_id):
        jwt_Payload = JWT_PAYLOAD
        jwt_Payload["ClientCode"] = client_id
        jwt_Payload["JwtCode"] = self.jwt
        url = self.JWT_VALIDATION_ROUTE
        response = self.session.post(url, json=jwt_Payload, headers=HEADERS).json()
        return response["body"]["Message"]

    def historical_candles(self,exch,exchType,scripcode,interval,fromdate,todate,client_id):
        historical_headers = HISTORICAL_CANDLE_HEADERS
        historical_headers["x-clientcode"] = client_id
        historical_headers["x-auth-token"] = self.jwt
        url = self.HISTORICAL_CANDLE_ROUTE+exch+"/"+exchType+"/"+scripcode+"/"+interval+"?from="+fromdate+"&end="+todate
        response = self.session.get(url, headers=historical_headers).json()
        return response

    def set_payload(self, order: Order) -> None:
        self.order_payload["_ReqData"]["body"]["OrderFor"] = order.order_for
        self.order_payload["_ReqData"]["body"]["Exchange"] = order.exchange
        self.order_payload["_ReqData"]["body"]["ExchangeType"] = order.exchange_segment
        self.order_payload["_ReqData"]["body"]["Price"] = order.price
        self.order_payload["_ReqData"]["body"]["OrderID"] = order.order_id
        self.order_payload["_ReqData"]["body"]["OrderType"] = order.order_type
        self.order_payload["_ReqData"]["body"]["Qty"] = order.quantity
        # Passing today's unix timestamp
        self.order_payload["_ReqData"]["body"]["OrderDateTime"] = f"/Date({TODAY_TIMESTAMP})/"
        self.order_payload["_ReqData"]["body"]["ScripCode"] = order.scrip_code
        self.order_payload["_ReqData"]["body"]["AtMarket"] = order.atmarket
        self.order_payload["_ReqData"]["body"]["RemoteOrderID"] = order.remote_order_id
        self.order_payload["_ReqData"]["body"]["ExchOrderID"] = order.exch_order_id
        self.order_payload["_ReqData"]["body"]["DisQty"] = order.DisQty
        self.order_payload["_ReqData"]["body"]["IsStopLossOrder"] = order.is_stoploss_order
        self.order_payload["_ReqData"]["body"]["StopLossPrice"] = order.stoploss_price
        self.order_payload["_ReqData"]["body"]["IsVTD"] = order.is_vtd
        self.order_payload["_ReqData"]["body"]["IOCOrder"] = order.ioc_order
        self.order_payload["_ReqData"]["body"]["IsIntraday"] = order.is_intraday
        self.order_payload["_ReqData"]["body"]["PublicIP"] = order.public_ip
        self.order_payload["_ReqData"]["body"]["AHPlaced"] = order.ahplaced
        # Passing the next day's UNIX timestamp
        self.order_payload["_ReqData"]["body"]["ValidTillDate"] = order.vtd
        self.order_payload["_ReqData"]["body"]["TradedQty"] = order.traded_qty
        self.order_payload["_ReqData"]["body"]["iOrderValidity"] = order.order_validity

    def place_order(self, order: Order, client_id, order_requester_code):
        """
        Places a fresh order
        """
        self.set_payload(order)
        self.order_payload["_ReqData"]["body"]["OrderFor"] = "P"
        return self.order_request("OP", client_id, order_requester_code)

    def modify_order(self, order: Order, client_id, order_requester_code):
        """
        Modifies an existing order
        """
        self.set_payload(order)
        self.order_payload["_ReqData"]["body"]["OrderFor"] = "M"
        return self.order_request("OP", client_id, order_requester_code)

    def cancel_order(self, order: Order, client_id, order_requester_code):
        """
        Cancels an existing order
        """
        self.set_payload(order)
        self.order_payload["_ReqData"]["body"]["OrderFor"] = "C"
        return self.order_request("OP", client_id, order_requester_code)

    #Functions for strategies - Start
    def short_straddle(self,symbol,expiry,strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        CE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price,'CE')
        CE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price,'CE')
        CE_Exch = self.get_option_exchange(symbol,expiry,strike_price,'CE')
        PE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price,'PE')
        PE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price,'PE')
        PE_Exch = self.get_option_exchange(symbol,expiry,strike_price,'PE')
        
        if (CE_ScripCode == "Not Found!" or PE_ScripCode == "Not Found!"):
            return "Symbol details not found. Please provide correct symbol."

        PE_Order = Order(order_type="SELL", scrip_code=int(PE_ScripCode), quantity=qty, exchange=PE_Exch,
                 exchange_segment=PE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_Order = Order(order_type="SELL", scrip_code=int(CE_ScripCode), quantity=qty, exchange=CE_Exch,
                 exchange_segment=CE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        PE_Order_Res = self.place_order(order=PE_Order, client_id=client_id, order_requester_code=order_requester_code)
        if PE_Order_Res["Message"] == "Success":
            CE_Order_Res = self.place_order(order=CE_Order, client_id=client_id, order_requester_code=order_requester_code)
            if CE_Order_Res["Message"] == "Success":
                return "Success"
            else:
                return "Couldn't place order. Try again."
        else:
            return "Couldn't place order. Try again."

    def long_straddle(self,symbol,expiry,strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        CE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price,'CE')
        CE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price,'CE')
        CE_Exch = self.get_option_exchange(symbol,expiry,strike_price,'CE')
        PE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price,'PE')
        PE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price,'PE')
        PE_Exch = self.get_option_exchange(symbol,expiry,strike_price,'PE')
        
        if (CE_ScripCode == "Not Found!" or PE_ScripCode == "Not Found!"):
            return "Symbol details not found. Please provide correct symbol."

        PE_Order = Order(order_type="BUY", scrip_code=int(PE_ScripCode), quantity=qty, exchange=PE_Exch,
                 exchange_segment=PE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_Order = Order(order_type="BUY", scrip_code=int(CE_ScripCode), quantity=qty, exchange=CE_Exch,
                 exchange_segment=CE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        PE_Order_Res = self.place_order(order=PE_Order, client_id=client_id, order_requester_code=order_requester_code)
        if PE_Order_Res["Message"] == "Success":
            CE_Order_Res = self.place_order(order=CE_Order, client_id=client_id, order_requester_code=order_requester_code)
            if CE_Order_Res["Message"] == "Success":
                return "Success"
            else:
                return "Couldn't place order. Try again."
        else:
            return "Couldn't place order. Try again."

    def short_strangle(self,symbol,expiry,strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        CE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price[0],'CE')
        CE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price[0],'CE')
        CE_Exch = self.get_option_exchange(symbol,expiry,strike_price[0],'CE')
        PE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price[1],'PE')
        PE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price[1],'PE')
        PE_Exch = self.get_option_exchange(symbol,expiry,strike_price[1],'PE')
        
        if (CE_ScripCode == "Not Found!" or PE_ScripCode == "Not Found!"):
            return "Symbol details not found. Please provide correct symbol."

        PE_Order = Order(order_type="SELL", scrip_code=int(PE_ScripCode), quantity=qty, exchange=PE_Exch,
                 exchange_segment=PE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_Order = Order(order_type="SELL", scrip_code=int(CE_ScripCode), quantity=qty, exchange=CE_Exch,
                 exchange_segment=CE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        PE_Order_Res = self.place_order(order=PE_Order, client_id=client_id, order_requester_code=order_requester_code)
        if PE_Order_Res["Message"] == "Success":
            CE_Order_Res = self.place_order(order=CE_Order, client_id=client_id, order_requester_code=order_requester_code)
            if CE_Order_Res["Message"] == "Success":
                return "Success"
            else:
                return "Couldn't place order. Try again."
        else:
            return "Couldn't place order. Try again."

    def long_strangle(self,symbol,expiry,strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        CE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price[0],'CE')
        CE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price[0],'CE')
        CE_Exch = self.get_option_exchange(symbol,expiry,strike_price[0],'CE')
        PE_ScripCode = self.get_option_scripcode(symbol,expiry,strike_price[1],'PE')
        PE_ExchType = self.get_option_exchangetype(symbol,expiry,strike_price[1],'PE')
        PE_Exch = self.get_option_exchange(symbol,expiry,strike_price[1],'PE')
        
        if (CE_ScripCode == "Not Found!" or PE_ScripCode == "Not Found!"):
            return "Symbol details not found. Please provide correct symbol."

        PE_Order = Order(order_type="BUY", scrip_code=int(PE_ScripCode), quantity=qty, exchange=PE_Exch,
                 exchange_segment=PE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_Order = Order(order_type="BUY", scrip_code=int(CE_ScripCode), quantity=qty, exchange=CE_Exch,
                 exchange_segment=CE_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        PE_Order_Res = self.place_order(order=PE_Order, client_id=client_id, order_requester_code=order_requester_code)
        if PE_Order_Res["Message"] == "Success":
            CE_Order_Res = self.place_order(order=CE_Order, client_id=client_id, order_requester_code=order_requester_code)
            if CE_Order_Res["Message"] == "Success":
                return "Success"
            else:
                return "Couldn't place order. Try again."
        else:
            return "Couldn't place order. Try again."

    def iron_fly(self,symbol,expiry,buy_strike_price,sell_strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        buy_strike_price.sort()
        CE_BUY_ScripCode = self.get_option_scripcode(symbol,expiry,buy_strike_price[1],'CE')
        CE_BUY_ExchType = self.get_option_exchangetype(symbol,expiry,buy_strike_price[1],'CE')
        CE_BUY_Exch = self.get_option_exchange(symbol,expiry,buy_strike_price[1],'CE')
        PE_BUY_ScripCode = self.get_option_scripcode(symbol,expiry,buy_strike_price[0],'PE')
        PE_BUY_ExchType = self.get_option_exchangetype(symbol,expiry,buy_strike_price[0],'PE')
        PE_BUY_Exch = self.get_option_exchange(symbol,expiry,buy_strike_price[0],'PE')
        CE_SELL_ScripCode = self.get_option_scripcode(symbol,expiry,sell_strike_price,'CE')
        CE_SELL_ExchType = self.get_option_exchangetype(symbol,expiry,sell_strike_price,'CE')
        CE_SELL_Exch = self.get_option_exchange(symbol,expiry,sell_strike_price,'CE')
        PE_SELL_ScripCode = self.get_option_scripcode(symbol,expiry,sell_strike_price,'PE')
        PE_SELL_ExchType = self.get_option_exchangetype(symbol,expiry,sell_strike_price,'PE')
        PE_SELL_Exch = self.get_option_exchange(symbol,expiry,sell_strike_price,'PE')

        if (CE_BUY_ScripCode == "Not Found!" or PE_BUY_ScripCode == "Not Found!" or CE_SELL_ScripCode == "Not Found!" or PE_SELL_ScripCode == "Not Found!"):
            return "Symbol details not found. Please provide correct details."

        PE_BUY_Order = Order(order_type="BUY", scrip_code=int(PE_BUY_ScripCode), quantity=qty, exchange=PE_BUY_Exch,
                 exchange_segment=PE_BUY_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_BUY_Order = Order(order_type="BUY", scrip_code=int(CE_BUY_ScripCode), quantity=qty, exchange=CE_BUY_Exch,
                 exchange_segment=CE_BUY_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        PE_SELL_Order = Order(order_type="SELL", scrip_code=int(PE_SELL_ScripCode), quantity=qty, exchange=PE_SELL_Exch,
                 exchange_segment=PE_SELL_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_SELL_Order = Order(order_type="SELL", scrip_code=int(CE_SELL_ScripCode), quantity=qty, exchange=CE_SELL_Exch,
                 exchange_segment=CE_SELL_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        orders = [PE_BUY_Order, CE_BUY_Order, PE_SELL_Order, CE_SELL_Order]
        for i in orders:
            Order_Res = self.place_order(order=i, client_id=client_id, order_requester_code=order_requester_code)
            if Order_Res["Message"] == "Success":
                continue
            else:
                return "Couldn't place order. "+ Order_Res["Message"] + " Try again."
        return "Success"

    def iron_condor(self,symbol,expiry,buy_strike_price,sell_strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        buy_strike_price.sort()
        sell_strike_price.sort()
        CE_BUY_ScripCode = self.get_option_scripcode(symbol,expiry,buy_strike_price[1],'CE')
        CE_BUY_ExchType = self.get_option_exchangetype(symbol,expiry,buy_strike_price[1],'CE')
        CE_BUY_Exch = self.get_option_exchange(symbol,expiry,buy_strike_price[1],'CE')
        PE_BUY_ScripCode = self.get_option_scripcode(symbol,expiry,buy_strike_price[0],'PE')
        PE_BUY_ExchType = self.get_option_exchangetype(symbol,expiry,buy_strike_price[0],'PE')
        PE_BUY_Exch = self.get_option_exchange(symbol,expiry,buy_strike_price[0],'PE')
        CE_SELL_ScripCode = self.get_option_scripcode(symbol,expiry,sell_strike_price[1],'CE')
        CE_SELL_ExchType = self.get_option_exchangetype(symbol,expiry,sell_strike_price[1],'CE')
        CE_SELL_Exch = self.get_option_exchange(symbol,expiry,sell_strike_price[1],'CE')
        PE_SELL_ScripCode = self.get_option_scripcode(symbol,expiry,sell_strike_price[0],'PE')
        PE_SELL_ExchType = self.get_option_exchangetype(symbol,expiry,sell_strike_price[0],'PE')
        PE_SELL_Exch = self.get_option_exchange(symbol,expiry,sell_strike_price[0],'PE')

        if (CE_BUY_ScripCode == "Not Found!" or PE_BUY_ScripCode == "Not Found!" or CE_SELL_ScripCode == "Not Found!" or PE_SELL_ScripCode == "Not Found!"):
            return "Symbol details not found. Please provide correct details."

        PE_BUY_Order = Order(order_type="BUY", scrip_code=int(PE_BUY_ScripCode), quantity=qty, exchange=PE_BUY_Exch,
                 exchange_segment=PE_BUY_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_BUY_Order = Order(order_type="BUY", scrip_code=int(CE_BUY_ScripCode), quantity=qty, exchange=CE_BUY_Exch,
                 exchange_segment=CE_BUY_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        PE_SELL_Order = Order(order_type="SELL", scrip_code=int(PE_SELL_ScripCode), quantity=qty, exchange=PE_SELL_Exch,
                 exchange_segment=PE_SELL_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        CE_SELL_Order = Order(order_type="SELL", scrip_code=int(CE_SELL_ScripCode), quantity=qty, exchange=CE_SELL_Exch,
                 exchange_segment=CE_SELL_ExchType, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        orders = [PE_BUY_Order, CE_BUY_Order, PE_SELL_Order, CE_SELL_Order]
        for i in orders:
            Order_Res = self.place_order(order=i, client_id=client_id, order_requester_code=order_requester_code)
            if Order_Res["Message"] == "Success":
                continue
            else:
                return "Couldn't place order. "+ Order_Res["Message"] + " Try again."
        return "Success"

    def put_calendar(self,symbol,expiry,strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        ScripCode_BUY = self.get_option_scripcode(symbol,expiry[0],strike_price,'PE')
        ExchType_BUY = self.get_option_exchangetype(symbol,expiry[0],strike_price,'PE')
        Exch_BUY = self.get_option_exchange(symbol,expiry[0],strike_price,'PE')
        ScripCode_SELL = self.get_option_scripcode(symbol,expiry[1],strike_price,'PE')
        ExchType_SELL = self.get_option_exchangetype(symbol,expiry[1],strike_price,'PE')
        Exch_SELL = self.get_option_exchange(symbol,expiry[1],strike_price,'PE')
        
        if (ScripCode_BUY == "Not Found!" or ScripCode_SELL == "Not Found!"):
            return "Symbol details not found. Please provide correct symbol."

        Order_BUY = Order(order_type="BUY", scrip_code=int(ScripCode_BUY), quantity=qty, exchange=Exch_BUY,
                 exchange_segment=ExchType_BUY, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        Order_SELL = Order(order_type="SELL", scrip_code=int(ScripCode_SELL), quantity=qty, exchange=Exch_SELL,
                 exchange_segment=ExchType_SELL, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        Order_BUY_Res = self.place_order(order=Order_BUY, client_id=client_id, order_requester_code=order_requester_code)
        if Order_BUY_Res["Message"] == "Success":
            Order_SELL_Res = self.place_order(order=Order_SELL, client_id=client_id, order_requester_code=order_requester_code)
            if Order_SELL_Res["Message"] == "Success":
                return "Success"
            else:
                return "Couldn't place order. Try again."
        else:
            return "Couldn't place order. Try again."

    def call_calendar(self,symbol,expiry,strike_price,qty,isIntra,client_id,order_requester_code,RemoteOrderID):
        ScripCode_BUY = self.get_option_scripcode(symbol,expiry[0],strike_price,'CE')
        ExchType_BUY = self.get_option_exchangetype(symbol,expiry[0],strike_price,'CE')
        Exch_BUY = self.get_option_exchange(symbol,expiry[0],strike_price,'CE')
        ScripCode_SELL = self.get_option_scripcode(symbol,expiry[1],strike_price,'CE')
        ExchType_SELL = self.get_option_exchangetype(symbol,expiry[1],strike_price,'CE')
        Exch_SELL = self.get_option_exchange(symbol,expiry[1],strike_price,'CE')
        
        if (ScripCode_BUY == "Not Found!" or ScripCode_SELL == "Not Found!"):
            return "Symbol details not found. Please provide correct symbol."

        Order_BUY = Order(order_type="BUY", scrip_code=int(ScripCode_BUY), quantity=qty, exchange=Exch_BUY,
                 exchange_segment=ExchType_BUY, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        Order_SELL = Order(order_type="SELL", scrip_code=int(ScripCode_SELL), quantity=qty, exchange=Exch_SELL,
                 exchange_segment=ExchType_SELL, price=0, is_intraday=isIntra, atmarket=True, order_id=0,
                  remote_order_id=RemoteOrderID, exch_order_id="0", order_for=OrderFor.PLACE,
                 DisQty=0, stoploss_price=0, is_stoploss_order=False, ioc_order=False,
                  is_vtd=False, vtd=f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced=AHPlaced.NORMAL_ORDER, public_ip='192.168.1.1',
                 order_validity=OrderValidity.DAY, traded_qty=0)
        Order_BUY_Res = self.place_order(order=Order_BUY, client_id=client_id, order_requester_code=order_requester_code)
        if Order_BUY_Res["Message"] == "Success":
            Order_SELL_Res = self.place_order(order=Order_SELL, client_id=client_id, order_requester_code=order_requester_code)
            if Order_SELL_Res["Message"] == "Success":
                return "Success"
            else:
                return "Couldn't place order. Try again."
        else:
            return "Couldn't place order. Try again."
    #Functions for strategies - End