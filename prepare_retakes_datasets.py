import os
import json
from prepare_avg_marks_datasets import fulfill_frame

def merge_retakes(groups):
    frame = dict()
    for group in groups:
        for i in range(6):
            check_file = os.path.exists(f'jsons/Grades_json{group}_{i+1}.json')
            if check_file:
                file = open(f'jsons/Grades_json{group}_{i+1}.json')
                j = json.load(file)
                for key, value in j.items():
                    retakes_quantity = len(value['pretest_retake']) + len(value['exam_retake']) +\
                            len(value['CP_retake']) + len(value['other_retake'])
                    if key not in frame:
                        frame[key] = list()
                    if len(frame[key]) > 0 and frame[key][-1][0] == i + 1:
                        frame[key][-1] = (i + 1, retakes_quantity)
                    else:
                        frame[key].append((i + 1, retakes_quantity))
    return frame