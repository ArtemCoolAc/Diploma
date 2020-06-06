import csv
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pickle
import json

def labeling(rects, labels, values, annotation):
    """Attach a text label above each bar in *rects*, displaying its height."""
    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    rect = ax.bar(x, values, 0.9, label='Б16-503 I')
    # ax.set_title('Средняя успеваемость студентов {}, {} семестр'.format(group_name, term))
    ax.set_title(annotation)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    fig.autofmt_xdate()
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def analyze_one_term(group_name='Б16-503', term=1):

    name = f'new_svod/SvodSession_{group_name}_{term}.csv'

    file = open(name, 'r')
    for i in range(4): # deleting 4 first not necessary strings
        file.readline()
    reader = csv.reader(file, delimiter=',')  # read CSV
    session = list()

    for line in reader:
        if len(line) and line[-3] != '*' and line[-3] != '#7' and line[-3] != '#0' and line[-3] != '' and \
        (line[-3] != 'а' or line[-1] != ''):  # * means that the subject wasn't chosen
            session.append(line)  # read session in a huge list

    # session.pop() # pop extra unnesessary data
    session.pop(0)

    #for line in session:
    #    if 'отч' not in line:
    #        line[2] = line[2][:-1]  # delete last \n

    mapping = {'A': '5', 'B': '4', 'C': '4', 'D': '4', 'E': '3', '': '0', 'н/а': '0'}  # ECTS to mark
    extra_mapping = {'н/а': '0'}

    session_new = dict()

    for line in session:
        line[-2] = '0'
        if len(line[-3]) > 1:  # if it is not 'a'
            if line[-3] != 'н/а':
                if line[-3][-3:] == 'н/а' and len(line[-3]) > 3:
                    line[-3] = '0'
                else:
                    line[-3] = line[-3][-1]  # н-а->{mark}, => {mark}
            line[-2] = '1'  # 0 - no-retake, 1 - retake
        line[-2] = '1' if line[-1] == 'F' else line[-2]
        if line[3] == 'Зачеты':
            line[-3] = mapping[line[-1]]  # mapping pretest '3' to mark
        # print(line)
        line[-3] = '0' if line[-3] == 'н/а' or line[-3] == '' else line[-3]
        line[-1] = 'F' if line[-1] == '' and line[-3] != 'а' else line[-1]

    for line in session:
        expultion_date = None
        if 'отч' in line[2]:
            splitted = line[2].split('отч')
            line[2] = splitted[0]
            expultion_date = splitted[1][2:]
        line[2] = line[2][:-1].strip()
        if line[2] not in session_new:  # add FIO to key of dict      
            session_new[line[2]] = list()
        session_new[line[2]].append(line)  # add subject to the list

    for key, value in session_new.items():
        """Transforming to dict with 
        {FIO}->[{ECTS},{mark},{pretest_retake}, {exam_retake}, {CP_retake}, {other_retake}, {lists}]"""
        local = dict()
        local['ECTS'] = list()
        local['mark'] = list()
        local['pretest_retake'] = list()
        local['exam_retake'] = list()
        local['CP_retake'] = list()
        local['other_retake'] = list()
        local['lists'] = list()
        local['expel'] = expultion_date
        local['rest'] = 0 # debt
        local['average'] = 0 # average student mark per term
        local['100'] = list()
        local['100_average'] = 0
        for line in value:
            local['ECTS'].append(line[-1]) if line[-1].strip() != '' else ''
            local['mark'].append(line[-3])
            if local['mark'][-1] == '6':
                local['mark'][-1] = '0'
            mapping = {'0F': 0, '1F': 25, '2F': 50, '3E': 62, '3D': 66, '4D': 71, '4C': 80, '4B': 86, '5A': 92}
            mark_id = f"{local['mark'][-1]}{local['ECTS'][-1]}"
            if mark_id in mapping:
                local['100'].append(mapping[mark_id])
            else:
                local['100'].append(0)
            local['lists'].append(line)
            if line[-2] == '1':
                if line[3] == 'Зачеты':
                    local['pretest_retake'].append((line[5], line[6], line[7]))
                elif line[3] == 'Экзамены':
                    local['exam_retake'].append((line[5], line[6], line[7]))
                elif line[3] == 'КР/КП':
                    local['CP_retake'].append((line[5], line[6], line[7]))
                else:
                    local['other_retake'].append((line[5], line[6], line[7]))
        b = list(filter(lambda x: x in ['2', '3', '4', '5'], local['mark']))
        marks_list = list(filter(lambda x: x in ['0', '1', '2', '3', '4', '5'], local['mark']))
        subjects_number = {1: 8, 2: 8, 3: 9, 4: 10, 5: 9, 6: 9}
        true_length = subjects_number[term] if len(marks_list) else len(marks_list)
        true_length = 10 if term == 5 and group_name not in ['Б16-503', 'Б16-513'] else true_length
        local['average'] = round(sum(map(int, marks_list)) / true_length, 2)
        local['100_average'] = round(sum(local['100']) / true_length)

        local['rest'] = abs(len(b) - len(local['mark']))
        session_new[key] = local

    data = dict()

    for key, value in session_new.items():
        data[key] = dict()
        for key2, value2 in value.items():
            if key2 != 'lists':
                data[key][key2] = value2
    # data.pop('sFamIO')
    data_new = copy.deepcopy(data)
    for key, value in data_new.items():
        # print(value)
        if '' in value['ECTS']:
            value['ECTS'] = list(filter(lambda a: a != '', value['ECTS']))
        if 'а' in value['mark']:
            value['mark'] = list(filter(lambda a: a != 'а', value['mark']))
        if '' in value['mark']:
            for i in range(len(value['mark'])):
                value['mark'][i] = '0'
        # print('ФАМИЛИЯ : {}'.format(key))
        # print(value)
        value['mark'] = list(map(int, value['mark']))

    # for key, value in data_new.items():
    #   ...:     mean_marks.push((key, ))


    with open(f'dicts/__Grades_dict{group_name}_{term}.txt', 'w') as file1:
        file1.write(str(data_new))

    with open(f'jsons/Grades_json{group_name}_{term}.json', 'w') as file2:
        json.dump(data_new, file2, ensure_ascii=False)

    mean_marks = list()
    for key, value in data_new.items():
        mean_marks.append((key, sum(value['mark']) / len(value['mark'])))
    labels = list(data_new.keys())
    values = [round(elem[1], 3) for elem in mean_marks]
    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    rect = ax.bar(x, values, 0.9, label='Б16-503 I')
    ax.set_title('Средняя успеваемость студентов {}, {} семестр'.format(group_name, term))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    fig.autofmt_xdate()

    # fig.xticks(x, labels, rotation='vertical')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rect)
    fig.set_size_inches(14,8)
    plt.savefig('new_graphs/Средняя успеваемость студентов {}, {} семестр'.format(group_name, term), dpi=114)
    return data_new


def analyze_all_terms(group_name='Б16-503', first=0, last=6):

    common = list()
    for i in range(first, last): 
        data = analyze_one_term(group_name, i+1) 
        common.append(data) 
    terms = [1,2,3,4,5,6]
    common_mean_values = list()
    for elem in common: 
        i = 1 
        mean_marks = list() 
        for key, value in elem.items(): 
            mean_marks.append(sum(value['mark'])/len(value['mark'])) 
        common_mean_values.append(sum(mean_marks)/len(mean_marks))
    
    labels = terms
    values = [round(elem, 3) for elem in common_mean_values]
    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    rect = ax.bar(x, values, 0.9, label='Б16-503 I')
    ax.set_title('Средняя успеваемость студентов {}, за семестры'.format(group_name))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    fig.autofmt_xdate()

    # fig.xticks(x, labels, rotation='vertical')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rect)
    fig.set_size_inches(14,8)
    plt.savefig('graphs/Средняя успеваемость студентов {}, за семестры'.format(group_name), dpi=114)
    # print(common)

if __name__ == '__main__':
    # analyze_all_terms()
    analyze_one_term('Б16-513', 1)