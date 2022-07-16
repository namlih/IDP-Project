from pytrends.request import TrendReq
import pytrends.exceptions 
import pandas as pd
import time
from datetime import datetime, timedelta
import requests

class GoogleTrendsAPIConnector:
    """
    A class to connect Google Trends API endpoint
    """

    def __init__(self):
        self.trend_req = TrendReq(hl='en-US', tz=360, retries=5, timeout=(2,15))
        self.data = pd.DataFrame()

    def load_kw_info(self,kw_info):
        self.kw = kw_info['name']
        self.start_date = kw_info['start_date']
        if kw_info['end_date'] == '':
            self.end_date = datetime.today().strftime('%Y%m%d') # setting the end date to today
        else:
            self.end_date = kw_info['end_date']    
        #self.days = pd.date_range(start=self.start_date,end=self.end_date, freq='7D').format()
        #self.days = pd.date_range(start=self.start_date,end=self.end_date, freq='6M').format()

    def get_data(self):
        self.is_data_ready = False
        
        self.empty_intervals = list()
        print(self.kw)
        
        counter = 0
        self.data = pd.DataFrame()

        more_retry_limit = 5
        more_retry_counter = 0
        more_retry_finished = False
        #while counter < len(self.days)-1:
        while counter < 1:
            #start_day = self.days[counter]
            start_day = self.start_date
            #end_day = self.days[counter+1]
            end_day = self.end_date
            #tf = start_day+'T00 '+end_day+'T00'
            tf = start_day+' '+end_day
            print('    '+tf)
            new_data = pd.DataFrame()           
            try:
                self.trend_req.build_payload([self.kw], cat=0, timeframe=tf, geo='', gprop='')
                new_data = self.trend_req.interest_over_time()
                #more_retry_counter = 0
            except pytrends.exceptions.ResponseError as e:
                print(e)
                #if more_retry_counter == more_retry_limit:
                #    more_retry_counter = 0
                #    more_retry_finished = True
                #    
                #else: 
                #    counter -= 1
                #    more_retry_counter += 1
                if e.response.status_code == 429:
                    time.sleep(60.0)
                
            except requests.exceptions.Timeout as e:
                print(e)
                #if more_retry_counter != more_retry_limit:
                #    more_retry_counter = 0
                #    more_retry_finished = True 
                    
                #else: 
                #    counter -= 1
                #    more_retry_counter += 1
            except:
                print('default exception')
                break
            
            
            if new_data.shape[0] == 0:
                counter -= 1
                more_retry_counter += 1
                
                if more_retry_counter == more_retry_limit:
                    more_retry_counter = 0
                    more_retry_finished = True
                
                if more_retry_finished == True:
                        self.empty_intervals.append((self.kw,start_day,end_day))
                        more_retry_finished = False
                        if self.data.shape[0] > 0:
                            self.is_data_ready = True
                            self.data['keyword'] = [self.kw for _ in range(self.data.shape[0])]
                            self.data.columns = ['value']+self.data.columns.to_list()[1:]
                            self.end_date = start_day
                        print('some problem happened during fetching the interval: ',start_day,' -> ',end_day)
                        break

            elif new_data.shape[0] > 0:
                print('data fetched')        
                new_data['interval'] = [start_day+' -> '+end_day for _ in range(new_data.shape[0])]
                self.data = self.data.append(new_data)
                more_retry_counter = 0
            
            counter += 1

        if len(self.empty_intervals) == 0:
            self.is_data_ready = True
            self.data['keyword'] = [self.kw for _ in range(self.data.shape[0])]
            self.data.columns = ['value']+self.data.columns.to_list()[1:]
            #self.end_date = self.days[-1]
