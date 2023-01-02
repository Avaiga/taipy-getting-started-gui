
# Scoping 

Scoping determines how Data Nodes are shared between cycles, scenarios, and pipelines. Indeed, multiple scenarios can have their own Data Nodes or share the same one. For example, the initial/historical dataset is usually shared by all the scenarios/pipelines/cycles. It has a Global Scope and will be unique in the entire application.


```python
from taipy.core.config import Scope
```


```python
def filter_by_month(df, month):
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df[df['Date'].dt.month == month]
    return df

def count_values(df):
    return len(df)
```

- **Pipeline** scope: two pipelines can reference different Data Nodes even if their names are the same. For example, we can have a _prediction_ Data Node of an ARIMA model (ARIMA pipeline) and a _prediction_ Data Node of a RandomForest model (RandomForest pipeline). A scenario can contain multiple pipelines.

- **Scenario** scope: pipelines share the same Data Node within a scenario. 

- **Cycle** scope: scenarios from the same cycle share the same Data Node.

- **Global** scope: unique Data Node for all the scenarios/pipelines/cycles.

=== "Taipy Studio/TOML configuration"

    - Create new file: 'config_05.toml'
    - Open Taipy Studio view
    - Go to the 'Config files' section of Taipy Studio
    - Right click on the right configuration
    - Choose 'Taipy: Show View'
    - Add your first Data Node by clicking the button on the right above corner of the windows
    - Create a name for it and change its details in the 'Details' section of Taipy Studio
            - name: historical_data
            - Details: default_path=xxxx/yyyy.csv, storage_type=csv
    - Do the same for the month_data and nb_of_values
            - name: output
            - Details: storage_type:pickle
    - Add a task and choose a function to associate with `<module>.<name>:function`
            -name: filter_current
            -Details: function=`__main__.filter_current:function`
    - Do the same for count_values
    - Link the Data Nodes and the tasks
    - Add a pipeline and link it to the tasks
    - Add a scenario and link to the pipeline
    - Add the frequency property and put "WEEKLY:FREQUENCY" (DAILY, WEEKLY, MONTHLY, YEARLY)

    ```python
    Config.load('config_05.toml')

    # my_scenario is the id of the scenario configured
    scenario_cfg = Config.scenarios('my_scenario')
    ```
    
=== "Python configuration"

    ```python
    historical_data_cfg = Config.configure_csv_data_node(id="historical_data",
                                                     default_path="time_series.csv",
                                                     scope=Scope.GLOBAL)
    month_cfg =  Config.configure_data_node(id="month", scope=Scope.CYCLE)

    month_values_cfg = Config.configure_data_node(id="month_data",
                                                   scope=Scope.CYCLE)
    nb_of_values_cfg = Config.configure_data_node(id="nb_of_values")


    task_filter_by_month_cfg = Config.configure_task(id="filter_by_month",
                                                     function=filter_by_month,
                                                     input=[historical_data_cfg,month_cfg],
                                                     output=month_values_cfg)

    task_count_values_cfg = Config.configure_task(id="count_values",
                                                     function=count_values,
                                                     input=month_values_cfg,
                                                     output=nb_of_values_cfg)

    pipeline_cfg = Config.configure_pipeline(id="my_pipeline",
                                             task_configs=[task_filter_by_month_cfg,
                                                           task_count_values_cfg])

    scenario_cfg = Config.configure_scenario(id="my_scenario",
                                             pipeline_configs=[pipeline_cfg],
                                             frequency=Frequency.MONTHLY)


    #scenario_cfg = Config.configure_scenario_from_tasks(id="my_scenario",
    #                                                    task_configs=[task_filter_by_month_cfg,
    #                                                                  task_count_values_cfg])
    ```


```python
tp.Core().run()

scenario_1 = tp.create_scenario(scenario_cfg,
                                creation_date=dt.datetime(2022,10,7),
                                name="Scenario 2022/10/7")
scenario_2 = tp.create_scenario(scenario_cfg,
                               creation_date=dt.datetime(2022,10,5),
                               name="Scenario 2022/10/5")
scenario_3 = tp.create_scenario(scenario_cfg,
                                creation_date=dt.datetime(2021,9,1),
                                name="Scenario 2021/9/1")
```

Scenario 1 and 2 belongs to the same cycle so we can define the month just once for scenario 1 and 2 because month has a Cycle scope.

![](sommething.svg){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }


```python
scenario_1.month.write(10)
print("Scenario 1: month", scenario_1.month.read())
print("Scenario 2: month", scenario_2.month.read())
```
Results:
```
    Scenario 1: month 10
    Scenario 2: month 10
```


```python
print("\nScenario 1: submit")
scenario_1.submit()
print("Value", scenario_1.nb_of_values.read())
```

Results:
```
    Scenario 1: submit
    [2022-12-22 16:20:05,810][Taipy][INFO] job JOB_filter_by_month_d71cfd10-f674-40c8-b7a5-c66bea8773ef is completed.
    [2022-12-22 16:20:05,902][Taipy][INFO] job JOB_count_values_cbe0b3b3-2531-440a-9413-48845c9cfdf1 is completed.
    Value 849
```  


```python
print("Scenario 2: submit")
scenario_2.submit()
print("Value", scenario_2.nb_of_values.read())
```

Results:
```
    Scenario 2: submit
    [2022-12-22 16:20:06,356][Taipy][INFO] job JOB_filter_by_month_705fcb69-64fc-4f66-a5f3-90169e09f8bf is completed.
    [2022-12-22 16:20:06,426][Taipy][INFO] job JOB_count_values_5a8eea88-4477-48ab-a401-8036bada2267 is completed.
    Value 849
```


```python
print("\nScenario 3: submit")
scenario_3.month.write(9)
scenario_3.submit()
print("Value", scenario_3.nb_of_values.read())
```

Results:
``` 
    Scenario 3: submit
    [2022-12-22 16:20:07,404][Taipy][INFO] job JOB_filter_by_month_d0eefd6f-af96-46b8-b916-7cb94303ae4d is completed.
    [2022-12-22 16:20:07,578][Taipy][INFO] job JOB_count_values_469f6ae3-7a8a-4b65-9175-899399013f60 is completed.
    Value 1012
```

Each `nb_of_values` has their own value for each scenario, they have a Scenario scope.
