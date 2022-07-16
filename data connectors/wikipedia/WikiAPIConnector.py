import requests
import pandas as pd
import json
import argparse
from datetime import datetime

current_date = datetime.today().strftime('%Y%m%d')

class WikiAPIConnector:
    """
    A class to connect Wikipedia API endpoint

    Connects to the API endpoint of Wikipedia and 
    extracts specified metrics of articles given
    with the json file
    """

    def __init__(self,articles_metrics):
        """
        Constructor assigns articles and metrics attributes with the values
        comes from articles_metrics dict
        """
        self.data = pd.DataFrame()
        self.articles = articles_metrics['articles']
        self.metrics = articles_metrics['metrics']

    def create_url(self,article,metric):
        """A function that creates a url with the given article and metric parameters"""
        url = 'https://wikimedia.org/api/rest_v1/metrics/'
        url += metric
        url += '/per-article/en.wikipedia.org/all-access/all-agents/'
        url += article 
        url += '/daily/20000101/'
        url += current_date
        return url

    def get_metrics(self):
        """A function that get metrics of specified articles from API endpoint"""
        for metric in self.metrics:
            for article in self.articles:
                url = self.create_url(article,metric)
                headers = requests.utils.default_headers()
                headers.update(
                    {
                        'User-Agent': 'My User Agent 1.0',
                    }
                )
                res = requests.get(url,headers = headers)
                try:
                    print('article:',article)
                    
                    body = res.json()
                    new_data = pd.DataFrame(body['items']).drop(columns = ['project','granularity','access','agent'])
                    self.data = self.data.append(new_data)
                    print('article read')
                except:
                    print('problem with ',article,' article')


    def save_data(self):
        """A function that saves pandas dataframe object to a csv file"""
        self.data.to_csv('data.csv',index=False)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Wiki API Connector')

    parser.add_argument("--json",help="articles and metrics json file")

    args = parser.parse_args()
    with open(args.json) as json_file:
        articles_metrics = json.load(json_file)

    api_connector = WikiAPIConnector(articles_metrics)
    api_connector.get_metrics()
    api_connector.save_data()