import os
import logging
import logging.config
import argparse
import mlflow
import mlflow.sklearn
import traceback
from housing_price_pred.ingest_data import download_data
from housing_price_pred.train import train_data
from housing_price_pred.score import score_models

LOGGING_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s"
            + "%(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "root": {"level": "DEBUG"},
}


def configure_logger(
    logger=None, cfg=None, log_file=None, console=True, log_level="DEBUG"
):
    """Function to setup configurations of logger through function.

    The individual arguments of `log_file`, `console`, `log_level`
    will overwrite the ones in cfg.

    Parameters
    ----------
            logger:
                    Predefined logger object if present. If None a ew logger object
                    will be created from root.
            cfg: dict()
                    Configuration of the logging to be implemented by default
            log_file: str
                    Path to the log file for logs to be stored
            console: bool
                    To include a console handler(logs printing in console)
            log_level: str
                    One of `["INFO","DEBUG","WARNING","ERROR","CRITICAL"]`
                    default - `"DEBUG"`

    Returns
    -------
    logging.Logger
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s %(funcName)s:%(lineno)d - %(message)s"
    )

    if not cfg:
        logging.config.dictConfig(LOGGING_DEFAULT_CONFIG)
    else:
        logging.config.dictConfig(cfg)

    logger = logger or logging.getLogger(__name__)

    if log_file or console:
        for hdlr in logger.handlers:
            logger.removeHandler(hdlr)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(getattr(logging, log_level))
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        if console:
            sh = logging.StreamHandler()
            sh.setLevel(getattr(logging, log_level))
            sh.setFormatter(formatter)
            logger.addHandler(sh)

    return logger



if __name__ == "__main__":
    
    # Setting mlflow server
#     mlflow server --backend-store-uri mlruns/ --default-artifact-root mlruns/ --host 0.0.0.0 --port 5000
    remote_server_uri = "http://0.0.0.0:5000" # set to your server URI
    mlflow.set_tracking_uri(remote_server_uri)  # or set the MLFLOW_TRACKING_URI in the env
    
    exp_name = 'Housing_Price_Prediction'
    mlflow.set_experiment(exp_name)

    # Setting up Argparse

    parser = argparse.ArgumentParser()
    
    log_levels = {
    'critical': 'CRITERIA',
    'error':'ERROR',
    'debug': 'DEBUG',
    'info': 'INFO',
    'warning': 'WARNING',
    }

    DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
    HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"
    HOUSING_PATH = os.path.join(os.getcwd(),"data", "raw")
    PROCESSED_PATH = os.path.join(os.getcwd(),"data", "processed")
    PICKLE_PATH = os.path.join(os.getcwd(),'artifacts')
    PRED_PATH = os.path.join(os.getcwd(),'Predictions')
    
    
    parser.add_argument('--outpath', help='Provide Output Directory',default = HOUSING_PATH)
    parser.add_argument('--processed_path', help = 'Path where processed datasets will be stored',default = PROCESSED_PATH)
    parser.add_argument('--pickle_path', help = 'Directory to save model pkls', default = PICKLE_PATH)
    parser.add_argument('--pred_path', help = 'Saved Model Predictions', default = PRED_PATH)
    parser.add_argument('--log-level',dest='log_level',\
                        help="Specify the logging level. Choose from {'DEBUG','INFO','CRITICAL','WARNING','ERROR'},\
                        Default = INFO",default='info')
    parser.add_argument('--log-path',dest='log_path', help = 'Provide a path for logs to be stored', default = False)
    parser.add_argument('--no-console-log', dest = 'console_log',help = 'Logs will not be printed on Console', action ='store_false')
    parser.add_argument('--console-log', dest = 'console_log',help = 'Logs will be printed on Console', action ='store_true')
    
    args = parser.parse_args()
    level = log_levels.get(args.log_level.lower())
    if level is None:
        raise ValueError(
            f"log level given: {args.log_level}"
            f" -- must be one of: {' | '.join(log_levels.keys())}"
            )
    logger = configure_logger(log_file=args.log_path, console=args.console_log, log_level=level)
    
    with mlflow.start_run(run_name='PARENT_RUN') as parent_run:
        with mlflow.start_run(run_name='CHILD_RUN_1', nested=True) as child_run_1:
            housing, strat_train_set, strat_test_set = download_data(housing_url = HOUSING_URL, housing_path = args.outpath)
            mlflow.log_param("URL", HOUSING_URL)
            mlflow.log_param("Data Storage", args.outpath)
        with mlflow.start_run(run_name = 'CHILD_RUN_2',nested= True) as child_run_2:
            lin_mse, lin_rmse, tree_mse, tree_rmse, best_params_rnd, rmse_rnd, best_params_grid, rmse_grid = train_data(input_folder=args.outpath,\
                                                                                                                        processed_folder=args.processed_path,\
                                                                                                                        pickle_path=args.pickle_path)
            mlflow.log_param('Linear_Regression(rmse)',lin_rmse)
            mlflow.log_param('DecisionTree_Regression(rmse)',tree_rmse)
            mlflow.log_param('RandomForest Randomized Search(Best Parameters)',best_params_rnd)
            mlflow.log_param('RandomForest Randomized Search(rmse)',rmse_rnd)
            mlflow.log_param('RandomForest Grid Search(Best Parameters)',best_params_grid)
            mlflow.log_param('RandomForest Grid Search(rmse)',rmse_grid)
        with mlflow.start_run(run_name = 'CHILD_RUN_3',nested= True) as child_run_3:
            lin_reg_rmse, tree_reg_rmse, rnd_forest_reg_rmse, grd_forest_reg_rmse = score_models(processed_folder=\
                                                                                                  args.processed_path,\
                                                                                                  pickle_path=args.pickle_path,\
                                                                                                  output_path=args.pred_path
                                                                                                  )
            
            mlflow.log_param('Linear_Regression(rmse-test-set)',lin_reg_rmse)
            mlflow.log_param('DecisionTree_Regression(rmse-test-set)',tree_reg_rmse)
            mlflow.log_param('RandomForest Randomized Search(rmse-test-set)',rnd_forest_reg_rmse)
            mlflow.log_param('RandomForest Grid Search(rmse-test-set)',grd_forest_reg_rmse)
    print("parent run_id: {}".format(parent_run.info.run_id))
    print("child run_id : {}".format(child_run_1.info.run_id))
    print("child run_id : {}".format(child_run_2.info.run_id))
    print("child run_id : {}".format(child_run_3.info.run_id))
    print("--")


