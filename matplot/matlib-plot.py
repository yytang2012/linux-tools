#!/usr/bin/env python
# coding=utf-8

"""
Author: yytang
Date: 2017-03-29
"""
import matplotlib.pyplot as plt


class MatlibPlot(object):
    def __init__(self):
        print("MatlibPlot init")
        self.colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']

    def test(self):
        x = [i for i in range(1, 10)]
        y = [i * i for i in x]
        y1 = [i * i * i for i in x]
        plt.plot(x, y, 'ro')
        plt.plot(x, y)
        plt.plot(x, y1, 'bs')
        plt.axis([0, max(x), 0, max(y1)])
        plt.ylabel("y axis")
        plt.show()

    def test1(self):
        lines = []
        x = [i for i in range(1, 10)]
        y = [i * i for i in x]
        y1 = [i * i * i for i in x]
        fig = plt.figure()
        line, = plt.plot(y, label='line 1')
        # use keyword args
        plt.setp(line, color='red', linewidth=2.0)
        lines.append(line)
        line, = plt.plot(y1, label='line 2')
        # use keyword args
        plt.setp(line, color='blue', linewidth=2.0)
        lines.append(line)
        plt.legend(handles=lines)
        plt.xlabel(None)
        axes = plt.gca()
        axes.set_xlim([float(i)/2 for i in range(0, 20)])
        plt.show()
        fig.savefig('/home/yytang/Documents/apps/test.png')

    def lines(self, coords_list, legend=None, xlab=None, ylab=None, title='', axis=None):
        lines = []
        if legend is None:
            legend = ['line{0}'.format(i) for i in range(1, len(coords_list) + 1)]
        for ii, coords in enumerate(coords_list):
            if len(coords) == 2:
                x, y = coords
            else:
                y = coords
                x = [i for i in range(1, len(y) + 1)]
            plt.plot(x, y, 'o', color=self.colors[ii])
            line, = plt.plot(x, y, label=legend[ii])
            # use keyword args
            plt.setp(line, color=self.colors[ii], linewidth=1.0)
            lines.append(line)
            plt.xlabel(xlab)
            plt.ylabel(ylab)
        # plt.legend(handles=lines, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # plt.legend(handles=lines, bbox_to_anchor=(0., 1.005, 1., .101), loc=3,
        #    ncol=4, mode="expand", borderaxespad=0.)
        plt.title(title)
        plt.show()


def plot_data(dataset):
    m_plot = MatlibPlot()
    plot_candidates = [i for i in range(0, 15)] + [50]
    x_axis = []
    length = 0
    names = []
    for ii in plot_candidates:
        data = []
        delta = 1
        for dd, res_dict in enumerate(dataset):
            key = '{0}'.format(ii)
            y = [item[1] for item in res_dict[key]]
            length = len(y) if len(y) > length else length
            x = [i for i in range(delta + 1 + length - len(y), delta + length + 1)]
            x_axis = list(set(x).union(x_axis))
            data.append((x, y))
            if dd == 0:
                name = list(set([item[0] for item in res_dict[key] if item[0] is not None]))[0]
                names.append(name)
                print(name)
        # data.reverse()
        if ii != 50:
            title = '{0} :: {1:02d}'.format(names[ii], ii + 1)
            savedFileName = 'app{0:02d}-{1}'.format(ii + 1, names[ii])
        else:
            title = 'Total top 50 apps'
            savedFileName = 'top50-app'
        m_plot.lines(data, xlab='Date', ylab='Percentage')

if __name__ == "__main__":
    m_plot = MatlibPlot()
    m_plot.test1()
    # x = [i for i in range(1, 10)]
    # y = [i * i for i in x]
    # y1 = [i * i * i for i in x]
    # coords = [(x, y), y1]
    # m_plot.lines(coords)
    exit(0)
    import json

    with open('/home/yytang/Documents/apps/dataset.txt', 'r') as f:
        dataset_string = f.read()
        dataset = json.loads(dataset_string)
    # print_names(dataset)
    # summary_data(dataset)
    plot_data(dataset)
