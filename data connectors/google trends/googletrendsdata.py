from googletrendsapiconnector import GoogleTrendsAPIConnector
from googletrendsdatanormalizer import GoogleTrendsDataNormalizer
import pandas as pd
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--json",help="json file")

    args = parser.parse_args()
    with open(args.json) as json_file:
        req_info = json.load(json_file)

    data = pd.DataFrame()
    normalized_data = pd.DataFrame()
    api_connector = GoogleTrendsAPIConnector()
    #first loop for extracting data from end point
    for kw_info in req_info['keywords']:
        if kw_info['get_data']:
            try:                
                api_connector.load_kw_info(kw_info)
                print('get data')
                api_connector.get_data()
                if api_connector.is_data_ready == True:
                    data = data.append(api_connector.data)
                    kw_info['end_date'] = api_connector.end_date
                    file_name = kw_info['name']+'_'+kw_info['start_date']+'-'+kw_info['end_date']+'.csv'
                    file_name = 'data_daily/'+kw_info['name']+'/'+file_name
                    api_connector.data.to_csv(file_name)
            except:
                print('some problems happened with '+kw_info['name']+' data')
                pass

        if kw_info['normalize_data']:
            #try:
            print('normalize data of ',kw_info['name'])
            normalizer_data = pd.DataFrame()
            if kw_info['read_from_csv']:
                print('merging files')
                for file_name in kw_info['files']:
                    file_name = 'data_daily/'+kw_info['name']+'/'+file_name
                    normalizer_data = normalizer_data.append(pd.read_csv(file_name))
                normalizer_data.index = [pd.Timestamp(date) for date in normalizer_data['date'].to_list()]
                normalizer_data.drop(columns=['date'],inplace=True)
                normalizer_data.sort_index(inplace=True)
                normalizer_data.index = normalizer_data.index.rename('date')
                print('normalizer_data.columns:',normalizer_data.columns)
            else: 
                normalizer_data = normalizer_data.append(data[data['keyword'] == kw_info['name']].copy())
            
            normalizer = GoogleTrendsDataNormalizer(data=normalizer_data)
            print('  finding peak points')
            normalizer.find_peak_points()

            print('  finding overlapping dates')
            normalizer.find_overlapping_dates()

            print('  finding values at overlapping dates')
            normalizer.find_values_at_overlapping_dates()
            
            print('  expanding data')
            normalizer.expand_data()

            print('  finding normalization factors')
            normalizer.find_normalization_factors()

            print('  finding cumulative normalization factors')
            normalizer.find_cumulative_normalization_factor()

            print('  finding the interval with highest peak')
            normalizer.find_interval_with_highest_peak()

            print('  finding overall normalization factor')
            normalizer.find_overall_normalization_factor()

            print('  applying overall normalization to data')
            normalizer.apply_overall_normalization()
            
            file_name = 'normalized_'+kw_info['name']+'_'+kw_info['start_date']+'-'+kw_info['end_date']+'.csv'
            file_name = 'normalized_data_daily/' + file_name
            normalizer.normalized_data.to_csv(file_name)
            print(' ')

            #except:
            #    print('some problems happened with '+kw_info['name']+' data during normalization')
            #    pass

