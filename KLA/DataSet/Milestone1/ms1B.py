
from concurrent.futures import thread
import yaml
import os
from datetime import datetime, date
import time
import sys
import threading
from threading import Thread
from concurrent import futures


def read_yaml(file_name):
    with open(file_name, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def parseit(activities, name):
    if activities['Execution'] == 'Sequential':
        sequential_flow(activities['Activities'], parent=name)
    elif activities['Execution'] == 'Concurrent':
        concurrent_flow(activities['Activities'], parent=name)


def sequential_flow(activities, parent):
    for key in activities:
        if activities[key]['Type'] == 'Task':
            print(datetime.now(), end=';')
            print(f'{parent}.{key} Entry')
            if activities[key]['Function'] == 'TimeFunction':
                input_name = activities[key]['Inputs']['FunctionInput']
                execution_time = activities[key]['Inputs']['ExecutionTime']
                print(datetime.now(), end=';')
                print(
                    f'{parent}.{key} Executing TimeFunction ({input_name}, {execution_time})')
                time.sleep(int(execution_time))

            print(datetime.now(), end=';')
            print(f'{parent}.{key} Exit')

        elif activities[key]['Type'] == 'Flow':
            print(datetime.now(), end=';')
            print(f'{parent}.{key} Entry')
            parseit(activities[key], name=parent+'.'+key)
            print(datetime.now(), end=';')
            print(f'{parent}.{key} Exit')


def execute_concurrent_task(name, input_name, execution_time, type):
    print(datetime.now(), end=';')
    print(f'{name} Entry')
    if type == 'Task':
        print(datetime.now(), end=';')
        print(f'{name} Executing TimeFunction ({input_name}, {execution_time})')
        time.sleep(int(execution_time))
    elif type == 'Flow':
        parseit(input_name, name)
    print(datetime.now(), end=';')
    print(f'{name} Exit')


def concurrent_flow(activities, parent):
    threads = []
    for key in activities:
        if activities[key]['Type'] == 'Task':
            t = Thread(target=execute_concurrent_task, args=(
                parent+'.'+key, activities[key]['Inputs']['FunctionInput'], activities[key]['Inputs']['ExecutionTime'], activities[key]['Type']))
            t.start()
            threads.append(t)
        elif activities[key]['Type'] == 'Flow':
            print(datetime.now(), end=';')
            print(f'{parent}.{key} Entry')
            if activities[key]['Execution'] == 'Sequential':
                sequential_flow(
                    activities[key]['Activities'], parent=parent+'.'+key)
            else:
                t = Thread(target=concurrent_flow, args=(
                    activities[key]['Activities'], parent+'.'+key))
                t.start()
                threads.append(t)
            print(datetime.now(), end=';')
            print(f'{parent}.{key} Exit')

    # for t in threads:
    #     if t.is_alive():
    #         t.join()
    #     else:
    #         threads.remove(t)
    flag = 1
    while flag == 1:
        flag = 0
        for t in threads:
            if t.is_alive():
                flag = 1
                break
            else:
                threads.remove(t)


def main():
    file_name = 'DataSet\Milestone1\Milestone1B.yaml'
    if os.path.exists(file_name):
        data = read_yaml(file_name)

        stdoutOrigin = sys.stdout
        sys.stdout = open("testB.txt", "w")

        name = list(data.keys())[0]
        print(datetime.now(), end=';')
        print(f'{name} Entry')
        parseit(data[name], name)

        print(datetime.now(), end=';')
        print(f'{name} Exit')

        sys.stdout.close()
        sys.stdout = stdoutOrigin


if __name__ == '__main__':
    main()
