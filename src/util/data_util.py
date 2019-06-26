"""
@author Claas Voelcker

Utils module containing some data utility functions
"""
import numpy as np

from src.util.spn_util import get_categoricals


def get_categorical_data(spn, df, dictionary, header=1, types=False, date=False, assert_nan=False):
    """

    :param spn:
    :param df:
    :param dictionary:
    :param header:
    :param types:
    :param date:
    :return:
    """
    context = dictionary['context']
    categoricals = get_categoricals(spn, context)
    df_numerical = df.copy(deep=True)
    for i in categoricals:
        if df_numerical.iloc[:, i].isnull().values.any():
            non_nan = np.where(~np.isnan(df_numerical.iloc[:, i]))
        else:
            non_nan = np.arange(df_numerical.iloc[:, i].size)
        transformed = dictionary['features'][i]['encoder'].transform(
            df_numerical.values[non_nan, i].squeeze())
        df_numerical.iloc[non_nan, i] = transformed

    numerical_data = df_numerical.values.astype(float)

    categorical_data = {}
    for i in categoricals:
        non_nan = np.where(~np.isnan(df_numerical.iloc[:, i]))
        data = df_numerical.iloc[non_nan].groupby(context.feature_names[i])
        data = [data.get_group(x).values.astype(float) for x in data.groups]
        categorical_data[i] = data

    return numerical_data, categorical_data


def bin_gradient_data(data, gradients, bins):
    """
    Computes a histogram of normalized gradient data

    :param data: the underlying data
    :param gradients: the gradients
    :param bins: number of bins
    :return: a histogram object
    """
    bin_borders = np.linspace(-1, 1, num=bins+1)
    query_list = [np.where((gradients >= bin_borders[i]) & (gradients < bin_borders[i+1])) for i in range(len(bin_borders) - 1)]
    binned_data = []
    for query in query_list:
        binned_data.append(data[query[0],:])
    return binned_data
