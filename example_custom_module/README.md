This example contains two pipeline:
1. Hybrid pipeline: lighthweight and containerized pipeline
2. full lighthweight pipeline

The example show the principal components of KFP and how create a component with custom python module (reffer to and pipeline_lightweight.py components/load_data.py)



## Running lighthweight pipeline
![img](https://github.com/Our-Glass/kubeflow_pipelines_example/blob/main/example_custom_module/Pipeline.png)

1. Create base image with the custom modules for runing component split_data_light
```bash
python folder2docker.py \
    --path src \
    name mevo12318/base_im \
    --build \
    --push
```
Note: folder2docker.py create a requirementes.txt and Dockerfile, and if flag build & push is True, create the Image and push to dockerhub

3. Run pipeline
```bash
python pipeline_lightweight.py
```

4. Go to KFP dashboard for showing results


Note: it is not necessary build any component although I am using custom python module (src/utils.py)