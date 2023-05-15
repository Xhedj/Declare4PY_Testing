import os.path
from os import path, listdir
import sys
import time
import csv
import pdb
import pm4py

from src.Declare4Py.ProcessMiningTasks.ConformanceChecking.LTLAnalyzer import LTLAnalyzer
from src.Declare4Py.ProcessModels.LTLModel import LTLModelTemplate

#event_log = D4PyEventLog()
list_logs = listdir("/home/xhedj/Desktop/test_logs")
template_list = ["eventually_activity_a", "eventually_a_then_b", "eventually_a_or_b", "eventually_a_next_b_next_c"]
sepsis_parameters = [["ER Triage"], ["ER Triage", "CRP"],["ER Triage", "CRP"], ["ER Triage", "CRP", "LacticAcid"]]
bpic_parameters = [["Permit FINAL_APPROVED by SUPERVISOR"], ["Declaration SUBMITTED by EMPLOYEE", "Declaration "
                                                                                    "FINAL_APPROVED by SUPERVISOR"],
                   ["Declaration SUBMITTED by EMPLOYEE", "End trip"], ["End trip", "Permit FINAL_APPROVED by SUPERVISOR",
                                                       "Declaration SUBMITTED by EMPLOYEE"]]


for i in range(len(list_logs)):
    log_name = list_logs[i]
    log = pm4py.read_xes("/home/xhedj/Desktop/test_logs" + "/" + list_logs[i])
    print(log_name)
    parameters = []
    name = log_name.replace('.xes', '.csv')
    if log_name == "Sepsis Cases - Event Log.xes":
        parameters = sepsis_parameters
    else:
        parameters = bpic_parameters
    print(parameters)
    print(name)
    for i in range(4):
        template = template_list[i]
        param = parameters[i]
        template_model = LTLModelTemplate(template)
        print(param)
        model = template_model.get_templ_model(param)
        analyzer = LTLAnalyzer()
        analyzer.data_frame = log
        analyzer.ltl_model = model
        temp = []
        for j in range(5):
            start = time.time()
            analyzer.run()
            end = time.time()
            exec_time = end - start
            temp.append(exec_time)
        with open('/home/xhedj/Desktop/test_results/optimized_no_parallel/' + name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(temp)


