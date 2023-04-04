
from sklearn.datasets import load_breast_cancer
import pandas as pd
import numpy as np
import dill
from kfp.v2 import dsl
from kfp.v2.dsl import (
    component,
    Output,
    Dataset
)


@component(base_image="python:3.7", target_image="get_data:v1", packages_to_install=["scikit-learn","pandas","numpy","dill"])
def get_data(dataset: Output[Dataset]):
    cancer = load_breast_cancer()
    df_cancer = pd.DataFrame(np.c_[cancer['data'], cancer['target']], columns = np.append(cancer['feature_names'], ['target']))

    with open(dataset.path, "wb") as f:
        dill.dump(df_cancer, f)
    
    print("Data saved to {}".format(dataset.path))
    
