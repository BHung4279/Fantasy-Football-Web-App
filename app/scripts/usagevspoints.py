import pandas as pd
#import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def generate_figure():
    # import the csv file (2019-2.csv)
    df = pd.read_csv('2019-2.csv')

    # get rid of unnecesscary values
    # axis = 1 (0 = row, 1 = column) tells pandas that we are committing a change in the column axis
    # inplace = True tells pandas that we want to make a permanent change
    df.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'], axis = 1, inplace = True)

    # fixes the player names
    df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

    # clarifies stats
    df.rename({
        'TD': 'PassingTD',
        'TD.1': 'RushingTD',
        'TD.2': 'ReceivingTD',
        'TD.3': 'TotalTD',
        'Yds': 'PassingYDs',
        'Yds.1': 'RushingYDs',
        'Yds.2': 'ReceivingYDs',
        'Att': 'PassingAtt',
        'Att.1': 'RushingAtt'
    }, axis = 1, inplace = True)

    # separates into different dataframes based on (fantasy) positions
    rb_df = df[df['FantPos'] == 'RB']
    #wr_df = df[df['FantPos'] == 'WR']
    #qb_df = df[df['FantPos'] == 'QB']
    #te_df = df[df['FantPos'] == 'TE']

    # defines individual position stats
    rushing_columns = ['RushingAtt', 'RushingYDs', 'Y/A', 'RushingTD']
    receiving_columns = ['Tgt', 'Rec', 'ReceivingYDs', 'Y/R', 'ReceivingTD']
    passing_columns = ['PassingAtt', 'PassingYDs', 'PassingTD', 'Int']

    # defines a function to aid in transforming the dataframes
    def transform_columns(df, new_column_list):
        df = df[['Player', 'Tm', 'Age', 'G'] + new_column_list + ['FL']]
        return df

    # transforms the columns
    rb_df = transform_columns(rb_df, rushing_columns + receiving_columns)
    #wr_df = transform_columns(wr_df, rushing_columns + receiving_columns)
    #te_df = transform_columns(te_df, receiving_columns)
    #qb_df = transform_columns(qb_df, passing_columns)

    # creates new column for fantasy points
    rb_df['Fantasy Points'] = rb_df['RushingYDs'] * .1 + rb_df['RushingTD'] * 6 + rb_df['ReceivingYDs'] * .1 + rb_df['ReceivingTD'] * .6 - rb_df['FL'] * 2
    #wr_df['Fantasy Points'] = wr_df['RushingYDs'] * .1 + wr_df['RushingTD'] * 6 + wr_df['ReceivingYDs'] * .1 + wr_df['ReceivingTD'] * .6 - wr_df['FL'] * 2
    #te_df['Fantasy Points'] = te_df['ReceivingYDs'] * .1 + te_df['ReceivingTD'] * 6
    #qb_df['Fantasy Points'] = qb_df['PassingYDs'] * .04 + qb_df['PassingTD'] * 4

    # creates new columns for usage/game
    rb_df['Fantasy Points / Game'] = rb_df['Fantasy Points'] / rb_df['G']
    rb_df['Fantasy Points / Game'] = rb_df['Fantasy Points'].apply(lambda x: round(x, 2))
    rb_df['Usage / Game'] = (rb_df['Tgt'] + rb_df['RushingAtt'])/rb_df['G']
    rb_df['Usage / Game'] = rb_df['Usage / Game'].apply(lambda x: round(x, 2))

    rb_df['Fantasy Points / Game'].astype('int32').dtypes
    rb_df['Usage / Game'].astype('int32').dtypes
    #rb_df.replace([np.inf, -np.inf], np.nan)
    #rb_df.replace(np.nan, 0)
    #rb_df.fillna(0, inplace=True)
    #rb_df['Age'].astype('int32').dtypes
    #rb_df['G'].astype('int32').dtypes
    #rb_df['RushingAtt'].astype('int32').dtypes
    #rb_df['RushingYDs'].astype('int32').dtypes
    #rb_df['Y/A'].astype('int32').dtypes
    #rb_df['RushingTD'].astype('int32').dtypes
    #rb_df['Tgt'].astype('int32').dtypes
    #rb_df['Rec'].astype('int32').dtypes
    #rb_df['ReceivingYDs'].astype('int32').dtypes
    #rb_df['Y/R'].astype('int32').dtypes
    #rb_df['ReceivingTD'].astype('int32').dtypes
    #rb_df['FL'].astype('int32').dtypes

    #wr_df['Fantasy Points / Game'] = wr_df['Fantasy Points'] / wr_df['G']
    #wr_df['Fantasy Points / Game'] = wr_df['Fantasy Points'].apply(lambda x: round(x, 2))
    #wr_df['Usage / Game'] = (wr_df['Tgt'] + wr_df['RushingAtt'])/wr_df['G']
    #wr_df['Usage / Game'] = wr_df['Usage / Game'].apply(lambda x: round(x, 2))

    #te_df['Fantasy Points / Game'] = te_df['Fantasy Points'] / te_df['G']
    #te_df['Fantasy Points / Game'] = te_df['Fantasy Points'].apply(lambda x: round(x, 2))
    #te_df['Usage / Game'] = (te_df['Tgt']) / wr_df['G']
    #te_df['Usage / Game'] = te_df['Usage / Game'].apply(lambda x: round(x, 2))

    # seaborn styling
    sns.set_style('whitegrid')

    # create canvas (matplotlib)
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)

    # basic regression scatterplot with trendline
    plot_rb = sns.regplot(x = rb_df['Usage / Game'], y = rb_df['Fantasy Points / Game'], scatter = True)

    figure = plot_rb.get_figure()
    figure.savefig("output.png")
    # plot_rb.show()
    # print("here")

generate_figure()