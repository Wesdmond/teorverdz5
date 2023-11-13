from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import math
import pandas as pd

sns.set()
sns.set_style("whitegrid", {'grid.linestyle': '--'})

def getInputData():
    file = open('input.txt')
    data = file.read().split(' ')
    print("Исходные данные:")
    [print(i, end = ' ') for i in data]
    for i in range(len(data)):
        data[i] = float(data[i])
    return data
    
def variationSeries(data):
    data.sort()
    print("\n\nВариационный ряд:")
    [print(i, end = ' ') for i in data]
    return data

def getExtemum(data):
    print("\n\nMin value = %0.2f\nMax value = %0.2f" %(data[0], data[-1]))

def getScope(data):
    print("Размах выборки = %0.2f" %((data[-1] - data[0])))
    
def getM(data):
    p = []
    for i in range(len(set(data))):
        p.append(data.count(sorted(set(data))[i]) / len(data))
    M = sum([p[i] * sorted(set(data))[i] for i in range(len(set(data)))])
    print("\nОценка математического ожидания = %0.3f" % (M))
    return p, M

def getD(data, p, meanX):
    sqX = [(i - meanX)**2 for i in data]
    D = sum([sqX[i] * p[i] for i in range(len(data))])
    print("Оценка дисперсии = %0.2f" % (D))
    print("Оценка среднеквадратического отклонения = %0.2f" % (D**0.5))
    
def empiricFunction(data, p):
    print("\nЭмпирическая функция:")
    
    for i in range(len(data)):
        if (i == 0):
            print("x <= %0.2f -> 0" % (data[i]))
        else:
            first = data[i - 1]
            second = data[i]
            print("%0.2f < x <= %0.2f -> %0.2f" % (first, second, sum(p[0:data.index(second)])))
    print("x > %0.2f -> 1" % (data[-1]))
    
def getPlotEmpiric(data, p):
    def F(x):
        li = list(filter(lambda num: num <= x, data))
        if (len(li) == 0):
            return 0
        return round(sum(p[0:data.index(li[-1]) + 1]), 2)
    
    y = np.vectorize(F)
    __, ax = plt.subplots()
    for i in range(len(data)):
        if (i == 0):
            x = np.linspace(data[0] - 0.5, data[0], 10)
            ax.plot(x, y(x), color='red')
        else:
            x = np.linspace(data[i-1], data[i] - 0.000001, 10)
            ax.plot(x, y(x), color = 'red')
    x = np.linspace(data[-1], data[-1] + 0.5, 10)
    ax.plot(x, y(x), color = 'red')
    plt.title("График эмпирической функции")
    plt.show()
    
def getH(data, dataLen):
    return (data[-1] - data[0]) / (round(1 + math.log(dataLen, 2), 1))    
    
def getHistogramm(data, h):
    histogramm = []
    start = data[0] - h / 2
    while (start < data[-1]):
        counter = 0
        for val in data:
            if (val >= start and val < (start + h)):
                counter +=1 
        p = counter / (len(data) * h)
        histogramm.append((f"{round(start, 2)} {round(start+h, 2)}", round(p, 3)))
        start += h
    
    x, y = zip(*histogramm)
    
    __, ax = plt.subplots()
    ax.bar(x, y)
    plt.title('Гистограмма приведенных частот')
    plt.show()

def getPolygon(data, h):
    x, y = [], []
    start = data[0] - h / 2
    while (start < data[-1]):
        counter = 0
        for val in data:
            if (val >= start and val < (start + h)):
                counter += 1
        x.append((start + h) / 2)
        y.append(counter)
        start += h
            
    plt.plot(x, y)
    plt.title("Полигон приведенных частот")
    plt.show()


def main():
    data = variationSeries(getInputData())
    dataLen = len(data)
    
    getExtemum(data)
    
    getScope(data)
    
    p, M = getM(data)
    
    data = sorted(set(data))
    
    getD(data, p, M)
        
    empiricFunction(data, p)
    
    getPlotEmpiric(data, p)
    
    h = getH(data, dataLen)
    
    getHistogramm(data, h)
    
    getPolygon(data, h)
    
main()
