import json

from dns.name import empty
from Function.database import get_all_tasks, overwrite_from_all_rows

file_name = 'days.json'

def print_doings(date, doings): # print doings
    print(f'={date[8:] + date[4:8] + date[:4]}=')
    num = 1

    for i in doings:
        if str(i[0]) == date:
            for j in i[1]:
                print(str(num).ljust(3), str(j[0]).ljust(30), end=' ')
                if j[1] is True:
                    print('[Сделано]'.ljust(12), end=' ')
                else:
                    print('[Не сделано]', end=' ')

                if j[2] is True:
                    print('[Нужно]'.ljust(9), end=' ')
                else:
                    print('[Ненужно]', end=' ')
                num += 1
                print()
            print()

def add_new_task(result, what, date): # add new doing
    for i in range(len(result)):
        if str(result[i][0]) == date:
            new_doing = [what, False, True]
            result[i][1].append(new_doing)

    overwrite_from_all_rows(result)



def change_doings(ch_num, result, num, date): # change status or relevance (this day)
    what = 1

    for i in range(len(result)):
        if str(result[i][0]) == date:
            for j in range(len(result[i][1])):

                if what == int(ch_num):
                    if int(num) == 1:
                        if result[i][1][j][1] is False:
                            result[i][1][j][1] = True
                        else:
                            result[i][1][j][1] = False
                    else:
                        if result[i][1][j][2] is False:
                            result[i][1][j][2] = True
                        else:
                            result[i][1][j][2] = False
                what += 1

    overwrite_from_all_rows(result)

def change_doings2(ch_num, result, num): # change status or relevance (arch)
    what = 1
    for i in range(len(result)):
        for j in range(len(result[i][1])):
            if what == int(ch_num) and result[i][1][j][1] is False:
                if num == 1:
                    if result[i][1][j][1] is False:
                        result[i][1][j][1] = True
                    else:
                        result[i][1][j][1] = False
                else:
                    if result[i][1][j][2] is False:
                        result[i][1][j][2] = True
                    else:
                        result[i][1][j][2] = False

                what += 1
            elif result[i][1][j][1] is False:
                what += 1

    overwrite_from_all_rows(result)


def more_actions(result, date): # menu to change doings (for this day)
    print(f'1. Добавить новую запись\n2. Изменить статус\n3. Изменить нужность\n4. Выйти')

    num_var = input("Print number:")
    print()
    match num_var:
        case "1":
            what = input("Print a doing:")
            add_new_task(result, what, date)
        case "2":
            ch_num = input("Print number to change:")
            print()

            change_doings(ch_num, result, 1, date)
        case "3":
            ch_num = input("Print number to change:")
            print()

            change_doings(ch_num, result, 2, date)
        case "4":
            pass

    return num_var

def more_actions2(result): # menu to change doings (arch)
    print(f'1. Изменить статус\n2. Изменить нужность\n3. Выйти')

    num_var = input("Print number:")
    print()
    match num_var:
        case "1":
            ch_num = input("Print number to change:")
            print()

            change_doings2(ch_num, result, 1)
        case "2":
            ch_num = input("Print number to change:")
            print()

            change_doings2(ch_num, result, 2)
        case "3":
            pass

    return num_var

def day_list(date): # open this day list
    num = 0
    here = 1

    while num != 4:
        all_tasks = get_all_tasks()

        for i in all_tasks:
            if str(i[0]) == date:
                # print('find!')
                here = 0

        if here == 1:
            new_part = (date, [])

            all_tasks.append(new_part)
            overwrite_from_all_rows(all_tasks)


        print_doings(date, all_tasks)
        num = int(more_actions(all_tasks, date))

    return


def list_not_ready(): # open not ready list
    num = 0
    while num != 3:
        number = 1
        all_tasks = get_all_tasks()
        for i in all_tasks:
            print(f'={i[0][8:] + i[0][4:8] + i[0][:4]}=')
            for j in i[1]:
                if j[1] is False:
                    print(str(number).ljust(3), str(j[0]).ljust(30), end=' ')
                    if j[1] is True:
                        print('[Сделано]'.ljust(12), end=' ')
                    else:
                        print('[Не сделано]', end=' ')

                    if j[2] is True:
                        print('[Нужно]'.ljust(9), end=' ')
                    else:
                        print('[Ненужно]', end=' ')
                    number += 1
                    print()
            print()

        num = int(more_actions2(all_tasks))
    return

def lift_arch(date): # open arch list
    num = 0
    all_tasks = get_all_tasks()
    for i in all_tasks:
        if str(i[0]) != date:
            print(f'={i[0][8:] + i[0][4:8] + i[0][:4]}=')
            for j in i[1]:
                print(str(num).ljust(3), str(j[0]).ljust(15), end=' ')
                if j[1] is True:
                    print('[Сделано]'.ljust(12), end=' ')
                else:
                    print('[Не сделано]', end=' ')

                if j[2] is True:
                    print('[Нужно]'.ljust(9), end=' ')
                else:
                    print('[Ненужно]', end=' ')
                num += 1
                print()
            print()

    return
