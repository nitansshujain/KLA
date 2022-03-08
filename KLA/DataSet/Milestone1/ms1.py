from msilib import sequence
import os
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_HASH_VALUE
import sys
from time import time
from traceback import print_tb
import yaml
import os
from datetime import datetime, date
import time
import sys


def read_yaml(file_name):
    with open(file_name, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def write_yaml(file_name, data):
    with open(file_name, 'w') as f:
        yaml.dump(data, f)


def parse(activities, name):
    if activities['Execution'] == 'Sequential':
        sequential_flow(activities['Activities'], parent=name)
    elif activities['Execution'] == 'Concurrent':
        concurrent_flow(activities['Activities'], parent=name)


def concurrent_flow(activities):
    for activity in activities:
        print(activity)


def sequential_flow(activities, parent):
    for key in activities:
        if(activities[key]['Type'] == 'Task'):
            print(datetime.now(), end=';')
            print(f"{parent}.{key} Entry")

            if(activities[key]['Function'] == 'TimeFunction'):
                input_name = activities[key]['Inputs']['FunctionInput']
                execution_time = activities[key]['Inputs']['ExecutionTime']
                print(datetime.now(), end=';')
                print(
                    f"{parent}.{key} Executing TimeFunction ({input_name}, {execution_time})")
                time.sleep(int(execution_time))
            print(datetime.now(), end=';')
            print(f"{parent}.{key} Exit")
        elif(activities[key]['Type'] == 'Flow'):
            print(datetime.now(), end=';')
            print(f"{parent}.{key} Entry")
            parse(activities[key], name=parent+'.'+key)
            print(datetime.now(), end=';')
            print(f"{parent}.{key} Exit")


def main():
    file_name = 'DataSet\Milestone1\Milestone1A.yaml'
    if(os.path.exists(file_name)):
        data = read_yaml(file_name)

        stdoutOrigin = sys.stdout
        sys.stdout = open("test.txt", "w")

        name = list(data.keys())[0]
        print(datetime.now(), end=';')
        print(f"{name} Entry")

        parse(data[name], name)
        print(datetime.now(), end=';')
        print(f"{name} Exit")

        sys.stdout.close()
        sys.stdout = stdoutOrigin


if __name__ == '__main__':
    main()
