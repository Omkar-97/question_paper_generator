import random
import os
from itertools import combinations
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
question_list = []


def create_qp(question_cnt):
    """
    create_qp() generates the question paper randomly based on difficulty level and marks
    :return: None
    """
    difficulty_level = ['easy', 'medium', 'hard']
    with open('qp1.txt', 'w+') as fp:
        try:
            for i in range(1, question_cnt+1):
                df_temp = random.choice(difficulty_level)
                if df_temp == "easy":
                    fp.write("Q{},{},{}\n".format(i, df_temp, random.randint(1, 5)))
                if df_temp == "medium":
                    fp.write("Q{},{},{}\n".format(i, df_temp, random.randint(5, 10)))
                if df_temp == "hard":
                    fp.write("Q{},{},{}\n".format(i, df_temp, random.randint(10, 20)))
        except IOError as e:
            print(e)
        else:
            fp.close()


def sum_marks(marks_list, marks):
    """
    :param marks_list: List of marks based on difficulty level
    :param marks: Total difficulty marks
    :return: Combination of marks to match the final marks.
    """
    temp = []
    if len(marks_list) > 0:
        for rep in range(1, len(marks_list)+1):
            for i in range(0, len(marks_list)+1):
                temp += list(combinations(marks_list, rep))
            for item in temp:
                if sum(item) == marks:
                    return item


def marks_distribution():
    """
    marks_distribution() function generated the total marks
    :return: total (easy, medium, hard)
    """
    print("Enter total marks:", end=" ")
    total_marks = int(input())
    print("Split marks in percentage(%)")
    print("Easy:", end=" ")
    easy = int(input())
    print("Medium:", end=" ")
    medium = int(input())
    print("Hard:", end=" ")
    hard = int(input())

    easy_per = easy * total_marks // 100
    medium_per = medium * total_marks // 100
    hard_per = hard * total_marks // 100

    return easy_per, medium_per, hard_per


def get_question(ret_list, diff_val):
    """
    function get_question() generates the final question set
    :param ret_list: tuple consisting of combination of items to match final marks
    :param diff_val: difficulty value to search in JSON
    :return: None
    """
    marks = list(ret_list)
    try:
        for key, value in qp.items():
            for val in marks:
                if val in value:
                    if diff_val in value:
                        if key not in question_list:
                            question_list.append((key, val, diff_val))
                            marks.remove(val)
    except:
        pass


def qp_gen(qp, easy, medium, hard):
    """
    function qp_gen() generates the questions based on difficulty level and marks
    :param qp: question paper read
    :param easy: Total easy marks
    :param medium: Total medium marks
    :param hard: Total hard marks
    :return: List of questions.
    """
    easy_list = []
    medium_list = []
    hard_list = []

    for k, v in qp.items():
        diff_lvl, marks = v

        if diff_lvl == "easy":
            easy_list.append(marks)

        if diff_lvl == "medium":
            medium_list.append(marks)

        if diff_lvl == "hard":
            hard_list.append(marks)

    ret_list = sum_marks(easy_list, easy)
    if ret_list is not None:
        print("\nEasy questions marks: ", list(ret_list))
        get_question(ret_list, "easy")

    ret_list = sum_marks(medium_list, medium)
    if ret_list is not None:
        print("Medium questions marks: ", list(ret_list))
        get_question(ret_list, "medium")

    ret_list = sum_marks(hard_list, hard)
    if ret_list is not None:
        print("Hard questions marks: ", list(ret_list))
        get_question(ret_list, "hard")

    return question_list


def read_file():
    """
    read_file() function selects the file to read the list of questions.
    :return: json format of the text read from the file.
    """
    qp_dict = dict()
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=[("Text Files", "*.txt")])
    try:
        with open(file_path, 'r') as fp:
            qp_fp = fp.read()
        qp_temp = qp_fp.split("\n")
        for line in qp_temp:
            if line:
                temp_1 = line.split(",")
                qp_dict.update({temp_1[0]: (temp_1[1], int(temp_1[2]))})

        return qp_dict

    except IOError as e:
        print(e)


if __name__ == '__main__':

    print("\nQuestion Paper Generator\n")
    print("Enter number of questions to generate in database:", end=" ")
    question_cnt = int(input())
    create_qp(question_cnt)
    easy, medium, hard = marks_distribution()
    print("\nSelect the question paper")
    qp = read_file()
    if qp:
        final_qp = qp_gen(qp, easy, medium, hard)
        print("\nFinal question list")
        with open("final_qp.txt", 'w+') as fp:
            fp.write("Question\tMarks\tDifficulty\n")
            for questions in final_qp:
                print(questions)
                fp.write("{}\t\t\t{}\t\t{}\n".format(questions[0], questions[1], questions[2]))
            fp.close()
