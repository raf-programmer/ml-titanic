#!/usr/bin/env python3
import csv
import random

# jakas zmiana

def embarked_label(embarked):
    """
    C -> 1
    Q -> 2
    S -> 3
    """
    embarked_category_mapping = {"C": 1, "Q": 2, "S": 3}
    try:
        return embarked_category_mapping[embarked]
    except KeyError:
        return random.randint(1, 3)


def sex_label(sex):
    """
    male -> 0
    female -> 1
    """
    if sex == "male":
        return 0
    if sex == "female":
        return 1


def ticket_fixed_func(ticket):
    ticket_parts = ticket.split()
    num_parts = len(ticket_parts)
    ticket_num = ticket_parts[num_parts-1]
    try:
        return int(ticket_num)
    except ValueError:
        return None


def set_ticket_fixed(ticket_num, ticket_min, ticket_max):
    if ticket_num is None:
        return random.randint(ticket_min, ticket_max)
    else:
        return int(ticket_num)


def fare_category(fare):
    """
    0-20 -> 0
    20-40 -> 1
    40-80 -> 2
    80+ -> 3
    """
    fare = float(fare)
    if fare >= 0 and fare <= 20:
        return 0
    elif fare > 20 and fare <= 40:
        return 1
    elif fare > 40 and fare <= 80:
        return 2
    elif fare > 80:
        return 3


with open('original.csv', 'r') as csvfile, open('transformed.csv', 'a') as writefile:
    fieldnames = [
        'passenger_id',
        'survived',
        'pclass',
        'name',
        'sex',
        'sex_label',
        'age',
        'sibsp',
        'parch',
        'ticket',
        'ticket_fixed',
        'fare',
        'fare_category',
        'cabin',
        'embarked',
        'embarked_category',
    ]
    reader = csv.reader(csvfile, delimiter=',')
    writer = csv.DictWriter(writefile, delimiter=';', fieldnames=fieldnames, quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # writer.writerow(record)
    writer.writeheader()
    records_list = []
    ticket_min = -1
    ticket_max = -1
    age_sum = 0
    num_records_with_age = 0
    for i, row in enumerate(reader):
        passenger_id = row[0]
        survived = row[1]
        pclass = row[2]
        name = row[3]
        sex = row[4]
        age = row[5]
        sibsp = row[6]
        parch = row[7]
        ticket = row[8]
        fare = row[9]
        cabin = row[10]
        embarked = row[11]
        if i != 0:
            ticket_num = ticket_fixed_func(ticket)
            record = {
                'passenger_id': passenger_id,
                'survived': int(survived),
                'pclass': int(pclass),
                'name': name,
                'sex': sex,
                'sex_label': int(sex_label(sex)),
                'age': age,
                'sibsp': int(sibsp),
                'parch': int(parch),
                'ticket': ticket,
                'ticket_fixed': ticket_num,
                'fare': float(fare),
                'fare_category': int(fare_category(fare)),
                'cabin': cabin,
                'embarked': embarked,
                'embarked_category': int(embarked_label(embarked)),
            }
            if ticket_num is not None:
                if ticket_num < ticket_min:
                    ticket_min = ticket_num
            if ticket_num is not None:
                if ticket_num > ticket_max:
                    ticket_max = ticket_num
            if age != '':
                age_sum += float(age)
                num_records_with_age += 1
            records_list.append(record)
    records_list.sort(key=lambda x: x['name'])
    average_age = int(age_sum/num_records_with_age)
    for record in records_list:
        # if record['cabin'] == '':
        #     continue
        record['ticket_fixed'] = set_ticket_fixed(record['ticket_fixed'], ticket_min, ticket_max)
        if record['age'] == '':
            record['age'] = average_age
        else:
            record['age'] = float(record['age'])
        writer.writerow(record)
