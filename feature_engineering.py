import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineering(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["rooms_per_household"] = X["total_rooms"] / X["households"].replace(0, 1)
        X["bedrooms_per_room"] = X["total_bedrooms"] / X["total_rooms"].replace(0, 1)
        X["population_per_household"] = X["population"] / X["households"].replace(0, 1)
        return X