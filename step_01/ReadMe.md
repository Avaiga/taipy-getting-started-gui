# Taipy Core

Taipy Core is one of the components of Taipy to facilitate pipeline orchestration. There are a lot of reasons for using Taipy Core:

- Taipy Core efficiently manages the execution of your functions/pipelines.

- Taipy Core manages data sources and monitors KPIs.

- Taipy Core provides easy management of multiple pipelines and end-user scenarios, which comes in handy in the context of Machine Learning or Mathematical optimization.

To apprehend the Scenario Management aspect of Taipy, you need to understand four essential concepts.

## Four fundamental concepts in Taipy Core:
- Data Nodes: are the translation of variables in Taipy. Data Nodes don't contain the data but know how to retrieve it. They can refer to any data: any Python object (string, int, list, dict, model, dataframe, etc), a Pickle file, a CSV file, an SQL database, etc. They know how to read and write data. You can even write your own custom Data Node if needed to access a particular data format.

- Tasks: are the translation of functions in Taipy.

- Pipelines: are a list of tasks executed with intelligent scheduling created automatically by Taipy. They usually represent a sequence of Tasks/functions corresponding to different algorithms like a simple baseline Algorithm or a more sophisticated Machine-Learning pipeline.

- Scenarios: End-Users very often require modifying various parameters to reflect different business situations. Taipy Scenarios will provide the framework to "play"/"execute" pipelines under different conditions/variations (i.e., data/parameters modified by the end user)


## What is a configuration?

Configuration is the structure or model of what is our scenario. It represents our Direct Acyclic Graph but also how we want our data to be stored or how our code is run. Taipy is able to create multiple instances of this structure with different data thus, we need a way to define it through this configuration step.


## Taipy Studio for configuration

There are two ways to configure Taipy Core, either by Python code or with Taipy Studio. We strongly recommend using Taipy Studio. 

Taipy Studio is a VS Code extension that provides a graphical editor to describe pipelines. Everything can be done easily and faster through Taipy Studio. 


Let's create our first configuration and then create our entities to submit.


```python
from taipy import Config
import taipy as tp

# Normal function used by Taipy
def double(nb):
    return nb * 2
```

Two Data Nodes are being configured 'input' and 'output'. The 'input' Data Node has a _default_data_ put at 21. They will be stored as Pickle files automatically and they are unique to their scenario.

The task links the two scenarios through the Python function _double_.

The pipeline will contain this one task and the scenario will contain this one pipeline.

______________________ Taipy Studio ______________________
- Create new file: 'config.toml'
- Open Taipy Studio view
- Go to the 'Config files' section of Taipy Studio
- Right click on the right configuration
- Choose 'Taipy: Show View'
- Add your first Data Node by clicking the button on the right above corner of the windows
- Create a name for it and change its details in the 'Details' section of Taipy Studio
        - name: input
        - Details: default_data=21, storage_type:pickle
- Do the same for the output
        - name: output
        - Details: storage_type:pickle
- Add a task and choose a function to associate with `<module>.<name>:function`
        - name: double
        - Details: function=`__main__.double:function`
- Link the Data Nodes and the task
- Add a pipeline and link it to the task
- Add a scenario and link to the pipeline

_______ Taipy Core _______

Here is the code to configure a simple scenario.


```python
# Configuration of Data Nodes
input_data_node_cfg = Config.configure_data_node("input", default_data=21)
output_data_node_cfg = Config.configure_data_node("output")

# Configuration of tasks
task_cfg = Config.configure_task("double",
                                 double,
                                 input_data_node_cfg,
                                 output_data_node_cfg)

# Configuration of the pipeline and scenario
pipeline_cfg = Config.configure_pipeline("my_pipeline", [task_cfg])
scenario_cfg = Config.configure_scenario("my_scenario", [pipeline_cfg])
```


```python
# Run of the Core
tp.Core().run()

# Creation of the scenario and execution
scenario = tp.create_scenario(scenario_cfg)
tp.submit(scenario)

print("Value at the end of task", scenario.output.read())
```

    [2022-12-22 16:20:02,740][Taipy][INFO] job JOB_double_699613f8-7ff4-471b-b36c-d59fb6688905 is completed.
    Value at the end of task 42
    
