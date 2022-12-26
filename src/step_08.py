#  Taipy Core Data nodes - CSV, pickle
from taipy.core.config import Config, Frequency
import taipy as tp
import datetime as dt
import time


Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

# Normal function used by Taipy
def double(nb):
    return nb * 2

def add(nb):
    print("Wait 10 seconds in add function")
    time.sleep(10)
    return nb + 10

Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

# Configuration of Data Nodes
input_data_node_cfg = Config.configure_data_node("input", default_data=21)
intermediate_data_node_cfg = Config.configure_data_node("intermediate")
output_data_node_cfg = Config.configure_data_node("output")

# Configuration of tasks
first_task_cfg = Config.configure_task("double",
                                    double,
                                    input_data_node_cfg,
                                    intermediate_data_node_cfg)

second_task_cfg = Config.configure_task("add",
                                    add,
                                    intermediate_data_node_cfg,
                                    output_data_node_cfg)

# Configuration of the pipeline and scenario
pipeline_cfg = Config.configure_pipeline("my_pipeline", [first_task_cfg, second_task_cfg])



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


scenario_cfg = Config.configure_scenario("my_scenario",
                                         [pipeline_cfg],
                                         comparators={intermediate_data_node_cfg.id: compare_function})

#scenario_cfg = Config.configure_scenario_from_tasks(id="my_scenario",
#                                                    task_configs=[task_filter_by_month_cfg,
#                                                                  task_count_values_cfg])

Config.export("src/config_08.toml")

if __name__=="__main__":
    tp.Core().run()
    scenario_1 = tp.create_scenario(scenario_cfg)
    scenario_1.subscribe(callback_scenario_state)

    scenario_1.submit(wait=True)
    scenario_1.submit(wait=True, timeout=5)
     

    scenario_1 = tp.create_scenario(scenario_cfg)
    scenario_2 = tp.create_scenario(scenario_cfg)

    scenario_1.input.write(10)
    scenario_2.input.write(8)

    print("\nScenario 1: submit")
    scenario_1.submit()
    print("Value", scenario_1.output.read())

    print("\nScenario 2: first submit")
    scenario_2.submit()
    print("Value", scenario_2.output.read())


    print(tp.compare_scenarios(scenario_1, scenario_2))


    tp.Rest().run()
