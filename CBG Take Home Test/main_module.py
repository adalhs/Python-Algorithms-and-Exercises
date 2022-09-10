"""
TAKE HOME TEST
@author Adalberto Holguin
@email adalhs@yahoo.com

NOTE: This script should be able to handle an unlimited number of duplicate contest IDs and fix
all files accordingly.  However, as the files only included one duplicate contest ID, I could not
test this out.  I have added the unaltered, original files just in case, but feel free to add your
own copies.  Variations of the files with more than one duplicate contest ID, should also work as
long as the number of columns in the file do not change.  More columns can be added to the files
behind the ones already there, and the program should still work, but adding columns to the files in
front of, or between the ones already there will make the program not function properly.
"""
import file_processors

contest_ids = file_processors.process_contests_file()

if len(contest_ids) == 0:
    print("No duplicate contests were found in the 'contests.csv' file.")
else:
    for i in contest_ids:
        print("The duplicate contest ID " + i +
              " was removed from the 'contests.csv' file.")

correct_info = file_processors.process_choices_file(contest_ids)

for i in correct_info:
    print("The Choice ID " + i[0] + " included an illegal duplicate contest ID and "
          + "was removed from the 'choices.csv' file.")

file_processors.process_ballotmapper_file(correct_info)
