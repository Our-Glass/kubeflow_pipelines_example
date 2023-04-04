import dill
from kfp.v2 import dsl
from collections import namedtuple
from kfp.v2.dsl import (
    component,
    Input,
    Output,
    Dataset,
    Artifact,
    Metrics,
    Model,
)
import logging
import numpy as np
from sklearn.linear_model import LogisticRegression

    
@component(packages_to_install=["numpy","scikit-learn"], target_image="train_logistic:v1")
def train_logistic_model(
    dataset: Input[Dataset],
    output_model: Output[Model],
    metrics: Output[Metrics]
):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("Loading data")
    
    with np.load(dataset.path) as data:
        # extract the variables
        x_train = data['x_train']
        x_test = data['x_test']
        y_train = data['y_train']
        y_test = data['y_test']
        x_eval = data['x_eval']
        y_eval = data['y_eval']

    model = LogisticRegression()
    model.fit(x_train, y_train)

    score = model.score(x_test, y_test)
    logger.info(f"Test score: {score}")

    # include metrics in the output
    metrics.log_metric("accuracy", score)

    # save model
    with open(output_model.path, "wb") as f:
        dill.dump(model, f)

    logger.info("Model saved to {}".format(output_model.path))

    
        

