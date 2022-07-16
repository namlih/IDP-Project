import pandas as pd

class GoogleTrendsDataNormalizer:

    def __init__(self,data):
        self.data = data

    def find_peak_points(self):
        self.peak_points = self.data[self.data['value'] == 100].copy()
        self.peak_points.drop_duplicates(subset=['interval'],keep='first',inplace=True)
    
    def find_overlapping_dates(self):
        self.intervals = dict()
        self.intervals['intervals'] = self.peak_points['interval'].to_list()
        self.intervals['next_interval'] = self.intervals['intervals'][1:]+self.intervals['intervals'][-1:]
        self.intervals['prev_interval'] = self.intervals['intervals'][:1]+self.intervals['intervals'][:-1]

        self.overlap_dates = dict()
        self.overlap_dates['forward_overlap_date'] = [pd.Timestamp(interval[:10]+'T00') for interval in self.intervals['next_interval']]
        self.overlap_dates['backward_overlap_date'] = [pd.Timestamp(interval[-10:]+'T00') for interval in self.intervals['prev_interval']]

    def find_values_at_overlapping_dates(self):
        data_ = self.data.reset_index()
        print('data_.columns',data_.columns)
        self.forward_overlap_val = [data_[(data_['date'] == date) & (data_['interval'] == interval)]['value'].to_list()[0] \
                                    for (interval,date) in zip(self.intervals['intervals'],self.overlap_dates['forward_overlap_date'])]
        self.forward_overlap_val_next_interval = [data_[(data_['date'] == date) & (data_['interval'] == interval)]['value'].to_list()[0] \
                                                    for (interval,date) in zip(self.intervals['next_interval'],self.overlap_dates['forward_overlap_date'])]
        self.backward_overlap_val = [data_[(data_['date'] == date) & (data_['interval'] == interval)]['value'].to_list()[0] \
                                    for (interval,date) in zip(self.intervals['intervals'],self.overlap_dates['backward_overlap_date'])]
        self.backward_overlap_val_prev_interval = [data_[(data_['date'] == date) & (data_['interval'] == interval)]['value'].to_list()[0] \
                                                    for (interval,date) in zip(self.intervals['prev_interval'],self.overlap_dates['backward_overlap_date'])]

#    def find_values_at_overlapping_dates(self):
#        data_ = self.data.reset_index()

#        self.forward_overlap_val = list()
#        self.forward_overlap_val_next_interval = list()
#        self.backward_overlap_val = list()
#        self.backward_overlap_val_prev_interval = list()
#        for i in range(len(intervals)):
#            self.forward_overlap_val.append(data_[(data_['date'] == self.overlap_dates[i]) & \
#                                                  (data_['interval'] == self.intervals[i])]['value'].to_list()[0])
#            
#            self.forward_overlap_val.append(data_[(data_['date'] == self.overlap_dates[i]) & \
#                                                  (data_['interval'] == self.intervals[i])]['value'].to_list()[0])#

#            self.forward_overlap_val.append(data_[(data_['date'] == self.overlap_dates[i]) & \
#                                                  (data_['interval'] == self.intervals[i])]['value'].to_list()[0])
#
#            self.forward_overlap_val.append(data_[(data_['date'] == self.overlap_dates[i]) & \
#                                                  (data_['interval'] == self.intervals[i])]['value'].to_list()[0])

    def expand_data(self):
        self.peak_points['next_interval'] = self.intervals['next_interval']
        self.peak_points['prev_interval'] = self.intervals['prev_interval']
        self.peak_points['forward_overlap_date'] = self.overlap_dates['forward_overlap_date']
        self.peak_points['backward_overlap_date'] = self.overlap_dates['backward_overlap_date']
        self.peak_points['forward_overlap_val'] = [val if val != 0 else 1 for val in self.forward_overlap_val]
        self.peak_points['forward_overlap_val_next_interval'] = [val if val != 0 else 1 for val in self.forward_overlap_val_next_interval]
        self.peak_points['backward_overlap_val'] = [val if val != 0 else 1 for val in self.backward_overlap_val]
        self.peak_points['backward_overlap_val_prev_interval'] = [val if val != 0 else 1 for val in self.backward_overlap_val_prev_interval]

    def find_normalization_factors(self):
        self.peak_points['forward_normalization_factor'] = self.peak_points['forward_overlap_val_next_interval']/self.peak_points['forward_overlap_val']
        self.peak_points['backward_normalization_factor'] = self.peak_points['backward_overlap_val_prev_interval']/self.peak_points['backward_overlap_val']

    def find_cumulative_normalization_factor(self):
        self.days_factors = self.peak_points[['interval','forward_normalization_factor','backward_normalization_factor']].drop_duplicates()
        cumulative_normalization_factor = list()
        for interval in self.days_factors['interval'].unique():
            values = self.days_factors[self.days_factors['interval'] < interval]['forward_normalization_factor'].unique()
            cumulative_normalization_factor_val = 1
            for val in values:
                cumulative_normalization_factor_val *= val
            cumulative_normalization_factor.append(cumulative_normalization_factor_val)
        self.days_factors['cumulative_normalization_factor'] = cumulative_normalization_factor

    def find_interval_with_highest_peak(self):
        min_cum_nor_factor = self.days_factors['cumulative_normalization_factor'].min()
        self.peak_interval = self.days_factors[self.days_factors['cumulative_normalization_factor'] == min_cum_nor_factor]['interval'].to_list()[0]

    def find_overall_normalization_factor(self):
        overall_normalization_factor = list()
        for interval in self.days_factors['interval'].to_list():
            if interval < self.peak_interval:
                values = self.days_factors[(self.days_factors['interval'] < self.peak_interval) & (self.days_factors['interval'] >= interval)]['forward_normalization_factor'].unique()
            elif interval > self.peak_interval:
                values = self.days_factors[(self.days_factors['interval'] > self.peak_interval) & (self.days_factors['interval'] <= interval)]['backward_normalization_factor'].unique()
            else:
                values = [1]
            overall_normalization_factor_val = 1
            for val in values:
                overall_normalization_factor_val *= val
            overall_normalization_factor.append(overall_normalization_factor_val)
        self.days_factors['overall_normalization_factor'] = overall_normalization_factor
    
    def apply_overall_normalization(self):
        overall_normalization_factors = self.days_factors[['interval','overall_normalization_factor']].drop_duplicates()
        self.normalized_data = self.data.copy()
        self.normalized_data['normalized_'+'value'] = self.normalized_data['value']
        column_names = self.normalized_data.columns
        self.normalized_data = self.normalized_data.apply(lambda x: [x[0],x[1],x[2],x[3],x[0]*overall_normalization_factors[overall_normalization_factors['interval'] == x[2]]['overall_normalization_factor'].to_list()[0]],axis=1,result_type='expand')
        self.normalized_data.columns = column_names

