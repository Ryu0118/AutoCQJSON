import json
import sys
from question import Question


def main():
    file_name = sys.argv[1:]
    if file_name != [] and len(file_name) == 1:
        with open(file_name[0], 'r', encoding='utf-8') as file:
            questions = parse(file)
            dic = convert_to_dictionary(questions)
            dump_to_json(dic, file_name[0])
    else:
        raise Exception("you must have one argument")


def dump_to_json(dict, filename):
    json_file_name = filename.split('.')[0]
    with open(json_file_name + '.json', 'w', encoding='utf-8') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)


def convert_to_dictionary(questions) -> dict:
    dic = {}
    category_dic = {}
    subcategory_dic = {}

    prev_difficulty = ""
    prev_category = ""

    for i, question in enumerate(questions):
        subcategory_dic[question.subcategory] = question.questions
        if i == 0:
            category_dic[question.category] = [subcategory_dic]
            dic[question.difficulty] = [category_dic]
        else:
            if question.difficulty != prev_difficulty:
                category_dic = {}
                category_dic[question.category] = [subcategory_dic]
                dic[question.difficulty] = [category_dic]
            elif question.category != prev_category:
                category_dic = {}
                category_dic[question.category] = [subcategory_dic]
                dic[question.difficulty].append(category_dic)
            else:
                category_dic[question.category].append(subcategory_dic)
                dic[question.difficulty] = [category_dic]

        prev_category = question.category
        prev_difficulty = question.difficulty
        subcategory_dic = {}

    return dic


def parse(file) -> list:

    question_objects = []
    current_meta_dic = {}
    questions = []
    question = {}

    for i, line in enumerate(file):
        # blank
        if line == '\n':
            continue
        # classify
        if 'difficulty:' in line and 'category:' in line and 'subcategory:' in line:
            if i != 0:
                obj = Question(questions, **current_meta_dic)
                question_objects.append(obj)
                questions = []

            metadata = line.split(',')

            for element in metadata:
                tmp = element.split(':')
                current_meta_dic[tmp[0]] = tmp[1].strip()
        # question
        else:
            tmp = line.split(':')

            if 'options:' in line:
                options = list(map(str.strip, tmp[1].split(',')))
                tmp[1] = options

            elif 'answer:' in line:
                tmp[1] = int(tmp[1].strip())

            elif 'question:' or 'explanation' in line:
                tmp[1] = tmp[1].strip()

            question[tmp[0]] = tmp[1]

            if len(question) == 4:
                questions.append(question)
                question = {}

    obj = Question(questions, **current_meta_dic)
    question_objects.append(obj)
    questions = []

    return question_objects


if __name__ == '__main__':
    main()
