#!/usr/bin/env python
# coding: utf-8

from evidently.analyzers.base_analyzer import Analyzer
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare


class DataDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        result = dict()
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            if num_feature_names is None:
                num_feature_names = []
            else:
                num_feature_names = [name for name in num_feature_names if is_numeric_dtype(reference_data[name])]

            cat_feature_names = column_mapping.get('categorical_features')
            if cat_feature_names is None:
                cat_feature_names = []
            else:
                cat_feature_names = [name for name in cat_feature_names if is_numeric_dtype(reference_data[name])]
        else:
            date_column = 'datetime' if 'datetime' in reference_data.columns else None
            id_column = None
            target_column = 'target' if 'target' in reference_data.columns else None
            prediction_column = 'prediction' if 'prediction' in reference_data.columns else None

            utility_columns = [date_column, id_column, target_column, prediction_column]

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

        result["utility_columns"] = {'date':date_column, 'id':id_column, 'target':target_column, 'prediction':prediction_column}
        result["cat_feature_names"] = cat_feature_names
        result["num_feature_names"] = num_feature_names

        #calculate result
        result['metrics'] = {}
        for feature_name in num_feature_names:
            result['metrics'][feature_name] = dict(
                current_small_hist=[t.tolist() for t in np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                             bins=10, density=True)],
                ref_small_hist=[t.tolist() for t in np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                            bins=10, density=True)],
                feature_type='num',
                p_value=ks_2samp(reference_data[feature_name], current_data[feature_name])[1]
            )

        for feature_name in cat_feature_names:
            ref_feature_vc = reference_data[feature_name][np.isfinite(reference_data[feature_name])].value_counts()
            current_feature_vc = current_data[feature_name][np.isfinite(current_data[feature_name])].value_counts()

            keys = set(list(reference_data[feature_name][np.isfinite(reference_data[feature_name])].unique()) +
                       list(current_data[feature_name][np.isfinite(current_data[feature_name])].unique()))

            ref_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
                ref_feature_dict[key] = item

            current_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(current_feature_vc.index, current_feature_vc.values):
                current_feature_dict[key] = item

            f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
            f_obs = [value[1] for value in sorted(current_feature_dict.items())]

            # CHI2 to be implemented for cases with different categories
            p_value = chisquare(f_exp, f_obs)[1]

            result['metrics'][feature_name] = dict(
                current_small_hist=[t.tolist() for t in np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                             bins=10, density=True)],
                ref_small_hist=[t.tolist() for t in np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                            bins=10, density=True)],
                feature_type='cat',
                p_value=p_value,
            )
        return result
