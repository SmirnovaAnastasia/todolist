from Function.functions import day_list, list_not_ready, lift_arch
from datetime import datetime

while(True):
    now = datetime.now().strftime("%d.%m.%Y")
    # now = "28.10.2025"
    # print(now)

    print(f'=Здравствуй! Сегодня {now}. Что вы хотите сделать?=')
    print(f'1. Открыть список на день\n2. Открыть список невыполненных дел\n3. Открыть архив\n4. Выйти')
    num_var = input("Введите номер:")
    print()

    match num_var:
        case "1":
            day_list(now)
        case "2":
            list_not_ready()
        case "3":
            lift_arch(now)
        case "4":
            exit(0)
        case _:
            print("Введен неправильный номер!")


