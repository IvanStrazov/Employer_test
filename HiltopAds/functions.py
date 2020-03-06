# Python 3.7
# utf-8
# 04.03.2020



import pandas as pd
from classes import Pair, Feed
from zipfile import ZipFile



def load_logs():
    with ZipFile('test.zip') as z:
        logs = z.read('requests.csv').decode('utf8')
        logs = map(lambda x: x.split(';', 4), logs.replace('"', '').split('\n'))
        
    return logs



def pair_konv(logs):
    '''
    Сопоставление пар IP-UserAgent и агрегация логов по ним. Создание сэта уникальных фидов.
    '''
    pair_dict = {}
    feed_set = set()

    for log in logs:
        if len(log) < 5:
            continue
            
        key = tuple(log[3:5])
        if key not in pair_dict.keys():
            pair_dict[key] = Pair(log[2])
        else:
            pair_dict[key].feed_dict_add(log[2])

        feed_set.add(log[2])
        
    return pair_dict, feed_set



def feed_konv(pair_dict, feed_set):
    '''
    Сопоставление фидов с агрегированными данными и расчёт статистик.
    '''
    feed_dict = dict()
    for feed in feed_set:
        feed_dict[feed] = Feed()
        
    for pair in pair_dict.keys():
        for feed in pair_dict[pair].feed_dict.keys():
            feed_dict[feed].pair_add(pair_dict[pair].feed_dict[feed])
            
    for feed in feed_dict.keys():
        feed_dict[feed] = feed_dict[feed].complete_stat()
        
    feed_dict = pd.DataFrame.from_dict(feed_dict, orient='index', columns=['Total', 'Uniq', 'Resell', 'UniquenessMean', 'UniquenessMedian', 'UniquenessPerc90'])    
    
    return feed_dict



def stat_merge_and_save(logs):
    '''
    Загрузка дневной статы по фидам и связка с информацией из логов. Представление в нужном формате и сохранение в файл.
    '''
    with ZipFile('test.zip') as z:
        stat = pd.read_csv(z.open('stat_rps.tsv'), sep='\t')
    stat.rename(columns={'feed':'Feed', 'requests': 'Requests', 'rps': 'MaxRPS'}, inplace=True)
    stat = stat.merge(logs, how='outer', left_on='Feed', right_index=True).fillna(0)
    stat = stat[['Feed', 'Total', 'Uniq', 'MaxRPS', 'Requests', 'Resell', 'UniquenessMean', 'UniquenessMedian', 'UniquenessPerc90']]
    stat.sort_values('Total', ascending=False, inplace=True)
    stat.to_csv('report.tsv', sep='\t', index=False)