import numpy as np
import pandas as pd
import datetime as dt

#import data
def main():
    parse_date = ['time']
    idx = ['time']

    cgm_small = pd.read_csv('smallData/cgm_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    cgm_small = cgm_small.astype(float)
    cgm_small = cgm_small.rename(columns={"value": "cgm"})

    activity_small = pd.read_csv('smallData/activity_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    activity_small = activity_small.astype(float)
    activity_small = activity_small.rename(columns={"value": "activity"})

    basal_small = pd.read_csv('smallData/basal_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    basal_small = basal_small.astype(float)
    basal_small = basal_small.rename(columns={"value": "basal"})

    bolus_small = pd.read_csv('smallData/bolus_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    bolus_small = bolus_small.astype({'value': 'float','Id': 'float'})
    bolus_small = bolus_small.rename(columns={"value": "bolus"})

    hr_small = pd.read_csv('smallData/hr_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    hr_small = hr_small.astype(float)
    hr_small = hr_small.rename(columns={"value": "hr"})

    meal_small = pd.read_csv('smallData/meal_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    meal_small = meal_small.astype(float)
    meal_small = meal_small.rename(columns={"value": "meal"})

    smbg_small = pd.read_csv('smallData/smbg_small.csv',
                                 header=0, parse_dates=parse_date,
                                 index_col=idx)
    smbg_small = smbg_small.astype(float)
    smbg_small = smbg_small.rename(columns={"value": "smbg"})

    #join all the datasets on time index

    joined_df = cgm_small.join(activity_small.activity)
    joined_df = joined_df.join(basal_small.basal)
    joined_df = joined_df.join(bolus_small.bolus)
    joined_df = joined_df.join(hr_small.hr)
    joined_df = joined_df.join(meal_small.meal)
    joined_df = joined_df.join(smbg_small.smbg)

    #replace NaNs with 0s
    joined_df = joined_df.fillna(0)

    #add time5 columns with values rounded to 5min
    joined_df['round_5'] = joined_df.index.round('5min')
    #add time15 column with values rounded to 15min
    joined_df['round_15'] = joined_df.index.round('15min')

    #group by things by rounded 5 min
    mean_group = joined_df.groupby('round_5')['smbg','hr','cgm','basal'].mean()
    sum_group = joined_df.groupby('round_5')['activity','bolus','meal'].sum()
    grouped_df_5min = pd.merge(mean_group, sum_group, on='round_5')
    grouped_df_5min.to_csv('5min_rounded_df.csv')

    #group by things by rounded 15 min
    mean_group = joined_df.groupby('round_15')['smbg','hr','cgm','basal'].mean()
    sum_group = joined_df.groupby('round_15')['activity','bolus','meal'].sum()
    grouped_df_15min = pd.merge(mean_group, sum_group, on='round_15')
    grouped_df_15min.to_csv('15min_rounded_df.csv')


if __name__ == '__main__':
    main()
