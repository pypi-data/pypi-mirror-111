import pandas as pd
import requests
import json 
from .constants import APP_URLS
from .response import Response
from .utils import clean_query


class QuantDataApi:

    def __init__(self, api_auth_token):
        self.api_auth_token = api_auth_token

    response_class = Response

    def __get_headers(self):
        return {
            "AUTHORIZATION": "Token %s" % self.api_auth_token,
            "Content-type": "application/json",
            "charset": "utf-8"
        }

    def __clean_data(self, data, query_name):
        return data['data'][query_name]

    def __handle_request(self, query, query_name):
        status, response = self.response_class(self.post(query))
        if status == "success":
            return self.__clean_data(response, query_name)
        else:
            raise Exception(response)

    def post(self, query):
        headers = self.__get_headers()
        response = requests.post(
            APP_URLS['graphane'], json={'query': query}, headers=headers
        )
        return response

    def get_companies(self, stock="GPW"):
        filter_q = f"""stock: "{stock}" """
        query = """query {
            companies(%s) {
              symbol,
              name,
              stock
            }
        }""" % filter_q
        return self.__handle_request(query, "companies")
    
    def get_indexes(self, stock="GPW"):
        filter_q = f"""stock: "{stock}" """
        query = """query {
            indexes(%s) {
              symbol,
              stock
            }
        }""" % filter_q
        return self.__handle_request(query, "indexes")
    
    def get_quotations(self, symbol, date_from=None, date_to=None):
        filter_q = f"""symbol: "{symbol}" """
        if date_from:
            filter_q += f""", dateFrom: "{date_from}" """
        if date_to:
            filter_q += f""", dateTo: "{date_to}" """

        query = """query {
            quotationsBySymbol(%s) {
                stock,
                data
          }
        }""" % filter_q
        return self.__handle_request(clean_query(query), "quotationsBySymbol")

    def get_quotations_as_df(self, symbol, date_from=None, date_to=None,
                             stock="GPW"):
        response = self.get_quotations(symbol, date_from=date_from,
                                       date_to=date_to)
        data = []
        for d in response:
            if d['stock'] == stock:
                data = d['data']
        
        try:
            data = json.loads(data)
        except TypeError:
            data = []
        
        return pd.DataFrame(
            data, 
            columns=['datetime', 'high', 'low', 'open', 'close']
        )

    def get_reports(self, symbol):
        query = """query {
            reportsBySymbol(%s) {
              stock,
              data
          }
        }""" % f"""symbol: "{symbol}" """
        return self.__handle_request(clean_query(query), "reportsBySymbol")
