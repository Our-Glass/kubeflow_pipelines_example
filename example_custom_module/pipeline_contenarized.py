import kfp
from kfp.v2 import dsl
# Load components
from components.load_data.load_data import load_data
from components.print_meta.print_meta import print_meta
from components.split_data_custom.split_data_custom import split_data_custom as split_data

# Declare pipeline
@dsl.pipeline(name='pipeline artifcats')
def pipeline_custom_module_artifacts() -> str:
        task_load_data = load_data()
        task_split_data = split_data( x=task_load_data.outputs['X'], y=task_load_data.outputs['y'])
        task_split_data.enable_caching = False
        # task_print = print_meta(
        #         x_train=task_split_data.outputs['x_train_out'],
        #         x_test=task_split_data.outputs['x_test_out'])
        return "task_print.output"


NAME_EXPERIMENT = '02_pipeline_artifacts'
OUTPUT_FILE = '02_pipeline_artifacts.zip'

# Compile
kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=pipeline_custom_module_artifacts,
        package_path=OUTPUT_FILE)
        

# Instance client
client = kfp.Client()

# Create experiment
my_exp = client.create_experiment(name=NAME_EXPERIMENT)

# Run pipeline
my_run = client.run_pipeline(
        experiment_id = my_exp.id,
        job_name = 'pipeline_custom_module_artifacts',
        pipeline_package_path = OUTPUT_FILE
)
""" for running
python contenerized_examples/02_pipeline_custom_component2/pipeline.py
"""