#  Taipy Core Data nodes - CSV, pickle
from taipy.core.config import Config, Scope, Frequency
import taipy as tp
import datetime as dt
import pandas as pd
import time


def filter_by_month(df, month):
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df[df['Date'].dt.month == month]
    return df

def count_values(df):
    print("Wait 10 seconds")
    time.sleep(10)
    return len(df)


Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)


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



if __name__=="__main__":
    tp.Core().run()
    scenario_1 = tp.create_scenario(scenario_cfg, creation_date=dt.datetime(2022,10,7), name="Scenario 2022/10/7")
    scenario_1.month.write(10)
    scenario_1.submit()
    scenario_1.submit()

    time.sleep(30)


if __name__=="__main__":
    tp.Core().run()
    scenario_1 = tp.create_scenario(scenario_cfg, creation_date=dt.datetime(2022,10,7), name="Scenario 2022/10/7")
    scenario_1.month.write(10)
    scenario_1.submit(wait=True)
    scenario_1.submit(wait=True, timeout=5)