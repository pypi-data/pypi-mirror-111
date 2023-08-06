#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import tarfile
import argparse
import numpy as np
import pandas as pd
from scipy.stats import randint
from six.moves import urllib
import traceback
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedShuffleSplit,
    train_test_split,
)
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
import joblib
import logging
from housing_price_pred.logger import configure_logger

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s"
            + "%(funcName)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)

HOUSING_PATH = os.path.join(os.getcwd(),"data", "raw")
PROCESSED_PATH = os.path.join(os.getcwd(),"data", "processed")
PICKLE_PATH = os.path.join(os.getcwd(),'artifacts')


rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room = True):
        self.add_bedrooms_per_room = add_bedrooms_per_room
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X, y = None):
        rooms_per_household = X[:,rooms_ix] / X[:,households_ix]
        population_per_household = X[:,population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:,bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X,rooms_per_household,population_per_household,bedrooms_per_room]
        else:
            return np.c_[X,rooms_per_household,population_per_household]
    
    def get_feature_names(self):
        if self.add_bedrooms_per_room:
            return ['rooms_per_household','population_per_household','bedrooms_per_room']
        else:
            return ['rooms_per_household','population_per_household']

def get_feature_names_from_column_transformer(col_trans,idx_custom_column_adder):
    """Get feature names from a sklearn column transformer.
	
    The `ColumnTransformer` class in `scikit-learn` supports taking in a
    `pd.DataFrame` object and specifying `Transformer` operations on columns.
    The output of the `ColumnTransformer` is a numpy array that can used and
    does not contain the column names from the original dataframe. The class
    provides a `get_feature_names` method for this purpose that returns the
    column names corr. to the output array. Unfortunately, not all
    `scikit-learn` classes provide this method (e.g. `Pipeline`) and still
    being actively worked upon.
    
	NOTE: This utility function is a temporary solution until the proper fix is
    available in the `scikit-learn` library.
    """
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder as skohe
    
	# SimpleImputer has `add_indicator` attribute that distinguishes it from other transformers
    # Encoder had `get_feature_names` attribute that distinguishes it from other transformers
	# The last transformer is ColumnTransformer's 'remainder'
    col_name = []
    M = 0
    for transformer_in_columns in col_trans.transformers_:
        M+=1
        print('Iteration:',str(M))
        print('Transformer in Column: ',transformer_in_columns)
        is_pipeline=0
        raw_col_name = list(transformer_in_columns[2])
        d_type = transformer_in_columns[0]
        print('Type:',d_type)
        print('Raw_Col:',raw_col_name)
        
        
        if isinstance(transformer_in_columns[1], Pipeline): 
            # if pipeline, get the last transformer
            print('Pipeline:',transformer_in_columns[1])
            print('Steps:',transformer_in_columns[1].steps[-1])
            transformer = transformer_in_columns[1].steps[-1][1]
            created_cols = col_trans.named_transformers_[d_type].named_steps[transformer_in_columns[1].steps[idx_custom_column_adder][0]].get_feature_names()
            print('Created Col',created_cols)
            print('Last Step',transformer)
            is_pipeline=1
            print('Pipeline Value:',is_pipeline)
        else:
            transformer = transformer_in_columns[1]
            print(is_pipeline)
            
        try:
            if isinstance(transformer, str):
                if transformer == "passthrough":
                    names = transformer._feature_names_in[raw_col_name].tolist()
                    print('Names_1',names)

                elif transformer == "drop":
                    names = []
                    print('Names_2',names)

                else:
                    raise RuntimeError(
                        f"Unexpected transformer action for unaccounted cols :"
                        f"{transformer} : {raw_col_name}"
                    )

            elif isinstance(transformer, OneHotEncoder):
                names = list(transformer.get_feature_names(raw_col_name))
                print('Names3',names)
            
            elif isinstance(transformer, SimpleImputer) and transformer.add_indicator:
                missing_indicator_indices = transformer.indicator_.features_
                missing_indicators = [raw_col_name[idx] + '_missing_flag' for idx in missing_indicator_indices]

                names = raw_col_name + missing_indicators
                print('Names_4',names)
            
            else:
                names = list(transformer.get_feature_names()) + created_cols
                print('Names_5',names)
          
        except AttributeError as error:
              names = raw_col_name
              print('Names_6',names)
        if is_pipeline:
            names=[f'{col_}'for col_ in names] + created_cols
            print('Iteration ',str(M),':',names)
        col_name.extend(names)
    return col_name





def preprocess_data(input_folder, processed_folder):
    # read train and test sets
    strat_train_set = pd.read_csv(os.path.join(input_folder,'train.csv'))
    strat_test_set = pd.read_csv(os.path.join(input_folder,'test.csv'))
    
    rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

    # prepare train set
    housing = strat_train_set.copy()
    housing = strat_train_set.drop("median_house_value", axis=1)  # drop labels for training set
    housing_labels = strat_train_set["median_house_value"].copy()
    num_pipeline = Pipeline([
        ('imputer',SimpleImputer(strategy='median')),
        ('attribs_adder',CombinedAttributesAdder()),
        ('std_scaler',StandardScaler())])
    num_attribs = housing.select_dtypes([np.number]).columns.tolist()
    cat_attribs = ['ocean_proximity']
    full_pipeline = ColumnTransformer([
        ('num',num_pipeline,num_attribs),
        ('cat',OneHotEncoder(),cat_attribs)])
    
    housing_array = full_pipeline.fit_transform(housing)
    cols_ = get_feature_names_from_column_transformer(full_pipeline,1)
    housing_prepared = pd.DataFrame(data = housing_array, columns = cols_)
    housing_prepared.to_csv(os.path.join(processed_folder,'train_processed.csv'),index=False)

    # prepare test set
    X_test = strat_test_set.drop("median_house_value", axis=1)
    y_test = strat_test_set[["median_house_value"]].copy()
    X_test_array = full_pipeline.transform(X_test)
    X_test_prepared = pd.DataFrame(data=X_test_array,columns = cols_)
    X_test_prepared.to_csv(os.path.join(processed_folder,'test_processed.csv'),index=False)
    y_test.to_csv(os.path.join(processed_folder,'test_labels.csv'),index=False)
    return housing_prepared, housing_labels, X_test_prepared, y_test


def lin_reg(X_train, y_train, pickle_path):
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    pred = lin_reg.predict(X_train)
    lin_mse = mean_squared_error(y_train, pred)

    #lin_rmse
    lin_rmse = np.sqrt(lin_mse)
    #lin_mar
    lin_mae = mean_absolute_error(y_train, pred)
    # saving pickle file
    filename_lin_reg = 'lin_reg.pkl'
    joblib.dump(lin_reg, os.path.join(pickle_path,filename_lin_reg))
    return pred, lin_mse, lin_rmse, lin_mae

def tree_reg(X_train, y_train, pickle_path,random_state = 42):
    tree_reg = DecisionTreeRegressor(random_state= random_state)
    tree_reg.fit(X_train, y_train)
    pred = tree_reg.predict(X_train)
    tree_mse = mean_squared_error(y_train, pred)
    tree_rmse = np.sqrt(tree_mse)
    tree_mae = mean_absolute_error(y_train, pred)
    #tree_rmse
    filename_tree_reg = 'tree_reg.pkl'
    joblib.dump(tree_reg, os.path.join(pickle_path,filename_tree_reg))
    return pred, tree_mse, tree_rmse, tree_mae

def rf_hyperparameter_tuner(X_train, y_train, search_type, params, pickle_path, n_iter = 10, cv = 5, random_state = 42):
    forest_reg = RandomForestRegressor(random_state=random_state)
    if search_type == 'Randomized':
        logger.info('Search Type: Randomized')
        rnd_search = RandomizedSearchCV(
            forest_reg,
            param_distributions=params,
            n_iter=n_iter,
            cv=cv,
            scoring="neg_mean_squared_error",
            random_state=random_state,
            )
        rnd_search.fit(X_train, y_train)
        cvres = rnd_search.cv_results_
        for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
            logger.info(np.sqrt(-mean_score), params)
        final_model = rnd_search.best_estimator_
        best_params = rnd_search.best_params_
        mse = -rnd_search.best_score_
        rmse = np.sqrt(mse)
        filename = 'rnd_forest_reg.pkl'
        joblib.dump(final_model, os.path.join(pickle_path,filename))
    elif search_type=='Grid':
        logger.info('Search Type: Grid')
        grid_search = GridSearchCV(
            forest_reg,
            params,
            cv=cv,
            scoring="neg_mean_squared_error",
            return_train_score=True,
            )
        grid_search.fit(X_train, y_train)
        cvres = grid_search.cv_results_
        for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
            logger.info(np.sqrt(-mean_score), params)
        feature_importances = grid_search.best_estimator_.feature_importances_
        sorted(zip(feature_importances, X_train.columns), reverse=True)
        final_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
        mse = -grid_search.best_score_
        rmse = np.sqrt(mse)
        filename = 'grd_forest_reg.pkl'
        joblib.dump(final_model, os.path.join(pickle_path,filename))
    else:
        print('Invalid search_type, please choose from {"Randomized","Grid"}')
    return cvres, best_params, rmse

def train_data(input_folder = HOUSING_PATH, processed_folder = PROCESSED_PATH, pickle_path = PICKLE_PATH, n_iter=10,cv=5,random_state=42):
    
    """Function to train data on various models such as Linear Regression, Decision Tree, Random Forest Tuned (Randomized and Grid Search)
    
    Parameters
    ----------
    input_folder: str, default "current_working_directory/data/raw"
                Path where the train and test data is stored.
                
    processed_folder: str, default "current_working_directory/data/processed"
                Path where preprocessed files (Intermediate) will be stored.
                
    pickle_path: str, default "current_working_directory/artifacts"
                Folder where trained models will be saved/stored.
                
    n_iter: int, default = 10
                Number of parameter settings that are sampled. n_iter trades off runtime vs quality of the solution.
                
    cv: int, default = 5
                cross-validation generator or an iterable.
                
    random_state: int, default = 42
    
    
    Returns
    -------
    lin_mse, lin_rmse, tree_mse, tree_rmse, best_params_rnd, rmse_rnd, best_params_grid, rmse_grid
    
    Function will pre-process train and test data, train various algorithms on train data and store the trained models in the specified folder.
    """
    os.makedirs(processed_folder, exist_ok=True)
    os.makedirs(pickle_path, exist_ok=True)
    try:
        housing_prepared, housing_labels, X_test_prepared, y_test = preprocess_data(input_folder=input_folder,
                                                                                    processed_folder=processed_folder)
        logger.info('Data processed successfuly')
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False
    
    try:
        logger.info('Starting to train data using Linear Regression...')
        pred_lr, lin_mse, lin_rmse, lin_mae = lin_reg(X_train = housing_prepared, y_train = housing_labels,\
                                                        pickle_path = pickle_path)
        logger.info('RMSE - Linear Regression: {}'.format(lin_rmse))
        logger.info('MAE - Linear Regression: {}'.format(lin_mae))
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False
    
    try:
        logger.info('Starting to train data using Decision Tree...')
        pred_dt, tree_mse, tree_rmse, tree_mae = tree_reg(X_train = housing_prepared, y_train = housing_labels,\
                                                            pickle_path = pickle_path)
        logger.info('RMSE - Decision Tree: {}'.format(tree_rmse))
        logger.info('MAE - Decision Tree: {}'.format(tree_mae))
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False
    try:
        logger.info('Starting Randomized Search for tuning Random Forest model')
        param_distribs = {
            "n_estimators": randint(low=1, high=200),
            "max_features": randint(low=1, high=8)
        }
        cvres_rnd, best_params_rnd, rmse_rnd = rf_hyperparameter_tuner(X_train = housing_prepared, y_train = housing_labels, search_type = "Randomized",\
                                            params = param_distribs, n_iter = n_iter, cv = cv, pickle_path = pickle_path,\
                                            random_state = random_state)
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False
        
    try:
        logger.info('Starting Grid Search for tuning Random Forest model')
        param_grid = [
            # try 12 (3×4) combinations of hyperparameters
            {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
#             # then try 6 (2×3) combinations with bootstrap set as False
            {"bootstrap": [False], "n_estimators": [3, 10], "max_features": [2, 3, 4]},
        ]
        cvres_grid, best_params_grid, rmse_grid = rf_hyperparameter_tuner(X_train = housing_prepared, y_train = housing_labels, search_type = "Grid",\
                                               params = param_grid, n_iter = n_iter, cv = cv, pickle_path = pickle_path,\
                                               random_state = random_state)
    except OSError as e:
        logger.error(e, exc_info=True)
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
        return False
    return lin_mse, lin_rmse, tree_mse, tree_rmse, best_params_rnd, rmse_rnd, best_params_grid, rmse_grid

if __name__ == "__main__":
    HOUSING_PATH = os.path.join(os.getcwd(),"data", "raw")
    PROCESSED_PATH = os.path.join(os.getcwd(),"data", "processed")
    PICKLE_PATH = os.path.join(os.getcwd(),'artifacts')
    
    parser = argparse.ArgumentParser()
    log_levels = {
    'critical': 'CRITERIA',
    'error':'ERROR',
    'debug': 'DEBUG',
    'info': 'INFO',
    'warning': 'WARNING',
    }

    parser.add_argument('--input_path', help='Provide path to directory where train and test data is stored',default = HOUSING_PATH)
    parser.add_argument('--processed_path', help = 'Path where processed datasets will be stored',default = PROCESSED_PATH)
    parser.add_argument('--pickle_path', help = 'Directory to save model pkls', default = PICKLE_PATH)
    parser.add_argument('--log-level',dest='log_level',\
                        help="Specify the logging level. Choose from {'DEBUG','INFO','CRITICAL','WARNING','ERROR'},\
                        Default = INFO",default='info')
    parser.add_argument('--log-path',dest='log_path', help = 'Provide a path for logs to be stored', default = False)
    parser.add_argument('--no-console-log', dest = 'console_log',help = 'Whether logs will be printed in console or not', action ='store_false')
    parser.add_argument('--console-log', dest = 'console_log',help = 'Whether logs will be printed in console or not', action ='store_true')
    args = parser.parse_args()
    level = log_levels.get(args.log_level.lower())
    if level is None:
        raise ValueError(
            f"log level given: {args.log_level}"
            f" -- must be one of: {' | '.join(log_levels.keys())}"
            )
    logger = configure_logger(log_file=args.log_path, console=args.console_log, log_level=level)
    lin_mse, lin_rmse, tree_mse, tree_rmse, best_params_rnd, rmse_rnd, best_params_grid, rmse_grid = train_data(input_folder=args.input_path,\
                                                                                                                processed_folder=args.processed_path,\
                                                                                                                pickle_path=args.pickle_path)
    logger.info('Linear regression (rmse)',str(lin_rmse))
    logger.info('DecisionTree Regression (rmse)',str(tree_rmse))
    logger.info(best_params_rnd)
    logger.info(best_params_grid)
    logger.info(rmse_rnd)
    logger.info(rmse_grid)

