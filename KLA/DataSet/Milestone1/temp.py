
from importlib.abc import Loader
from webbrowser import open_new
import yaml
from datetime import datetime
import time

now = datetime.now()
# print("now =", now)
res_lst = []
with open('DataSet\Milestone1\Milestone1A.yaml') as f:
    yaml_contents = yaml.load_all(f, Loader=yaml.FullLoader)
    for yaml_content in yaml_contents:
        # print(str(now) + ';M1A_Workflow Entry')
        res_lst.append(f"{str(datetime.now())};M1A_Workflow Entry")
        s = "M1A_Workflow"
        # print(yaml_content['M1A_Workflow']['Activities'])
        activity = yaml_content['M1A_Workflow']['Activities']
        # print(activity)

        for k, v in activity.items():
            # now = datetime.now()
            if 'Task' in k:
                # print(k)
                # print(v)
                function = ""
                function_input = ""
                execution_time = 0
                for k_, v_ in v.items():
                    if k_ == 'Function':
                        function = v_
                    if k_ == 'Inputs':
                        function_input = v_['FunctionInput']
                    if k_ == 'Inputs':
                        execution_time = v_['ExecutionTime']
                res_lst.append(f"{str(datetime.now())};{s}.{k} Entry")
                res_lst.append(
                    f"{str(datetime.now())};{s}.{k} Executing {function}({function_input}, {str(execution_time)})")

                if(int(execution_time) > 0):
                    time.sleep(int(execution_time))
                # res_lst.append(str(datetime.now()) + ';'+s+'.'+k + ' Exit')
                res_lst.append(f"{str(datetime.now())};{s}.{k} Exit")
            else:
                # print(k)
                # print(v)
                subtask = k
                activities = v['Activities']
                # print(activities)
                stack_lst = []
                res_lst.append(f"{str(datetime.now())};{s}.{subtask} Entry")
                for k, v in activities.items():
                    function = ""
                    function_input = ""
                    execution_time = 0

                    for k_, v_ in v.items():
                        if k_ == 'Function':
                            function = v_
                        if k_ == 'Inputs':
                            function_input = v_['FunctionInput']
                        if k_ == 'Inputs':
                            execution_time = v_['ExecutionTime']

                    res_lst.append(
                        f"{str(datetime.now())};{s}.{subtask}.{k} Entry")
                    res_lst.append(
                        f"{str(datetime.now())};{s}.{subtask}.{k} Executing {function} ({function_input}, {str(execution_time)})")

                    if(int(execution_time) > 0):
                        time.sleep(int(execution_time))
                    stack_lst.append(
                        f"{str(datetime.now())};{s}.{subtask}.{k} Exit")
                for lst in stack_lst:
                    res_lst.append(lst)
                res_lst.append(f"{str(datetime.now())};{s}.{subtask} Exit")
        res_lst.append(f"{str(datetime.now())};M1A_Workflow Exit")

textfile = open("test.txt", "w")
for element in res_lst:
    textfile.write(element + "\n")
textfile.close()
