import json

file_name = 'days.json'

def print_doings(date, doings): # print doings
    print(f'={date}=')
    num = 1

    for i in doings:
        for k in i:
            print(str(num).ljust(3), str(k[0]).ljust(15), end=' ')
            if k[1] is True:
                print('[Сделано]'.ljust(12), end=' ')
            else:
                print('[Не сделано]', end=' ')

            if k[2] is True:
                print('[Нужно]'.ljust(9), end=' ')
            else:
                print('[Ненужно]', end=' ')
            num += 1
            print()
    print()

def add_new_task(result, what, date): # add new doing
    for i in range(len(result)):
        if result[i]["time"] == date:
            new_doing = [what, False, True]
            result[i]["doings"].append(new_doing)

    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file)

def change_doings(ch_num, result, num, date): # change status or relevance (this day)
    what = 1
    for i in range(len(result)):
        if result[i]["time"] == date:
            # print(f'res[i]["doings"] : {result[i]["doings"][0]}')
            for j in range(len(result[i]["doings"])):
                if what == int(ch_num):
                    if num == 1:
                        if result[i]["doings"][j][1] is False:
                            result[i]["doings"][j][1] = True
                        else:
                            result[i]["doings"][j][1] = False
                    else:
                        if result[i]["doings"][j][2] is False:
                            result[i]["doings"][j][2] = True
                        else:
                            result[i]["doings"][j][2] = False
                what += 1

    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file)

def change_doings2(ch_num, result, num): # change status or relevance (arch)
    what = 1
    for i in range(len(result)):
        for j in range(len(result[i]["doings"])):
            if what == int(ch_num) and result[i]["doings"][j][1] is False:
                if num == 1:
                    if result[i]["doings"][j][1] is False:
                        result[i]["doings"][j][1] = True
                    else:
                        result[i]["doings"][j][1] = False
                else:
                    if result[i]["doings"][j][2] is False:
                        result[i]["doings"][j][2] = True
                    else:
                        result[i]["doings"][j][2] = False

                what += 1
            elif result[i]["doings"][j][1] is False:
                what += 1

    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file)


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
    while num != 4:
        doings = []
        here = 1
        new_part = []

        with open(file_name, 'r', encoding='utf-8') as f:
            try:
                result = json.load(f)
                ind = 0
                for i in result:
                    if str(i["time"]) == date:
                        doings.append(i["doings"])
                        here = 0

            except json.decoder.JSONDecodeError:
                pass

        if here == 1:
            new_part = {"time": date, "doings": []}

            result.append(new_part)
            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file)

        print_doings(date, doings)
        num = int(more_actions(result, date))
    return


def list_not_ready(): # open not ready list
    num = 0
    while num != 3:
        num_of_doing = 1
        with open(file_name, 'r', encoding='utf-8') as f:
            try:
                result = json.load(f)
                for i in result:
                    print(f'={i["time"]}=')
                    for j in i["doings"]:
                        if j[1] is False:
                            print(str(num_of_doing).ljust(3), str(j[0]).ljust(15), end=' ')
                            print('[Не сделано]', end=' ')

                            if j[2] is True:
                                print('[Нужно]'.ljust(9), end=' ')
                            else:
                                print('[Ненужно]', end=' ')
                            num_of_doing += 1
                            print()
                    print()
            except json.decoder.JSONDecodeError:
                pass

        num = int(more_actions2(result))
    return

def lift_arch(date): # open arch list
    num = 1
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            result = json.load(f)
            for i in result:
                if str(i["time"]) != date:
                    print(f'={i["time"]}=')
                    for j in i["doings"]:
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
        except json.decoder.JSONDecodeError:
            pass
