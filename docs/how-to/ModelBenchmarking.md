# How To Update Model Benchmarking

## Overview

Word language model(WLM), NanoGPT, and Bert all have an Azure Machine Learning job that will run benchmarking for the given model.
The benchmarking job runs the same steps for the models:
- Check that Accuracy is equal to or better than the prior model.
- Check that the specified benchmarks are met.

Which prior model to compare to and which benchmarks need to be met are all configured in each models cfg file.

## Model Config file

In the directory for each model there exist a configuration yaml file.
- [WLM Config](../../src/wlm/common/wlm_config.yml)
- [NanoGPT Config](../../src/nanogpt/common/nanogpt_config.yml)
- [Bert Config](../../src/bert/common/bert_config.yml)


Each of the configuration files contain a Benchmark key.
![Benchmark key](../media/model-cfg.png)

The **Model Compare Name** key dictates which registered model to compare the accuracy too.
The **Conditions** key holds an array of benchmarks to check against. By default each model is configured to only benchmark against accuracy.

### Model Compare Name
Model names can be found on the models tab in the AML workspace. Whatever name is specified is the model that will be compared against. The comparison is done by looking at the properties of the models.

![model names](../media/model_names.png)

### Conditions
The condition key is an array. Multiple conditions can be specified and each one must be met for a model to be registered.
For Example:
```yml
conditions:
    - metric: "accuracy"
        condition: ">"
        benchmark: 0.80
    - metric: "training_time"
        condition: "<"
        benchmark: 1
    - metric: "num_predictions"
        condition: ">"
        benchmark: 5
```


To add a condition, three fields are needed: metric, condition, and benchmark.
- Metric is the name of the field in the scoring report to benchmark against.
- Condition describes the comparison to do. Currently available conditions are:
    - **>**
    - **>=**
    - **<=**
    - **<**
- Benchmark is the value that must be met given the condition.
