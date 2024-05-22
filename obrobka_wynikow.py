import os
from tabulate import tabulate


print(os.getcwd())
os.chdir('Dane/')

os.chdir('algorytmy_planowania_czasu_CPU')                                              # do algorytmow planowania czasu CPU

f = open('Obliczone_dane.txt', 'w')
f.close()

content = os.listdir(os.getcwd())
directories = []
for element in content:
    if os.path.isdir(element):
        directories.append(element)

for directory in directories:
    tests = os.listdir(directory)
    print(f'{directory}:\n')

    f = open('Obliczone_dane.txt', 'a')
    f.write(f'{directory}:\n\n')
    f.close()

    for test in tests:
        with open(f'{directory}/{test}/Results.txt', 'r') as f:
            lines = len(f.readlines())
            f.seek(0)
            data = f.read()

        if lines < 300:
            amount = 10
        elif lines < 3000:
            amount = 100
        else:
            amount = 1000

        list_of_words = data.split()
        results = []
        for i in range(len(list_of_words)):
            if list_of_words[i] == 'wykonywania:':
                results.append(list_of_words[i+1])
        
        FCFS1 = float(results[0])
        FCFS2 = float(results[1])
        SJFnp1 = float(results[2])
        SJFnp2 = float(results[3])
        SJFp1 = float(results[4])
        SJFp2 = float(results[5])

        table = []                    
        temp = []                                  
        temp.append('AWT')
        temp.append(FCFS1)
        temp.append(SJFnp1)
        temp.append(SJFp1)
        table.append(temp)
        temp = []
        temp.append('ATAT')
        temp.append(FCFS2)
        temp.append(SJFnp2)
        temp.append(SJFp2)
        table.append(temp)

        print(f'Srednie czasy rozpoczecia i zakonczenia wykonywania dla {amount} procesow')
        print(tabulate(table, headers=[" ", "FCFS", "SJF np", "SJF p"]))
        print()

        f = open('Obliczone_dane.txt', 'a')
        f.write(f'Srednie czasy rozpoczecia i zakonczenia wykonywania dla {amount} procesow\n')
        f.write(tabulate(table, headers=[" ", "          FCFS", "       SJF np", "          SJF p"]))
        f.write('\n\n')
        f.close()

        SJFnp1_to_FCFS1 = FCFS1 / SJFnp1 * 100
        SJFnp2_to_FCFS2 = FCFS2 / SJFnp2 * 100
        SJFp1_to_FCFS1 = FCFS1 / SJFp1 * 100
        SJFp2_to_FCFS2 = FCFS2 / SJFp2 * 100
        SJFp1_to_SJFnp1 = SJFnp1 / SJFp1 * 100
        SJFp2_to_SJFnp2 = SJFnp2 / SJFp2 * 100

        table = []                                                            
        temp = []
        temp.append('AWT')
        temp.append(f'{round(SJFnp1_to_FCFS1,2 )}%')
        temp.append(f'{round(SJFp1_to_FCFS1, 2)}%')
        temp.append(f'{round(SJFp1_to_SJFnp1, 2)}%')
        table.append(temp)
        temp = []
        temp.append('ATAT')
        temp.append(f'{round(SJFnp2_to_FCFS2, 2)}%')
        temp.append(f'{round(SJFp2_to_FCFS2, 2)}%')
        temp.append(f'{round(SJFp2_to_SJFnp2, 2)}%')
        table.append(temp)

        print(tabulate(table, headers=["SJF np to FCFS", "SJF p to FCFS", "SJF p to SJF np"]))
        print()

        f = open('Obliczone_dane.txt', 'a')
        f.write(tabulate(table, headers=[" ", "SJF np to FCFS", "SJF p to FCFS", "SJF p to SJF np"]))
        f.write('\n\n\n')
        f.close()

    print('\n\n')

    f = open('Obliczone_dane.txt', 'a')
    f.write('\n\n\n----------------------------------------------------------------------------------------------------------------------------------\n\n')
    f.close()


os.chdir('../algorytmy_zastepowania_stron')                                             # do algorytmow zastepowania stron
f = open('Obliczone_dane.txt', 'w')
f.close()

content = os.listdir(os.getcwd())
directories = []
for element in content:
    if os.path.isdir(element):
        directories.append(element)

for directory in directories:
    tests = os.listdir(directory)
    print(f'{directory}:\n')

    f = open('Obliczone_dane.txt', 'a')
    f.write(f'{directory}:\n\n')
    f.close()

    results = []
    for test in tests:
        with open(f'{directory}/{test}/Results.txt', 'r') as f:
            data = f.read()

        hits = []
        faults = []
        success_rate = []
        list_of_words = data.split()
        for i in range(len(list_of_words)):
            if list_of_words[i] == 'Hits:':
                hits.append(int(list_of_words[i+1]))
            if list_of_words[i] == 'Faults:':
                faults.append(int(list_of_words[i+1]))
        
        for j in range(len(hits)):
            success_rate.append(hits[j] / (hits[j] + faults[j]) * 100)

        table = []
        temp = []
        temp.append('Hits')
        temp.append(hits[0])
        temp.append(hits[1])
        table.append(temp)
        temp = []
        temp.append('Faults')
        temp.append(faults[0])
        temp.append(faults[1])
        table.append(temp)
        temp = []
        temp.append('Success rate')
        temp.append(f'{round(success_rate[0], 2)}%')
        temp.append(f'{round(success_rate[1], 2)}%')
        table.append(temp)

        print(tabulate(table, headers=[" ", "LRU", "MFU"]))

        f = open('Obliczone_dane.txt', 'a')
        f.write(tabulate(table, headers=[" ", "LRU", "MFU"]))
        f.write('\n\n\n')
        f.close()

    print('\n\n')

    f = open('Obliczone_dane.txt', 'a')
    f.write('\n\n\n----------------------------------------------------------------------------------------------------------------------------------\n\n')
    f.close()