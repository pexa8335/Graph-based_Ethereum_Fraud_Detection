# API_Handling/ml_transformers.py

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder

# Bạn cần import numpy và các thư viện khác mà class sử dụng

class IntelligentImputer(BaseEstimator, TransformerMixin):
  def __init__(self, numeric_fill_value=0, categorical_fill_value='Unknown'):
    self.numeric_fill_value = numeric_fill_value
    self.categorical_fill_value = categorical_fill_value
  
  def fit(self, X, y=None):
    self.numeric_cols_ = X.select_dtypes(include=np.number).columns.tolist()
    self.categorical_cols_ = X.select_dtypes(exclude=np.number).columns.tolist()
    self.encoder_ = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    temp_categorical_data = X[self.categorical_cols_].fillna(self.categorical_fill_value) 
    self.encoder_.fit(temp_categorical_data)
    return self

  def transform(self, X):
    X_transformed = X.copy()
    if self.numeric_cols_:
      X_transformed[self.numeric_cols_] = X_transformed[self.numeric_cols_].fillna(self.numeric_fill_value)
    if self.categorical_cols_:
      X_transformed[self.categorical_cols_] = X_transformed[self.categorical_cols_].fillna(self.categorical_fill_value)
    X_transformed[self.categorical_cols_] = self.encoder_.transform(X_transformed[self.categorical_cols_])
    return X_transformed

  def get_feature_names_out(self, input_features=None):
    return self.numeric_cols_ + self.categorical_cols_

class ControlCharacterCleaner(BaseEstimator, TransformerMixin):
  def __init__(self):
    pass
  
  def _remove_control_char(self, s):
    cleaned = ''.join(c for c in str(s) if ord(c) >= 32 or c in '\t\n\r')
    return cleaned if cleaned.strip() != '' else np.nan

  def fit(self, X, y=None):
    self.object_cols_ = X.select_dtypes(include=['object', 'category']).columns.tolist()
    return self

  def transform(self, X):
      X_transformed = X.copy()
      for col in self.object_cols_:
          X_transformed[col] = X_transformed[col].apply(self._remove_control_char)
      return X_transformed

class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        return X_transformed.drop(columns=self.columns_to_drop, errors='ignore')