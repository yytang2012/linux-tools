"""
Created on Mar 1, 2016

@author: yutang
"""
from collections import defaultdict

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import numpy as np
import os


class RPlot(object):
    """
    classdocs
    """

    # Rsrc_dir = "/home/ami/yutang/workspace/DataReduction/R"
    # defaultPath = "/home/ami/yutang/Documents/week5"
    defaultDir = "~/Documents/apps"

    def initR(self):
        curDir = os.getcwd()
        srcDir = os.path.join(curDir, 'R')
        robjects.r.source("%s/vern.R" % srcDir)
        # robjects.r.source("%s/zhichun.R" % Rsrc_dir)

    def quitR(self):
        robjects.r.q()

    def __init__(self, directory):
        """
        Constructor
        """
        rootDir = os.path.expanduser(self.defaultDir)
        if not os.path.isdir(rootDir):
            os.makedirs(rootDir)
        rootDir = os.path.join(rootDir, directory)
        if not os.path.isdir(rootDir):
            os.makedirs(rootDir)
        self.rootDir = rootDir
        self.initR()

    def plot(self, data, *args, title='Title', xlab='X axis', ylab='Y axis', names=None, save=True, savedFileName=None,
             showType='normal', plotType='line', cdfType='normal', x_axis=None, y_axis=None):
        if save:
            if savedFileName is None:
                savePath = os.path.join(self.rootDir, 'file.png')
            else:
                savePath = os.path.join(self.rootDir, savedFileName + '.png')
            gr_devices = importr('grDevices')
            gr_devices.png(file=savePath)

        rDataList = []
        rData = self.preliminary_processing(data, showType, cdfType)
        rDataList.append(rData)
        for i in range(0, len(args)):
            rData = self.preliminary_processing(args[i], showType, cdfType)
            rDataList.append(rData)

        if names is not None:
            rNames = robjects.StrVector(names)
        else:
            rNames = ""
        if plotType == 'bar':
            robjects.r.barplot(rData, main=title, xlab=xlab, ylab=ylab, **{"names.arg": rNames})
        else:
            if x_axis is not None:
                robjects.r.plot(rDataList[0], main=title, xlab=xlab, ylab=ylab, type='o', col=1, xaxt='n', yaxt='n')
                if type(x_axis) == float:
                    r_lab = robjects.FloatVector(x_axis)
                else:
                    r_lab = robjects.IntVector(x_axis)
                robjects.r.axis(1, lab=r_lab, **{"at": robjects.r.seq(0.5, 10, 0.5)})
            else:
                robjects.r.plot(rDataList[0], main=title, xlab=xlab, ylab=ylab, type='o', col=1)
            robjects.r.title(rNames)
            for i in range(0, len(rDataList)):
                rData = rDataList[i]
                print("**********")
                print(data)
                print("**********")
                robjects.r.lines(rData, type='o', col=i + 2)
        if save:
            gr_devices.dev_off()

    def line_plot(self, data_vector_list, title='Title', xlab='X axis', ylab='Y axis', save=True, savedFileName=None,
                  type='o', showType='normal', cdfType='normal', x_axis=None, y_axis=None):
        if save:
            if savedFileName is None:
                savePath = os.path.join(self.rootDir, 'file.png')
            else:
                savePath = os.path.join(self.rootDir, savedFileName + '.png')
            gr_devices = importr('grDevices')
            gr_devices.png(file=savePath)

        """ Firstly, we need process the first data vector"""
        item = data_vector_list[0]
        first_x_vector = item[0]
        first_y_vector = item[1]
        r_first_x_vector = self.preliminary_processing(first_x_vector)
        r_first_y_vector = self.preliminary_processing(first_y_vector, showType, cdfType)

        if x_axis is None and y_axis is None:
            robjects.r.plot(r_first_x_vector, r_first_y_vector, type=type, main=title, xlab=xlab, ylab=ylab, col=2)
        elif x_axis is not None and y_axis is None:
            robjects.r.plot(r_first_x_vector, r_first_y_vector, type=type, main=title, xlab=xlab, ylab=ylab, col=2,
                            xaxt='n', xlim=robjects.IntVector([x_axis[0], x_axis[-1]]))
            robjects.r.axis(1, at=x_axis)
        elif x_axis is None and y_axis is not None:
            robjects.r.plot(r_first_x_vector, r_first_y_vector, type=type, main=title, xlab=xlab, ylab=ylab, col=2,
                            yaxt='n', ylim=robjects.IntVector([y_axis[0], y_axis[-1]]))
            robjects.r.axis(2, at=y_axis)
        else:
            robjects.r.plot(r_first_x_vector, r_first_y_vector, type=type, main=title, xlab=xlab, ylab=ylab, col=2,
                            xaxt='n', yaxt='n', xlim=robjects.IntVector([x_axis[0], x_axis[-1]]),
                            ylim=robjects.IntVector([y_axis[0], y_axis[-1]]))
            robjects.r.axis(1, at=x_axis)
            robjects.r.axis(2, at=y_axis)

        for i in range(1, len(data_vector_list)):
            item = data_vector_list[i]
            r_x_vector = self.preliminary_processing(item[0])
            r_y_vector = self.preliminary_processing(item[1], showType, cdfType)
            robjects.r.lines(r_x_vector, r_y_vector, type=type, col=i + 2, xaxt='n', yaxt='n',
                             xlab='', ylab='')
        if save:
            gr_devices.dev_off()

    def box_plot(self, dataVec, main=None, xlab=None, ylab=None, names=None, save=False, savefile=None, cdf=True):
        if save:
            if savefile is None:
                savePath = os.path.join(self.defaultPath, 'file.png')
            else:
                savePath = os.path.join(self.defaultPath, savefile + '.png')
            grdevices = importr('grDevices')
            grdevices.png(file=savePath)
        rnames = robjects.StrVector(names)

        robjects.r.lcdf(robjects.IntVector(dataVec[0]), True)
        rdata0 = robjects.IntVector(dataVec[0])
        rdata1 = robjects.IntVector(dataVec[1])
        rdata2 = robjects.IntVector(dataVec[2])
        rdata3 = robjects.IntVector(dataVec[3])
        rdata4 = robjects.IntVector(dataVec[4])
        rdata5 = robjects.IntVector(dataVec[5])
        rdata6 = robjects.IntVector(dataVec[6])
        rdata7 = robjects.IntVector(dataVec[7])
        rdata8 = robjects.IntVector(dataVec[8])
        rdata9 = robjects.IntVector(dataVec[9])

        # =======================================================================
        # if (cdf == True):
        #     rdata0 = robjects.r.cdf(rdata0, **{"return.cdf":True})
        #     rdata1 = robjects.r.cdf(rdata1, **{"return.cdf":True})
        #     rdata2 = robjects.r.cdf(rdata2, **{"return.cdf":True})
        #     rdata3 = robjects.r.cdf(rdata3, **{"return.cdf":True})
        #     rdata4 = robjects.r.cdf(rdata4, **{"return.cdf":True})
        #     rdata5 = robjects.r.cdf(rdata5, **{"return.cdf":True})
        #     rdata6 = robjects.r.cdf(rdata6, **{"return.cdf":True})
        #     rdata7 = robjects.r.cdf(rdata7, **{"return.cdf":True})
        #     rdata8 = robjects.r.cdf(rdata8, **{"return.cdf":True})
        #     rdata9 = robjects.r.cdf(rdata9, **{"return.cdf":True})
        # =======================================================================

        robjects.r.box_plot(rdata0, rdata1, rdata2, rdata3, rdata4, rdata5, rdata6, rdata7, rdata8, rdata9,
                            main=main, xlab=xlab, ylab=ylab, names=rnames, las=2)
        if save:
            grdevices.dev_off()

    def preliminary_processing(self, data, showType='normal', cdfType='normal'):
        if type(data[0]) == int and showType == 'normal' and cdfType == 'normal':
            rData = robjects.IntVector(data)
        else:
            rData = robjects.FloatVector(data)
        if 'log' == showType:
            rData = robjects.r.log2(rData)
        # convert data to required output
        if 'lcdf' == cdfType:
            rData = robjects.r.lcdf(rData, **{"return.cdf": True})
        elif 'cdf' == cdfType:
            rData = robjects.r.cdf(rData, **{"return.cdf": True})
        else:
            pass
        return rData

    def summary(self, data):
        # check data type
        if type(data) is not list:
            print("Error happen, The data should be a list type")
            return
        if type(data[0]) is int:
            rData = robjects.IntVector(data)
        else:
            rData = robjects.FloatVector(data)
        rSummary = robjects.r.summary(rData)
        summary = list(rSummary)
        return summary


def summary_data(dataset):
    candidates = [i for i in range(0, 50)]
    for res_dict in dataset:
        print("------------------------------------------------------")
        for ii in candidates:
            key = '{0}'.format(ii)
            value = res_dict[key]
            array = np.array([item[1] for item in value])
            # print("{0:.2f}%".format(np.average(array) * 100))
            # print("{0:.2f}".format(np.std(array)))
            print("name: {0} -- mean : {1:.6f} -- std : {2:.6f}".format(value[0][0], np.average(array), np.std(array)))


def plot_data(dataset):
    plt = RPlot('top50apps')
    last_one = 150
    plot_candidates = [i for i in range(0, last_one)]
    x_axis = []
    length = 0
    names = []
    delta = 1
    for ii in plot_candidates:
        data = []
        for dd, res_dict in enumerate(dataset):
            key = '{0}'.format(ii)
            y = [item[1] for item in res_dict[key]]
            length = len(y) if len(y) > length else length
            x = [i for i in range(delta + 1 + length - len(y), delta + length + 1)]
            x_axis = list(set(x).union(x_axis))
            data.append((x, y))
            if dd == 0:
                app_names = list(set([item[0] for item in res_dict[key] if item[0] is not None]))
                name = app_names[0] if len(app_names) != 0 else "unKown"
                names.append(name)
                print(name)
        # data.reverse()
        title = '{0} :: {1:02d}'.format(names[ii], ii + 1)
        savedFileName = 'app{0:02d}-{1}'.format(ii + 1, names[ii])

        plt.line_plot(data, x_axis=x_axis, title=title, savedFileName=savedFileName, xlab='Date', ylab='Percentage')
        # for ii, name in enumerate(names):
        #     if ii < 15:
        #         print("|App{0}| {1}|".format(ii+1, name))
    """ Plot all apps """
    data = []
    for dd, res_dict in enumerate(dataset):
        y_dict = defaultdict(lambda: 0)
        total = len(plot_candidates)
        for ii in plot_candidates:
            key = '{0}'.format(ii)
            for jj, item in enumerate(res_dict[key]):
                y_dict[jj] += item[2]

        y = [y_dict[i] for i in range(0, len(y_dict))]
        x = [i for i in range(delta + 1 + length - len(y), delta + length + 1)]
        data.append((x, y))
        array = np.array(y)
        print("{0:.2f}%".format(np.average(array) * 100))
        print("{0:.2f}".format(np.std(array)))

    # data.reverse()
    title = 'Total top {0} apps'.format(total)
    savedFileName = 'top{0}-app'.format(total)
    plt.line_plot(data, x_axis=x_axis, title=title, savedFileName=savedFileName, xlab='Date', ylab='Percentage')



def print_names(dataset):
    for res_dict in dataset:
        for ii, item in enumerate(res_dict):
            key = "{0}".format(ii)
            name = set([temp[0] for temp in res_dict[key] if temp[0] is not None])
            print("ii:{0}, name:{1}".format(ii, name))


if __name__ == '__main__':
    plt = RPlot('test')
    x = [1, 2, 1, 5, 7, 3, 2, 4, 6]
    y = [11, 22, 33, 66, 55, 22, 44, 77, 88]
    x_axis = [i / 2 for i in range(1, 23)]
    y_axis = [i * 5 for i in range(1, 19)]
    x1 = [i + 2 for i in range(1, 10)]
    y1 = [i * 5 for i in range(1, 10)]
    # y_axis = None
    # x_axis = None
    print(x)
    print(y)
    print(x1)
    print(y1)
    names = ['aj']
    # plt.barPlot(a, names = names, save = True)
    # input("a")
    # plt.line_plot([(x, y),(x1, y1)], title="Car Milage Data", xlab="Number of Cylinders", ylab="Miles Per Gallon",
    #               x_axis=x_axis, y_axis=y_axis)
    #  y = [  2.20172550e-02,   5.25959994e-05,   5.40322627e-05,   3.25912685e-07,
    # 1.78416707e-07,   1.94993499e-02,   1.77399988e-02,   1.43384238e-02,
    # 0.00000000e+00,   1.62873366e-04,   5.78444944e-05,   7.30342348e-03,
    # 1.55062404e-05,   8.33606093e-06,   1.03701761e-05,   4.32144901e-04,
    # 1.53440716e-02,   5.47510030e-03,   0.00000000e+00,   1.49716386e-03,
    # 1.14971908e-03,   2.93063063e-04,   5.15696131e-04,   0.00000000e+00,
    # 0.00000000e+00,   0.00000000e+00,   9.28241438e-04]
    #  x = [i for i in range(1, len(y)+1)]
    #
    #  y1 = [  9.19836292e-06,   7.60629011e-03,   5.54888519e-02,   5.62506890e-02,
    # 5.39993201e-02,   7.88588794e-03,   7.38059711e-03,   1.43415659e-04,
    # 2.51932196e-05,   2.04974834e-05,   1.75353060e-02,   0.00000000e+00,
    # 0.00000000e+00,   1.39024522e-02,   4.79058450e-02,   1.17802254e-03,
    # 2.68859346e-04,   2.07253814e-03,   0.00000000e+00,   1.69135812e-02,
    # 1.34203508e-02,   1.29119192e-04,   0.00000000e+00,   2.76437210e-02,
    # 0.00000000e+00,   1.67189375e-02,   1.71487165e-02]
    #  x1 = [i for i in range(1, len(y1)+1)]
    #  args = [(x1, y1), (x, y)]
    import json

    with open('/home/yytang/Documents/apps/task6/dataset-apps-150.txt', 'r') as f:
    # with open('/home/yytang/Documents/apps/task5/task5-dataset-6.txt', 'r') as f:
        dataset_string = f.read()
        dataset = json.loads(dataset_string)
    # print_names(dataset)
    summary_data(dataset)
    # plot_data(dataset)
    # plt.line_plot(args, x_axis=x, title='App1', savedFileName='app01', xlab='Date', ylab='Percentage')
