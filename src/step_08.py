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


def callback_scenario_state(scenario, job):
    """All the scenarios are subscribed to the callback_scenario_state function. It means whenever a job is done, it is called.
    Depending on the job and the status, it will update the message stored in a json that is then displayed on the GUI.

    Args:
        scenario (Scenario): the scenario of the job changed
        job (_type_): the job that has its status changed
    """
    print(scenario.name)
    if job.status.value == 7:
        for data_node in job.task.output.values():
            print(data_node.read())


if __name__=="__main__":
    tp.Core().run()
    scenario_1 = tp.create_scenario(scenario_cfg, creation_date=dt.datetime(2022,10,7), name="Scenario 2022/10/7")
    scenario_1.subscribe(callback_scenario_state)

    scenario_1.submit(wait=True)
    scenario_1.submit(wait=True, timeout=5)


def compare_function(*data_node_results):
    compare_result= {}
    current_res_i = 0
    for current_res in data_node_results:
        compare_result[current_res_i]={}
        next_res_i = 0
        for next_res in data_node_results:
            print(f"comparing result {current_res_i} with result {next_res_i}")
            compare_result[current_res_i][next_res_i] = next_res - current_res
            next_res_i += 1
        current_res_i += 1
    return compare_result


scenario_cfg = Config.configure_scenario("multiply_scenario",
                                         [pipeline_cfg],
                                         comparators={month_cfg.id: compare_function},
                                         frequency=Frequency.MONTHLY)

#scenario_cfg = Config.configure_scenario_from_tasks(id="my_scenario",
#                                                    task_configs=[task_filter_by_month_cfg,
#                                                                  task_count_values_cfg])

if __name__=="__main__":   
    tp.Core().run()

    scenario_1 = tp.create_scenario(scenario_cfg,
                                    creation_date=dt.datetime(2022,10,7),
                                    name="Scenario 2022/10/7")
    scenario_2 = tp.create_scenario(scenario_cfg,
                                    creation_date=dt.datetime(2022,8,5),
                                    name="Scenario 2022/8/5")

    scenario_1.month.write(10)
    scenario_2.month.write(8)
    print("Scenario 1: month", scenario_1.month.read())
    print("Scenario 2: month", scenario_2.month.read())

    print("\nScenario 1: submit")
    scenario_1.submit()
    print("Value", scenario_1.nb_of_values.read())

    print("\nScenario 2: first submit")
    scenario_2.submit()
    print("Value", scenario_2.nb_of_values.read())


    print(tp.compare_scenarios(scenario_1, scenario_2))


    tp.Rest().run()
