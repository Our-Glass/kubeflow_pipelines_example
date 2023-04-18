import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import Input, Output, Dataset, Model


@dsl.component(packages_to_install=['pandas', 'scikit-learn'])
def load_data(
        X: Output[Dataset],
        y: Output[Dataset]):
        import pandas as pd
        from sklearn.datasets import load_iris
        
        iris = load_iris()
        X_data = pd.DataFrame(iris.data, columns=iris.feature_names)
        y_data = pd.Series(iris.target)
        
        # transform series to dataframe and add column 'y'
        y_data = pd.DataFrame(y_data, columns=['y'])
        
        X_data.to_csv(X.path)
        y_data.to_csv(y.path)


# split_data_light --> lightweigth component with custom python model
@dsl.component(base_image='mevo12318/base_im:latest', packages_to_install=['pandas', 'scikit-learn'])
def split_data_light(
        x: Input[Dataset],
        y: Input[Dataset],
        x_train_out: Output[Dataset],
        x_test_out: Output[Dataset]):

        # Import libraries
        import pandas as pd
        from src.utils import parse_df
        from sklearn.model_selection import train_test_split
        
        # Load data from input
        with open(x.path, "rb") as f:
                X_data = pd.read_csv(f)
        with open(y.path, "rb") as f:
                y_data = pd.read_csv(f)

        print(f"type(x) = {type(X_data)}")
        print(f"type(y) = {type(y_data)}")
                
        # Split data
        x_train, x_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=42)
        
        # Parse data
        x_train, x_test = parse_df(x_train, x_test, y_train, y_test)
        
        # save data
        with open(x_train_out.path, "wb") as f:
                x_train.to_csv(f)
        with open(x_test_out.path, "wb") as f:
                x_test.to_csv(f)


@dsl.component(packages_to_install=['pandas'])
def print_meta(
        x_train: Input[Dataset],
        x_test: Input[Dataset],
        ) -> str:
        import pandas as pd
        

        # Load data from input
        with open(x_train.path, "rb") as f:
                X_train = pd.read_csv(f)
        with open(x_test.path, "rb") as f:
                X_test = pd.read_csv(f)
        
        len_X_train = len(X_train)
        path_X_train = x_train.path
        uri_X_train = x_train.uri
        
        len_X_test = len(X_test)
        path_X_test = x_test.path
        uri_X_test = x_test.uri
        
        return f"""
        len_X_train: {len_X_train}
        path_X_train: {path_X_train}
        uri_X_train: {uri_X_train}
        
        len_X_test: {len_X_test}
        path_X_test: {path_X_test}
        uri_X_test: {uri_X_test}
        """


@dsl.component(packages_to_install=['pandas', 'scikit-learn', 'pickle5'])
def train_model(
        x_train: Input[Dataset],
        model_out: Output[Model]):
        import pickle
        import pandas as pd
        from sklearn.linear_model import LinearRegression

        # Load data from input
        with open(x_train.path, "rb") as f:
                X_train = pd.read_csv(f)
        
        # Train model
        y_train = X_train['y']
        X_train = X_train.drop(['y'], axis=1)
        
        # create model for classification iris dataset
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # save model
        with open(model_out.path, "wb") as f:
                pickle.dump(model, f)


@dsl.component(packages_to_install=['pandas', 'pickle5'])
def test_model(
        x_test: Input[Dataset],
        model_in: Input[Model]) -> str:
        import pickle
        import pandas as pd

        # Load data from input
        with open(x_test.path, "rb") as f:
                X_test = pd.read_csv(f)
        
        # Load model
        with open(model_in.path, "rb") as f:
                model = pickle.load(f)
        
        # Test model
        y_test = X_test['y']
        X_test = X_test.drop(['y'], axis=1)
        
        # Get metrics
        score = model.score(X_test, y_test)
        
        return f"score: {score}"
        

# Declare pipeline
@dsl.pipeline(name='pipeline artifcats')
def pipeline_custom_module_artifacts_light() -> str:
        task_load_data = load_data()
        task_split_data = split_data_light( x=task_load_data.outputs['X'], y=task_load_data.outputs['y'])
        task_print = print_meta(
                x_train=task_split_data.outputs['x_train_out'],
                x_test=task_split_data.outputs['x_test_out'])        
        task_train_model = train_model( x_train=task_split_data.outputs['x_train_out'])
        task_test_model = test_model( x_test=task_split_data.outputs['x_test_out'], model_in=task_train_model.outputs['model_out'])

        return task_print.output


NAME_EXPERIMENT = '02_pipeline_artifacts_light'
OUTPUT_FILE = '02_pipeline_artifacts_light.zip'

# Compile
kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=pipeline_custom_module_artifacts_light,
        package_path=OUTPUT_FILE)
        

# Instance client
client = kfp.Client()

# Create experiment
my_exp = client.create_experiment(name=NAME_EXPERIMENT)

# Run pipeline
my_run = client.run_pipeline(
        experiment_id = my_exp.id,
        job_name = 'pipeline_custom_module_artifacts_light',
        pipeline_package_path = OUTPUT_FILE
)
""" for running
python contenerized_examples/02_pipeline_custom_component2/pipeline.py
"""