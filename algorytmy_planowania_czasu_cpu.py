import random
from tabulate import tabulate
import copy
import numpy as np
import os
import datetime
import csv


#-----------------------------------------------------------------------------------------------------------------------------------------
# Generacja danych

def data_generator():
    max_arrive_time = 60
    max_burst_time = 50
    n = int(input('Wprowadz ilosc procesow: '))
    # do generacji ze srednia i odchyleniem standardowym
    mean = float(input('Wprowadz sredni czas wykonywania procesu: '))
    standard_deviation = float(input('Wprowadz odchylenie standardowe: '))

    arrive_time = []
    burst_time = []
    for i in range(0, n):
        arrive_time.append(random.randint(0, max_arrive_time))
        # burst_time.append(random.randint(1, max_burst_time))

    # do generacji ze srednia i odchyleniem standardowym
    burst_time = np.int16(np.abs(np.random.normal(mean, standard_deviation, n)))
    for i in range(0, n):
        if burst_time[i] == 0:                                                  # Zamiana czasu wykonywania procesu na wartosc 1 w przypadku wygenerowania 0
            burst_time[i] = 1

    database = dict()
    print(burst_time)

    for i in range(n):                                                          # Stworzenie bazy procesów
        key = f'P{i+1}'
        list_times = []
        list_times.append(arrive_time[i])
        list_times.append(burst_time[i])
        database[key] = list_times

    database_sorted = sorted(database.items(), key=lambda item: item[1][0])     # Sortowanie po czasie przybycia
    print(database_sorted)
    
    keys = list(database.keys())
    save_database_to_file(keys, arrive_time, burst_time)

    return database, database_sorted, n


#-----------------------------------------------------------------------------------------------------------------------------------------
# Operacje na plikach

def save_database_to_file(keys, arrive_time, burst_time):
    if not os.path.isdir(f'{os.getcwd()}/Dane/'):
        os.mkdir(f'{os.getcwd()}/Dane/')

    with open(f'{os.getcwd()}/Dane/Data.csv', 'w') as f:
            writer = csv.writer(f)
            for k in range(len(keys)):
                writer.writerow([keys[k], arrive_time[k], burst_time[k]])


def save_results_to_file(algorithm_name, table, average_waiting_time, average_turn_around_time):
    with open(f'{os.getcwd()}/Dane/Results.txt', 'a') as f:
        f.write(f'{algorithm_name}\n')
        f.write(f'{tabulate(table, headers=["Process", "Arrival time", "Burst time", "Exit time", "Turn around time", "Waiting time"])}\n')
        f.write(f"Sredni czas oczekiwania na rozpoczecie wykonywania: {average_waiting_time}\n")
        f.write(f"Sredni czas oczekiwania na zakonczenie wykonywania: {average_turn_around_time}\n\n")


def archive_data():
    directory = datetime.datetime.fromtimestamp(os.path.getctime(f'{os.getcwd()}/Dane/Data.csv')).strftime("%Y-%m-%d_%H:%M:%S")
    # print(directory)
    if not os.path.isdir(f'{os.getcwd()}/Dane/algorytmy_planowania_czasu_CPU'):
        os.mkdir(f'{os.getcwd()}/Dane/algorytmy_planowania_czasu_CPU')
    os.mkdir(f'{os.getcwd()}/Dane/algorytmy_planowania_czasu_CPU/{directory}')
    os.rename(f'{os.getcwd()}/Dane/Data.csv', f'{os.getcwd()}/Dane/algorytmy_planowania_czasu_CPU/{directory}/Data.csv')
    os.rename(f'{os.getcwd()}/Dane/Results.txt', f'{os.getcwd()}/Dane/algorytmy_planowania_czasu_CPU/{directory}/Results.txt')


#-----------------------------------------------------------------------------------------------------------------------------------------
# Wspólne funkcje algorytmów

def add_to_queue(database_sorted, global_time, queue, j):                # Dodawanie do kolejki procesów
    if database_sorted[j][1][0] == global_time:
        key = database_sorted[j][0]
        temp = []
        temp.append(database_sorted[j][1][0])
        temp.append(database_sorted[j][1][1])
        queue[key] = temp
    return queue


def additional_info(global_time, arrive_time, burst_time, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i):
    # exit time
    exit_time.append(global_time+1)

    # turn around time, (exit - arrive)
    turn_around_time.append(exit_time[i] - arrive_time)

    # waiting time, (turn around - burst)
    waiting_time.append(turn_around_time[i] - burst_time)

    average_turn_around_time += turn_around_time[i]

    average_waiting_time += waiting_time[i]

    return exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i


def show(results, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time):
    table = []                                                              # Tworzenie tablicy po czytelne wypisanie wyników
    for i in range(len(results)):
        data = []
        data.append(results[i][0])
        data.append(results[i][1][0])
        data.append(results[i][1][1])
        data.append(exit_time[i])
        data.append(turn_around_time[i])
        data.append(waiting_time[i])
        table.append(data)

    print(tabulate(table, headers=["Process", "Arrival time", "Burst time", "Exit time", "Turn around time", "Waiting time"]))
    print(f"Sredni czas oczekiwania na rozpoczecie wykonywania: {average_waiting_time}")
    print(f"Sredni czas oczekiwania na zakonczenie wykonywania: {average_turn_around_time}")
    print()

    return table


#-----------------------------------------------------------------------------------------------------------------------------------------
# Algorytm FCFS

def FCFS(database_sorted, n):
    algorithm_name = 'Algorytm planowania czasu CPU - FCFS'
    print('Algorytm planowania czasu CPU - FCFS')

    queue = dict()
    global_time = 0
    exit_time = []
    turn_around_time = []
    waiting_time = []
    average_waiting_time = 0
    average_turn_around_time = 0
    results = []
    number_of_processes = n
    i = 0
    j = 0
    active_process = 0

    while number_of_processes > 0:
        # print(f'GLOBAL TIME: {global_time}')
        while j < n and database_sorted[j][1][0] == global_time:
            queue = add_to_queue(database_sorted, global_time, queue, j)
            j += 1

        queue_sorted = sorted(queue.items(), key=lambda item: item[1][0])       # Sortowanie po czasie przybycia
        # print('QUEUE')
        # print(queue)
        # print('SORTED QUEUE')
        # print(queue_sorted)
        
        if queue:                                                               # Pobranie procesu jeżeli jest kolejka
            if active_process == 0:
                active_process = 1
                process_name = queue_sorted[0][0]
                arrive_time = queue_sorted[0][1][0]
                burst_time = queue_sorted[0][1][1]
                temp_burst_time = burst_time

                results.append(queue_sorted[0])                                 # Dodanie danych do listy wyników   
            
            burst_time -= 1

            if burst_time == 0:
                active_process = 0

                exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i = additional_info(global_time, arrive_time, temp_burst_time, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i)

                del queue[process_name]                                         # Usunięcie procesu z kolejek

                i += 1
                number_of_processes -= 1

        global_time += 1

    average_waiting_time = (average_waiting_time/n)                             # Obliczenie średniego czasu oczekiwania na rozpoczecie wykonywania
    average_turn_around_time = (average_turn_around_time/n)                     # Obliczenie średniego czasu oczekiwania na zakonczenie wykonywania

    table = show(results, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time)    # Wypisanie wyników

    save_results_to_file(algorithm_name, table, average_waiting_time, average_turn_around_time)                         # Zapisanie wyników


#-----------------------------------------------------------------------------------------------------------------------------------------
# Algorytm SJF bez wywłaszczenia

def SJF_non_preemptive(database_sorted, n):
    algorithm_name = 'Algorytm planowania czasu CPU - SJF bez wywlaszczenia'
    print('Algorytm planowania czasu CPU - SJF bez wywlaszczenia')

    queue = dict()
    global_time = 0
    exit_time = []
    turn_around_time = []
    waiting_time = []
    average_waiting_time = 0
    average_turn_around_time = 0
    results = []
    number_of_processes = n
    i = 0
    j = 0
    active_process = 0

    while number_of_processes > 0:
        # print(f'GLOBAL TIME: {global_time}')
        while j < n and database_sorted[j][1][0] == global_time:
            queue = add_to_queue(database_sorted, global_time, queue, j)
            j += 1

        queue_sorted = sorted(queue.items(), key=lambda item: item[1][1])       # Sortowanie po czasie wykonywania
        # print('QUEUE')
        # print(queue)
        # print('SORTED QUEUE')
        # print(queue_sorted)
        
        if queue:                                                               # Pobranie procesu jeżeli jest kolejka
            if active_process == 0:
                active_process = 1
                process_name = queue_sorted[0][0]
                arrive_time = queue_sorted[0][1][0]
                burst_time = queue_sorted[0][1][1]
                temp_burst_time = burst_time

                results.append(queue_sorted[0])                                 # Dodanie danych do listy wyników

            burst_time -= 1

            if burst_time == 0:
                active_process = 0
                
                exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i = additional_info(global_time, arrive_time, temp_burst_time, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i)
                
                del queue[process_name]                                         # Usunięcie procesu z kolejek

                i += 1
                number_of_processes -= 1

        global_time += 1

    average_waiting_time = (average_waiting_time/n)                             # Obliczenie średniego czasu oczekiwania na rozpoczecie wykonywania
    average_turn_around_time = (average_turn_around_time/n)                     # Obliczenie średniego czasu oczekiwania na zakonczenie wykonywania

    table = show(results, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time)    # Wypisanie wyników

    save_results_to_file(algorithm_name, table, average_waiting_time, average_turn_around_time)                         # Zapisanie wyników


#-----------------------------------------------------------------------------------------------------------------------------------------
# Algorytm SJF z wywłaszczeniem

def SJF_preemptive(database_sorted, n):
    algorithm_name = 'Algorytm planowania czasu CPU - SJF z wywlaszczeniem'
    print('Algorytm planowania czasu CPU - SJF z wywlaszczeniem')

    queue = dict()
    global_time = 0
    exit_time = []
    turn_around_time = []
    waiting_time = []
    average_waiting_time = 0
    average_turn_around_time = 0
    results = []
    number_of_processes = n
    i = 0
    temp_database = dict()
    j = 0

    while number_of_processes > 0:
        # print(f'GLOBAL TIME: {global_time}')
        while j < n and database_sorted[j][1][0] == global_time:
            queue = add_to_queue(database_sorted, global_time, queue, j)
            j += 1

        queue_sorted = sorted(queue.items(), key=lambda item: item[1][1])       # Sortowanie po czasie wykonywania
        # print('QUEUE')
        # print(queue)
        # print('SORTED QUEUE')
        # print(queue_sorted)
        
        if queue:                                                               # Pobranie procesu jeżeli jest kolejka
            process_name = queue_sorted[0][0]
            arrive_time = queue_sorted[0][1][0]
            burst_time = queue_sorted[0][1][1]
            burst_time -= 1
            queue_sorted.pop(0)                                                 # Usunięcie z posortowanej kolejki procesu o najkrótszym czasie wykonywania
            
            if not burst_time == 0:
                temp = []
                temp.append(arrive_time)
                temp.append(burst_time)
                queue[process_name] = temp                                      # Dodanie do kolejki procesu ze zmniejszonym czasem wykonywania o 1
            else:
                del queue[process_name]                                         # Usunięcie z kolejki procesu; proces został wykonany

                temp_database[process_name] = copy.copy(database[process_name]) # Stworzenie tymczasowej kopii usuniętego procesu
                temp_database_list = list(temp_database.items())                # bezpośrednio z bazy danych po potrzebne dane do wyników

                exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i = additional_info(global_time, arrive_time, temp_database_list[i][1][1], exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time, i)

                i += 1
                number_of_processes -= 1

        global_time += 1


    temp_database = list(temp_database.items())
    for i in range(len(temp_database)):
        results.append(temp_database[i])                                        # Dodanie danych do listy wyników

    average_waiting_time = (average_waiting_time/n)                             # Obliczenie średniego czasu oczekiwania na rozpoczecie wykonywania
    average_turn_around_time = (average_turn_around_time/n)                     # Obliczenie średniego czasu oczekiwania na zakonczenie wykonywania

    table = show(results, exit_time, turn_around_time, waiting_time, average_waiting_time, average_turn_around_time)    # Wypisanie wyników

    save_results_to_file(algorithm_name, table, average_waiting_time, average_turn_around_time)                         # Zapisanie wyników


#-----------------------------------------------------------------------------------------------------------------------------------------
# Główny skrypt

database, database_sorted, n = data_generator()

FCFS(database_sorted, n)
SJF_non_preemptive(database_sorted, n)
SJF_preemptive(database_sorted, n)

archive_data()