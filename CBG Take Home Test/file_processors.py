"""
These functions will read the files obtain the data necessary from them, and overwrite them
with the correct information.
"""
import csv
from difflib import SequenceMatcher


def process_contests_file():
    """
    This function reads the contests.csv file and rewrites it, getting rid of any duplicate records.
    To determine duplicates, it looks at the value in the "ContestFullName" column.  The function will
    save duplicate contest's ID as the keys in the contest_id_pairs dictionary, and the correct contest
    IDs in the dictionary's values.  It will return this information to be used in the process_choices_file
    method.
    """
    contest_list = []
    contest_id_pairs = {}

    try:
        with open("contests.csv", "r") as contests_file:
            reader = csv.reader(contests_file)
            for row in reader:
                if len(contest_list) == 0:
                    contest_list.append(row)
                else:
                    is_duplicate = False
                    for i in range(len(contest_list)):

                        # Determines if there is a duplicate contest by comparing ContestFullNames
                        if row[3] == contest_list[i][3]:

                            # enters duplicate and corresponding correct contest id as key : value pair
                            contest_id_pairs[row[0]] = contest_list[i][0]
                            is_duplicate = True

                    if not is_duplicate:
                        contest_list.append(row)
    except IOError:
        print("Error reading file.")

    try:
        with open("contests.csv", "w", encoding="UTF-8", newline="") as contests_file:
            writer = csv.writer(contests_file)
            writer.writerows(contest_list)
    except IOError:
        print("Error writing to file.")
    return contest_id_pairs


def process_choices_file(id_pairs):
    """
    This function reads the choices.csv file and overwrites it, taking out the records that have
    the duplicate contest ID(s).  In the process of removing incorrect records, it also obtains the
    necessary information to fix the records in the ballotmapper.csv file that include the illegal
    contest and choice IDs.
    """

    choices_list = []
    corrected_info = []

    try:
        with open("choices.csv", "r") as choices_file:
            reader = csv.reader(choices_file)
            for row in reader:
                if len(choices_list) == 0:
                    choices_list.append(row)
                else:
                    # if row has a duplicate contest ID
                    if row[1] in id_pairs:
                        for i in choices_list:

                            # If the record in choices_list has the correct ID that is the value pair of the current file's row's duplicate,
                            # and the similarity in their ContestAndChoiceName column is greater than 98%, do not include that row in choices_list.
                            # Instead, get the necessary information from it to correct any record in ballotmapper.csv that includes the incorrect
                            # Choice ID.
                            if i[1] == id_pairs[row[1]] and SequenceMatcher(None, row[3], i[3]).ratio() > 0.98:
                                incorrect_choice = row[0]
                                correct_choice = i[0]
                                correct_contest = i[1]
                                corrected_info.append(
                                    [incorrect_choice, correct_choice, correct_contest])
                    else:
                        choices_list.append(row)
    except IOError:
        print("Error reading file.")

    try:
        with open("choices.csv", "w", encoding="UTF-8", newline="") as choices_file:
            writer = csv.writer(choices_file)
            writer.writerows(choices_list)

    except IOError:
        print("Error writing to file.")
    return corrected_info


def process_ballotmapper_file(new_info):
    """
    This function will read the ballotmapper.csv file, and if any records with illegal Choice IDs are found,
    will fix them with the correct information: the correct choice ID and contest ID.
    """

    ballotmapper_list = []
    record_counter = 0
    try:
        with open("ballotmapper.csv", "r") as ballotmapper_file:
            reader = csv.reader(ballotmapper_file)
            for row in reader:
                for i in new_info:

                    # Added these to clarify what the indexes I am using represent
                    illegal_choice_id = i[0]
                    legal_choice_id = i[1]
                    legal_contest_id = i[2]

                    if row[5] == illegal_choice_id:
                        row[5] = legal_choice_id
                        row[4] = legal_contest_id
                        record_counter += 1

                ballotmapper_list.append(row)
    except IOError:
        print("Error reading file.")

    try:
        with open("ballotmapper.csv", "w", encoding="UTF-8", newline="") as ballotmapper_file:
            writer = csv.writer(ballotmapper_file)
            writer.writerows(ballotmapper_list)
            print(str(record_counter) +
                  " record(s) were fixed in the 'ballotmapper.csv' file.")

    except IOError:
        print("Error writing to file.")
