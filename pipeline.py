import kfp
import kfp.dsl as dsl
from kubernetes import client as k8s
from kubernetes import client as k8s_client

EXPERIMENT_NAME = 'Sentiment Analysis Pipeline'
IMAGE_USERNAME = <your docker hub username>

client = kfp.Client()

@dsl.pipeline(
    name='Sentiment Analysis Pipeline',
    description='A pipeline to analyze sentiment of BTS videos'
)
def sentiment_analysis_pipeline(

    data_extraction_image=f'{IMAGE_USERNAME}/dataextraction:latest',
    preprocessing_image=f'{IMAGE_USERNAME}/preprocessing:latest',
    data_file='/mnt/bts.data',
    train_file='/mnt/bts_train.data',
    test_file='/mnt/bts_test.data',
    validation_file='/mnt/bts_validation.data',
    preprocess_file='/mnt/bts_preprocessed.data',
    split_size=0.2,

):

    vop = dsl.VolumeOp(
        name="create_pvc",
        resource_name="bts-pvc",
        modes=dsl.VOLUME_MODE_RWO,
        size="1Gi"
    )

    data_extraction_op = dsl.ContainerOp(
            name='data_extraction',
            image=data_extraction_image,
            command=['python'],
            arguments=['/app/dataextraction.py',"--data_file", data_file,],
            pvolumes={"/mnt": vop.volume}
        )

    preprocessing_op = dsl.ContainerOp(
            name='preprocessing',
            image=preprocessing_image,
            command=['python'],
            arguments=[
                '/app/preprocessing.py',
                '--data_file', data_file,
                '--preprocess_file', preprocess_file,
                '--train_file', train_file,
                '--test_file', test_file,
                '--validation_file', validation_file,
                '--split_size', split_size,
                ],
            pvolumes={"/mnt": data_extraction_op.pvolume}
        )


if __name__ == '__main__':
    import kfp.compiler as compiler
    pipeline_func = sentiment_analysis_pipeline
    pipeline_filename = pipeline_func.__name__ + '.pipeline.zip'
    compiler.Compiler().compile(pipeline_func, pipeline_filename)

    try:
        experiment = client.create_experiment(EXPERIMENT_NAME)
    except:
        experiment = client.create_experiment(EXPERIMENT_NAME)


    arguments = {}
    run_name = pipeline_func.__name__ + ' sentiment_run'
    run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename, arguments)

    print(run_result)
    print(run_name)
    print(pipeline_filename)
    print(arguments)








            
