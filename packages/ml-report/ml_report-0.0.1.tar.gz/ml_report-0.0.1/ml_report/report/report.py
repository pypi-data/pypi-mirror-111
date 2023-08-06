import dill as pickle
import joblib
import json
import numpy as np
import os
import pandas as pd
from eli5 import explain_weights_df
from os.path import dirname, join
from sklearn.base import BaseEstimator
from sklearn.model_selection._search import BaseSearchCV
from sklearn.model_selection import cross_val_predict, GridSearchCV
from typing import Iterable, Union

from ml_report.report.metrics_report import metrics_report


search_filename = "search.pickle"
model_filename = "model.pickle"


class Report(object):
    def __init__(
        self,
        estimator,
        param_grid,
        df: pd.DataFrame,
        iv: Union[Iterable[str], str],
        dv: Union[Iterable[str], str],
        optimization_metric,
        metrics=None,
        scorers=None,
        search_cv: BaseSearchCV = None,
        rebuild_model=True,
        report_path="ml_reports",
        *args,
        **kwargs,
    ):

        self.estimator = estimator
        self.df = df
        self.iv = iv
        self.dv = dv
        self.param_grid = param_grid

        self.rebuild_model = rebuild_model
        self.report_path = report_path

        self.search_cv = search_cv
        self.y_pred = None

        self.search = None
        self.m = None

        self.metrics_df = None
        self.submetrics_df = None

        self.report_path = report_path
        self.create_report_path()
        self._save_args()

        if search_cv is not None:
            self.search_cv = search_cv
        else:
            self.search_cv = GridSearchCV(
                estimator=self.estimator,
                param_grid=param_grid,
                scoring=scorers,
                # cv=n_splits,
                refit="r2",
                return_train_score=True,
                # n_jobs=n_jobs,
                verbose=10,
            )

    def detailed_report(self, *args, **kwargs):
        pass  # TODO

    def fit(self, *args, **kwargs):
        self.search_cv.fit(X=self.df[self.iv], y=self.df[self.dv], *args, **kwargs)

    def _save_args(self):
        with open(self._to_report_path("args.json"), "w+") as f:
            json.dump(self.__dict__, f)

    def _save_model(self):
        # Pickle model.
        joblib.dump(self.search_cv, search_filename)
        joblib.dump(self.search_cv.best_estimator_, model_filename)

    def build_report(self, save=True):
        df_metrics_report = metrics_report(self.search)

        if save:
            df_metrics_report.to_csv()

    def create_report_path(self):
        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)

    def _to_report_path(self, path):
        return join(self.report_path, path)


# def load_report(report_path):
#     report = Report()
#     # Load pickled model.
#     report.search = joblib.load(search_filename)
#     report.m = joblib.load(model_filename)

#
# def report(
#     df: pd.DataFrame,
#     iv: Union[Iterable[str], str],
#     dv: Union[Iterable[str], str],
#     estimator,
#     param_grid,
#     scorers,
#     rebuild_model,
#     search_cv: BaseSearchCV = GridSearchCV,
#     n_jobs=1,
#     n_splits=10,
#     seed=0,
#     report_path="model_reports",
# ):
#     search_filename = "search.pickle"
#     model_filename = "model.pickle"
#
#     np.random.seed(seed)
#
#     if rebuild_model:
#         search = search_cv(
#             estimator=estimator,
#             param_grid=param_grid,
#             scoring=scorers,
#             cv=n_splits,
#             refit="r2",
#             return_train_score=True,
#             n_jobs=n_jobs,
#             verbose=10,
#         )
#
#         search.fit(X=df[iv], y=df[dv])
#
#         # Pickle model.
#         joblib.dump(search, search_filename)
#         joblib.dump(search.best_estimator_, model_filename)
#         print("Model pickled.")
#
#     # Load pickled model.
#     search = joblib.load(search_filename)
#     m = joblib.load(model_filename)
#
#     # Create path to store reports.
#     if not os.path.exists(report_path):
#         os.makedirs(report_path)
#
#     with open(f"{report_path}/best_params.json", "w+") as f:
#         json.dump(search.best_params_, f)
#
#     df_metrics = metrics_report(search)
#     df_metrics.round(3).to_csv(f"{report_path}/metrics.csv", index=False)
#
#     explain_weights_df(m).round(3).to_csv(
#         f"{report_path}/eli5_explanation.csv", index=False
#     )
#
#     return search
