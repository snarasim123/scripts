
def file_length(file_name):
    file = open(file_name)
    total_lines: int = len(file.readlines())
    file.close()
    return total_lines