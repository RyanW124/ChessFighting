import os

def path(relative_path):
    my_prefix = ['/', 'Users', 'ryan.wong', 'Desktop', 'isb', 'grade 10', 'Game Design', 'Git', 'Game-Design', 'ChessFighting']

    entire_path = my_prefix + relative_path
    path = os.path.join(*entire_path)
    if os.path.isfile(path):
        return path
    else:
        path = os.path.join(*relative_path)
        if os.path.isfile(path):
            return path
    return None