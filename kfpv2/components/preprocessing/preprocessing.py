
import pandas as pd
import numpy as np
from typing import NamedTuple
import dill
from sklearn.model_selection import train_test_split
from kfp.v2 import dsl
from collections import namedtuple
from kfp.v2.dsl import (
    component,
    Input,
    Output,
    Dataset,
    Artifact,
)



@component(base_image="python:3.7", target_image="preprocessing:v1", packages_to_install=["scikit-learn","pandas","numpy","dill"])
def training_data_processing(dataset_input: Input[Dataset],split_size: float, dataset: Output[Dataset]):
    with open(dataset_input.path,"rb") as f:
        data = dill.load(f)
    target_name = 'target'
    data_target = data[target_name]
    data = data.drop([target_name], axis=1)
    # split data in x_train, x_test, y_train, y_test and x_eval, y_eval
    x_train, x_test, y_train, y_test = train_test_split(data, data_target, test_size=split_size, random_state=42)
    x_train, x_eval, y_train, y_eval = train_test_split(x_train, y_train, test_size=split_size, random_state=42)

    # save data
    with open(dataset.path, "wb") as f:
        np.savez(
            f,
            x_train=x_train,
            x_test=x_test,
            y_train=y_train,
            y_test=y_test,
            x_eval=x_eval,
            y_eval=y_eval,
        )
    print(f"Saved on : {dataset.path}")






  
