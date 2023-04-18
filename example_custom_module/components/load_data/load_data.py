# load dataset from sklearn
import pandas as pd
from kfp.v2 import dsl
from kfp.v2.dsl import Output, Dataset
from sklearn.datasets import load_iris


# Note: Due is artifact the outputs are declarated in the arguments of the function
@dsl.component(base_image='python:3.7', target_image='mevo12318/load_data_test_custom:v1', packages_to_install=['pandas', 'scikit-learn'])
def load_data(
        X: Output[Dataset],
        y: Output[Dataset]):
    #import pandas as pd
    #from sklearn.datasets import load_iris
    
    iris = load_iris()
    X_data = pd.DataFrame(iris.data, columns=iris.feature_names)
    y_data = pd.Series(iris.target)
    
    # transform series to dataframe and add column 'y'
    y_data = pd.DataFrame(y_data, columns=['y'])
    
        
    X_data.to_csv(X.path)
    y_data.to_csv(y.path)

""" Build component
kfp components build contenerized_examples/02_pipeline_custom_component2/components/load_data/ --component-filepattern load_data.py --no-push-image
"""