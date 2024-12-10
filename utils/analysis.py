import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy import stats
import statsmodels.api as sm

class DataAnalyzer:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        self.df = df

    def basic_stats(self, column):
        try:
            if column not in self.df.columns:
                raise ValueError(f"Column {column} not found in DataFrame")
                
            numeric_data = pd.to_numeric(self.df[column], errors='coerce')
            stats_dict = {
                "mean": round(numeric_data.mean(), 2),
                "median": round(numeric_data.median(), 2),
                "std": round(numeric_data.std(), 2),
                "skew": round(numeric_data.skew(), 2),
                "kurtosis": round(numeric_data.kurtosis(), 2),
                "missing_values": numeric_data.isna().sum(),
                "count": numeric_data.count()
            }
            return stats_dict
            
        except Exception as e:
            print(f"Error calculating basic stats: {e}")
            return None

    def correlation_analysis(self, columns=None):
        try:
            if columns is not None:
                if not all(col in self.df.columns for col in columns):
                    raise ValueError("One or more specified columns not found")
                numeric_df = self.df[columns].select_dtypes(include=[np.number])
            else:
                numeric_df = self.df.select_dtypes(include=[np.number])
                
            if numeric_df.empty:
                raise ValueError("No numeric columns available for correlation")
                
            return numeric_df.corr()
            
        except Exception as e:
            print(f"Error in correlation analysis: {e}")
            return None

    def perform_pca(self, columns, n_components=2):
        try:
            if not all(col in self.df.columns for col in columns):
                raise ValueError("One or more specified columns not found")
                
            # Handle missing values
            data = self.df[columns].fillna(method='ffill')
            
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            pca = PCA(n_components=min(n_components, len(columns)))
            pca_result = pca.fit_transform(scaled_data)
            
            return pca_result, pca.explained_variance_ratio_
            
        except Exception as e:
            print(f"Error performing PCA: {e}")
            return None, None

    def time_series_analysis(self, date_column, value_column):
        try:
            if date_column not in self.df.columns or value_column not in self.df.columns:
                raise ValueError("Specified columns not found")
                
            # Convert to datetime and sort
            self.df[date_column] = pd.to_datetime(self.df[date_column])
            ts_data = self.df.sort_values(date_column).set_index(date_column)[value_column]
            
            # Handle missing values
            ts_data = ts_data.fillna(method='ffill')
            
            # Determine period based on data frequency
            period = min(12, len(ts_data) // 2)
            
            decomposition = sm.tsa.seasonal_decompose(ts_data, period=period)
            return decomposition
            
        except Exception as e:
            print(f"Error in time series analysis: {e}")
            return None

    def outlier_detection(self, column):
        try:
            if column not in self.df.columns:
                raise ValueError(f"Column {column} not found")
                
            data = pd.to_numeric(self.df[column], errors='coerce')
            data = data.dropna()
            
            if len(data) == 0:
                raise ValueError("No numeric data available for outlier detection")
                
            z_scores = stats.zscore(data)
            outliers = (abs(z_scores) > 3)
            
            return {
                "outliers": outliers,
                "outlier_indices": data[outliers].index.tolist(),
                "outlier_values": data[outliers].tolist()
            }
            
        except Exception as e:
            print(f"Error in outlier detection: {e}")
            return None