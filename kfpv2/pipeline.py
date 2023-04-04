
from kfp.v2 import dsl
from kubernetes import client as k8s
from kubernetes import client as k8s_client
from components.preprocessing.preprocessing import training_data_processing
from components.dataextraction.dataextraction import get_data
from components.train_linear.train_linear import train_linear_model
from components.train_logistic.train_logistic import train_logistic_model


# create a breast cancer pipeline
@dsl.pipeline(
    name='Breast Cancer Pipeline',
    description='A pipeline to predict breast cancer'
)
def breast_cancer_pipeline(
    split_size: float = 0.2
):
    # get data
    get_data_task = get_data()
    # split data
    split_data_task = training_data_processing(dataset_input=get_data_task.outputs['dataset'],split_size=split_size)
    train_linear_model_task = train_linear_model(dataset=split_data_task.outputs['dataset'])
    train_logistic_model_task = train_logistic_model(dataset=split_data_task.outputs['dataset'])
    # TODO: add a component to evaluate the model

if __name__ == '__main__':
    import kfp
    EXPERIMENT_NAME = 'brest_cancer'
    pipelineGzFile = 'breast_cancer.zip'

    kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=breast_cancer_pipeline,
        package_path=pipelineGzFile)



# run the pipeline

    client = kfp.Client()
    my_exp = client.create_experiment(
        name=EXPERIMENT_NAME
    )
    my_run = client.run_pipeline(
        my_exp.id, 
        'breast_cancer_pipeline', 
        pipelineGzFile,
        #enable_caching=False
    )