# -*- coding: UTF-8 -*-


class Mins_array:
    def __init__(self, num=20):
        self.__HTtime_tmp = datetime.datetime.strptime('00:00:00.00', "%H:%M:%S.%f")
        self.__array = []
        self.num = num

    def addData(self, time, data):
        if self.__HTtime_tmp.hour == time.hour and self.__HTtime_tmp.minute == time.minute:
            self.__array[-1] = data
        else:
            if len(self.__array) < self.num:
                self.__array += [data]
            else:
                self.__array = self.__array[1:] + [data]
        self.__HTtime_tmp = time
        return self.__array

    def getMa(self, numMa):
        if (numMa > self.num):
            print("Error from MA")
            return False
        else:
            return sum(self.__array[-numMa:]) * 1. / min(len(self.__array), numMa)

class OHLC_minsArray:
    def __init__(self, num=20):
        self.__HTtime_tmp = datetime.datetime.strptime('00:00:00.00', "%H:%M:%S.%f")
        self.__HTtime_tmp2 = datetime.datetime.strptime('00:00:00.00', "%H:%M:%S.%f")
        self.num = num
        self.O = []
        self.H = []
        self.L = []
        self.C = []
        self.point = 0
        self.H_tmp = -999999
        self.L_tmp = 999999
        self.Ktmp, self.Dtmp = 50., 50.
        self.K, self.D = 50., 50.

    def addData(self, time, data):
        if self.__HTtime_tmp.hour == time.hour and self.__HTtime_tmp.minute == time.minute:
            if (self.H_tmp < 0):
                self.C += [data]
                self.H_tmp = max(self.H_tmp, data)
                self.L_tmp = min(self.L_tmp, data)
                self.H += [self.H_tmp]
                self.L += [self.L_tmp]
                #if (len(self.C) > 1):
                #    print('MMM', time.minute, time.second, self.O[-2], self.H[-2], self.L[-2], self.C[-2])
            else:
                self.C[self.point - 1] = data
                self.H_tmp = max(self.H_tmp, data)
                self.L_tmp = min(self.L_tmp, data)
                self.H[self.point - 1] = self.H_tmp
                self.L[self.point - 1] = self.L_tmp
            return time.minute, time.second, self.O[-1], self.H[-1], self.L[-1], self.C[-1]
        else:
            if len(self.O) == len(self.C):  # 避免那區間內只有一筆資料
                if len(self.O) < self.num:
                    self.O += [data]
                else:
                    self.O = self.O[1:] + [data]
                    del self.C[0], self.H[0], self.L[0]
                self.H_tmp = -999999
                self.L_tmp = 999999
                self.point = len(self.O)
            self.__HTtime_tmp = time
            return time.minute, time.second, self.O[-1], self.O[-1], self.O[-1], self.O[-1]

    def getKD(self, time, numKD=9):
        if (numKD > self.num):
            print("Error from KD")
            return False
        else:
            if len(self.H) >= numKD:
                if max(self.H[-numKD:]) != min(self.L[-numKD:]):
                    if self.__HTtime_tmp2.hour != time.hour or self.__HTtime_tmp2.minute != time.minute:
                        self.Ktmp = self.K
                        self.Dtmp = self.D
                    RSV = (self.C[-min(numKD, len(self.C))] - min(self.L[-numKD:])) * 1. / \
                          (max(self.H[-numKD:]) - min(self.L[-numKD:])) * 100.
                    K = 2. / 3 * self.Ktmp + 1. / 3 * RSV
                    D = 2. / 3 * self.Dtmp + 1. / 3 * K
                self.__HTtime_tmp2 = time
                return RSV, K, D
