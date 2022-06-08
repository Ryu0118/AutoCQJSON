import json
import sys
from question import Question


def main():
    file_name = sys.argv[1:]
    if file_name != [] and len(file_name) == 1:
        if not file_name[0].endswith('.txt'):
            terminate('File extension should be txt')

        with open(file_name[0], 'r', encoding='utf-8') as file:
            questions = parse(file)
            dic = convert_to_dictionary(questions)
            dump_to_json(dic, file_name[0])
    else:
        terminate('you must have one argument')


def dump_to_json(dict, filename):
    json_file_name = filename.split('.')[0]
    with open(json_file_name + '.json', 'w', encoding='utf-8') as file:
        json.dump(dict, file, indent=2, ensure_ascii=False)
        print('Successfully Processed!!')
        print(f'Please See "{json_file_name}.json"')


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
    question_count = 0
    is_defined_metadata = False

    for i, line in enumerate(file):
        # blank
        if line == '\n':
            if 0 < len(question) < 4:
                terminate(
                    f'{4 - len(question)} pieces of data are missing.')

            continue

        # meta data
        if 'difficulty:' in line and 'category:' in line and 'subcategory:' in line:
            is_defined_metadata = True

            if i != 0:
                obj = Question(questions, **current_meta_dic)
                question_objects.append(obj)
                questions = []

            metadata = line.split(',')

            # Error handling
            if len(metadata) != 3:
                terminate(
                    f'line {i + 1}: Metadata is missing.\ndefine "difficulty:", "category:" and "subcategory:"')

            for element in metadata:
                tmp = element.split(':')
                # Error handling
                if len(tmp) != 2:
                    terminate(
                        f'Wrong syntax at line {i + 1}\nline {i + 1}: {line}\nYou cannot use ":" ')

                current_meta_dic[tmp[0]] = tmp[1].strip()

        # question
        else:
            tmp = line.split(':')
            # Error handling
            if len(tmp) != 2:
                terminate(
                    f'Wrong syntax at line {i + 1}\nline {i + 1}: {line}\nYou cannot use ":" ')

            if not is_defined_metadata:
                terminate(
                    f'The metadata of question is not defined.\ndefine "difficulty:", "category:" and "subcategory:" on line {i - 1}')

            # rendering of each token
            if 'options:' in line:
                options = list(map(str.strip, tmp[1].split(',')))
                tmp[1] = options

            elif 'answer:' in line:
                tmp[1] = int(tmp[1].strip())

            elif 'question:' in line or 'explanation:' in line:
                tmp[1] = tmp[1].strip()

            else:
                terminate(
                    f'line {i + 1}: Undefined token "{tmp[0]}"')

            question[tmp[0]] = tmp[1]

            if len(question) == 4:
                questions.append(question)
                question_count += 1
                question = {}

    obj = Question(questions, **current_meta_dic)
    question_objects.append(obj)
    questions = []
    print(f'question count -> {question_count}')

    return question_objects


def terminate(message):
    print(message)
    sys.exit()


if __name__ == '__main__':
    main()
