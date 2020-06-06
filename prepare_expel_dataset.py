import os
import json
from collections import Counter

def names():
    transferred_from_department = ['СКВОРЦОВ М.С.', 'АФАНАСЬЕВ А.А.', 'БЕЛЯЕВА Е.В.', 'АХМАДАЛИЕВА Ф.А.',
                                   'ДОДОНОВ А.Д.', 'КАДЫРОВ Э.З.', 'КУХАРЁНОК О.С.', 'ТОПАЛЭ М.С.', 
                                   'БЕРЕЗОВСКАЯ Г._.', 'ЗИАТДИНОВА К.Р.', 'ШАНЫГИН Д.С.']

    expelled_in_sixth_term = ['ДОНЕНКО А.С.', 'КОНИНА А.О.', 'СТРУБАЛИНА Т.А.']

    return transferred_from_department, expelled_in_sixth_term


def merge_preliminary_data(groups):
    frame = dict()
    for group in groups:
        for i in range(6):
            check_file = os.path.exists(f'jsons/Grades_json{group}_{i+1}.json')
            if check_file:
                file = open(f'jsons/Grades_json{group}_{i+1}.json')
                j = json.load(file)
                for key, value in j.items():
                    if key not in frame:
                        frame[key] = list()
                    frame[key].append(
                        (i + 1,
                         len(value['pretest_retake']),
                         len(value['exam_retake'])+len(value['CP_retake']),
                         value['average'])
                    )
                file.close()
    return frame


def correct_dataset(frame):
    transferred, expelled_six = names()
    new_frame = dict()
    for key, value in frame.items():
        if key not in new_frame and key not in transferred and len(value) > 1:
            new_frame[key] = list()
        if key not in transferred and len(value) > 1:
            analyzed_value = value[:-1] # extract last term
            count_extra_terms = Counter([elem[0] for elem in analyzed_value])
            extra_terms_quantity = sum(count_extra_terms.values()) - len(count_extra_terms)
            pretest_retakes_quantities = [elem[1] for elem in analyzed_value]
            mean_pretest_retake = sum(pretest_retakes_quantities) / len([pretest_retakes_quantities])
            exam_retakes_quantities = [elem[2] for elem in analyzed_value]
            mean_exam_retake = sum(exam_retakes_quantities) / len(exam_retakes_quantities)
            average_points = [elem[3] for elem in analyzed_value]
            mean_average_point = sum(average_points) / len(average_points)
            label = 0
            if key in expelled_six or value[-1][0] != 6:
                label = 1
            new_frame[key] = [round(mean_pretest_retake, 2), 
                              round(mean_exam_retake, 2),
                              round(mean_average_point, 2), 
                              extra_terms_quantity, 
                              label]
    return new_frame


if __name__ == '__main__':
    groups = ['Б14-503', 'Б14-504', 'Б15-502', 'Б16-503', 'Б16-513']
    j1 = merge_preliminary_data(groups)
    j2 = correct_dataset(j1)
    print(j2)