
## Execution modes

Taipy has different ways to execute the code. There is two different job execution modes:
- standalone: asynchronous. Jobs can be runned in parallel depending on the graph of execution if max_nb_of_workers > 1
- development mode: synchronous

Options of submit:
- wait: if wait is True, the submit is synchronous and will wait for the end of all the jobs (if timeout is not defined)
- timeout: if wait is True, Taipy will wait for the end of the submit until a certain amount of time




```python
#  Taipy Core Data nodes - CSV, pickle
from taipy.core.config import Config, Scope, Frequency
import taipy as tp
import datetime as dt
import pandas as pd
import time
```


```python
def filter_by_month(df, month):
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df[df['Date'].dt.month == month]
    return df

def count_values(df):
    print("Wait 10 seconds")
    time.sleep(10)
    return len(df)
```


```python
Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)
```

    <taipy.core.config.job_config.JobConfig at 0x2193e63c3d0>




```python
historical_data_cfg = Config.configure_csv_data_node(id="historical_data",
                                                 default_path="time_series.csv",
                                                 scope=Scope.GLOBAL)

month_cfg = Config.configure_data_node(id="month",
                                       scope=Scope.CYCLE)

month_values_cfg =  Config.configure_data_node(id="month_data",
                                               scope=Scope.CYCLE,
                                               cacheable=True)

nb_of_values_cfg = Config.configure_data_node(id="nb_of_values",
                                              cacheable=True)


task_filter_by_month_cfg = Config.configure_task(id="filter_by_month",
                                                 function=filter_by_month,
                                                 input=[historical_data_cfg, month_cfg],
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
#                                                    task_count_values_cfg])
```


```python
if __name__=="__main__":
    tp.Core().run()
    scenario_1 = tp.create_scenario(scenario_cfg, creation_date=dt.datetime(2022,10,7), name="Scenario 2022/10/7")
    scenario_1.month.write(10)
    scenario_1.submit()
    scenario_1.submit()

    time.sleep(30)
```



```python
if __name__=="__main__":
    tp.Core().run()
    scenario_1 = tp.create_scenario(scenario_cfg, creation_date=dt.datetime(2022,10,7), name="Scenario 2022/10/7")
    scenario_1.month.write(10)
    scenario_1.submit(wait=True)
    scenario_1.submit(wait=True, timeout=5)
```
