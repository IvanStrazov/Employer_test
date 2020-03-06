# Python 3.7
# utf-8
# 04.03.2020



from functions import *

if __name__ == '__main__':
    logs = load_logs()
    logs = feed_konv(*pair_konv(logs))
    stat_merge_and_save(logs)