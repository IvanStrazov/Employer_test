# Python 3.7
# utf-8
# 04.03.2020



import numpy as np



class Pair():
    '''
    Класс, представляющий уникальную пару IP-UserAgent.
    По ней извлекает из логов информацию и заносит её агрегацию в словарь фидов объекта.
    '''
    def __init__(self, feed):
        '''
        Инициализация:
            feed_dict (dct) - Сопоставление фидов со списком [Uniqueness, Resell, Total];
            temp (int) - Накопленное число вызова данной пары IP-UserAgent;
            start_feed (str) - Изначальный фид.
        '''
        self.feed_dict = {feed: [1, 0, 1]}
        self.temp = 1
        self.start_feed = feed
        
    def feed_dict_add(self, feed):
        '''
        Обработка нового лога, соответствующего данной паре IP-UserAgent.
        '''
        self.temp += 1
        
        if feed in self.feed_dict.keys():
            if feed == self.start_feed:
                self.feed_dict[feed][0] = self.temp
            else:
                self.feed_dict[feed][:2] = [self.temp, 1]
            self.feed_dict[feed][2] += 1
        else:
            self.feed_dict[feed] = [self.temp, 1, 1]
            

            
class Feed():
    '''
    Класс, представляющий уникальный фид. 
    Из агрегированной по парам IP-UserAgent информации отбирает по принадлежности к фиду и рассчитывает необходимые статистики.
    '''
    def __init__(self):
        '''
        Инициализация:
            Total (int) - суммарное число запросов в логе по фиду;
            Uniq (int) - число уникальных пар по фиду;
            uniqueness_list (list) - список всех Uniqueness из пар по фиду;
            resell_list (list) - список всех Resell из пар по фиду.
        '''
        self.Total = 0
        self.Uniq = 0
        self.uniqueness_list = list()
        self.resell_list = list()
        
    def pair_add(self, pair):
        '''
        Заполнение инициализированных параметров при проходе по парам.
        '''
        self.Uniq += 1
        self.Total += pair[2]
        self.uniqueness_list.append(pair[0])
        self.resell_list.append(pair[1])
        
    def complete_stat(self):
        '''
        Расчёт статистик.
        Для удобства использован numpy
        '''
        self.uniqueness_list = np.array(self.uniqueness_list)
        
        return [self.Total,
                self.Uniq,
                sum(self.resell_list) / len(self.resell_list), # Resell
                np.mean(self.uniqueness_list), # UniquenessMean
                np.median(self.uniqueness_list), # UniquenessMedian
                np.quantile(self.uniqueness_list, 0.9) # UniquenessPerc90
               ]