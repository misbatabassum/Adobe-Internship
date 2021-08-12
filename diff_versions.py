# emoji list reader - outputs the difference between version 12.1 and version 13.1, keeps track of subgroups

def clean_up_line(line):
    '''
    just give me the part of the line before the hash mark
    '''
    if line.startswith('#'):
        return line
    else:
        return line.split('#')[0]


def main():
    header = '''\
    ############################################
    # NOTE: Do NOT put entries tagged as       #
    #       - 'minimally-qualified',           #
    #       - 'non-fully-qualified' or         #
    #       - 'unqualified'                    #
    #       in here, since they will be        #
    #       ignored by the processing scripts. #
    ############################################

    '''

    with open('emoji-test12.txt', 'r') as f:
        data_12_list = f.read().splitlines()
    with open('emoji-test13.txt', 'r') as f2:
        data_13 = f2.read()
        data_13_list = data_13.splitlines()

    data_12_clean = [clean_up_line(line) for line in data_12_list]

    f3 = open("changes.txt", "w")
    f3.write(header)
    sub_groups = {}
    sub_group = None

    # assign one to every single line of the file, store in dict
    for line_number, line in enumerate(data_13_list):
        sub_groups[line_number] = sub_group
        if line.startswith('# subgroup'):
            sub_group = line

    # keep track of the sub group headers we’ve already written
    sub_groups_written = []

    # the normal loop, in an enumerator which lets us keep track of line numbers
    for line_number, line in enumerate(data_13_list):
        if 'fully-qualified' in line:  # only output lines that are cleaned and fully qualified
            if not clean_up_line(line) in data_12_clean:
                sub_group = sub_groups[line_number]
                # if the subgroup header has not been written, write it first.
                if sub_group not in sub_groups_written:
                    f3.write("\n" + sub_group + "\n")
                    sub_groups_written.append(sub_group)
                # write the normal line with the codepoint we need
                f3.write(line + "\n")

    f3.close()


if __name__ == '__main__':
    main()
