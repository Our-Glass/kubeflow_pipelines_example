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
import tensorflow as tf
import numpy as np
import dill
import logging




@component(packages_to_install=["tensorflow", "numpy","dill"], target_image="train_linear:v1", output_component_file="train_tensorflow.yaml")
def train_linear_model(
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

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(1, input_shape=(30,), activation="sigmoid"))
    model.compile(
        optimizer="sgd",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(x_train, y_train, epochs=100, batch_size=1, verbose=1)

    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test loss: {loss}")
    print(f"Test accuracy: {accuracy}")

    keras_model = tf.keras.models.Model(model.inputs, model.outputs)
    keras_model.save(output_model.path)