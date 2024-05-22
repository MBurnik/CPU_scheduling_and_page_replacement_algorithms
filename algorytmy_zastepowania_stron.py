import random
import os
import datetime
import csv


#-----------------------------------------------------------------------------------------------------------------------------------------
# Generacja danych

def data_generator():
    data = []
    max_data_value = 50
    memory_capacity = int(input('Wprowadz rozmiar pamieci: '))
    n = int(input('Wprowadz ilosc danych: '))
    for i in range(0, n):
        data.append(random.randint(0, max_data_value))
    print(len(data))
    print(data)

    save_data_to_file(data)

    return data, memory_capacity


#-----------------------------------------------------------------------------------------------------------------------------------------
# Operacje na plikach

def save_data_to_file(data):
    if not os.path.isdir(f'{os.getcwd()}/Dane/'):
        os.mkdir(f'{os.getcwd()}/Dane/')

    with open(f'{os.getcwd()}/Dane/Data.csv', 'w') as f:
        writer = csv.writer(f)
        for k in range(len(data)):
            writer.writerow([data[k]])


def save_results_to_file(algorithm_name, hits, faults):
    with open(f'{os.getcwd()}/Dane/Results.txt', 'a') as f:
        f.write(f'{algorithm_name}\n')
        f.write(f'Hits: {hits}\n')
        f.write(f'Faults: {faults}\n\n')


def archive_data():
    directory = datetime.datetime.fromtimestamp(os.path.getctime(f'{os.getcwd()}/Dane/Data.csv')).strftime("%Y-%m-%d_%H:%M:%S")
    # print(directory)
    if not os.path.isdir(f'{os.getcwd()}/Dane/algorytmy_zastepowania_stron'):
        os.mkdir(f'{os.getcwd()}/Dane/algorytmy_zastepowania_stron')
    os.mkdir(f'{os.getcwd()}/Dane/algorytmy_zastepowania_stron/{directory}')
    os.rename(f'{os.getcwd()}/Dane/Data.csv', f'{os.getcwd()}/Dane/algorytmy_zastepowania_stron/{directory}/Data.csv')
    os.rename(f'{os.getcwd()}/Dane/Results.txt', f'{os.getcwd()}/Dane/algorytmy_zastepowania_stron/{directory}/Results.txt')


#-----------------------------------------------------------------------------------------------------------------------------------------
# Wspólne funkcje

def show(hits, faults):
    print(f'Hits: {hits}')
    print(f'Faults: {faults}')
    

#-----------------------------------------------------------------------------------------------------------------------------------------
# Algorytm LRU

def LRU(data, memory_capacity):
    algorithm_name = 'Algorytm zastepowania stron - LRU'
    print('Algorytm zastepowania stron - LRU')

    pages = []
    faults = 0
    hits = 0

    for value in data:
        if value in pages:
            hits += 1
            pages.remove(value)                                                 # Usunięcie danej i dodane jej na koniec listy
            pages.append(value)
        
        else:
            faults += 1

            if len(pages) < memory_capacity:                                    # Dodanie danej jeżeli jest miejsce w pamięci
                pages.append(value)
            else:
                pages.remove(pages[0])                                          # Zastąpienie najrzadziej używanej danej
                pages.append(value)

        # print(pages)

    show(hits, faults)                                                          # Wypisanie wyników

    save_results_to_file(algorithm_name, hits, faults)                          # Zapisanie wyników


#-----------------------------------------------------------------------------------------------------------------------------------------
# Algorytm MFU

def MFU(data, memory_capacity):
    algorithm_name = 'Algorytm zastepowania stron - MFU'
    print('Algorytm zastepowania stron - MFU')

    pages = []
    database = dict()
    faults = 0
    hits = 0

    for value in data:
        if value in pages:
            hits += 1
            database[value] += 1                                                # Zwiększenie licznika wystąpień danej
        else:
            faults += 1

            if not value in database:                                           # Inicjalizacja licznika wystąpień dla danych
                database[value] = 0

            if len(pages) < memory_capacity:                                    # Dodanie danej jeżeli jest miejsce w pamięci
                pages.append(value)                                             # oraz zwiększenie licznika wystąpień
                database[value] += 1
            else:
                most_frequent = 0
                for i in pages:                                                 # Sprawdzenie pośród danych w pamięci,
                    frequency = database[i]                                     # która ma największą liczbę wystąpień
                    if frequency > most_frequent:                           
                        most_frequent = frequency
                        number = i

                database[number] = 0                                            # Wyzerowanie licznika wystąpień usuwanej danej
                pages.remove(number)                                            # Zastąpienie najczęściej używanej danej
                pages.append(value)                                             # oraz zwiększenie licznika wystąpień dla nowej danej
                database[value] += 1

        # print(pages)
        # print(database)

    show(hits, faults)                                                          # Wypisanie wyników

    save_results_to_file(algorithm_name, hits, faults)                          # Zapisanie wyników


#-----------------------------------------------------------------------------------------------------------------------------------------
# Główny skrypt

data, memory_capacity = data_generator()

LRU(data, memory_capacity)
MFU(data, memory_capacity)

archive_data()