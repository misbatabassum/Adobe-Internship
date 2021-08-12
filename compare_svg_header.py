import os
import sys  # argument, this means we cannot really run this from Sublime


# returning first line of svg file
def read_first_line(file_path):
    with open(file_path, 'r') as file:
        blob = file.read()
    first_line = blob.splitlines()[0]
    return first_line

# checking if 'xlink' exists in file. if true, then need to use ideal header extra otherwise use ideal header
def check_xlink(file_path):
    bool_var = False
    with open(file_path, 'r') as file:
        for line in file:
            if 'xlink' in line:
                bool_var = True
                break
    return bool_var


def main():
    # list_of_files_needing_changes = open("needsChanges.txt").readlines()

    ideal_header = '<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">'
    ideal_header_extra = '<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg" ' \
                         'xmlns:xlink="http://www.w3.org/1999/xlink"> '
    input_folder = sys.argv[-1]

    for file_name in os.listdir(input_folder):
        if os.path.splitext(file_name)[-1] == '.svg':  # grab all files ending with .svg
            file_path = os.path.join(input_folder, file_name) 
            header = read_first_line(file_path)
            xlink_exists = check_xlink(file_path)

            if header == ideal_header or header == ideal_header_extra:
                # print('header is ok')
                continue
            else:
                file = open(file_path, 'r')
                list_of_lines = file.readlines()

                if xlink_exists:  # xlink line exists - using header with extra parameter
                    list_of_lines[0] = ideal_header_extra + "\n"
                else: 
                    file = open(file_path, 'r')
                    list_of_lines = file.readlines()
                    list_of_lines[0] = ideal_header + "\n"

                file = open(file_path, 'w')
                file.writelines(list_of_lines)
                file.close()


if __name__ == '__main__':
    main()
