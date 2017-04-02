"""
Created on Mar 1, 2017

@author: yytang
"""
import os
import rpy2.robjects as robjects


class RPlot(object):
    """
    classdocs
    """

    # Rsrc_dir = "/home/ami/yutang/workspace/DataReduction/R"
    # defaultPath = "/home/ami/yutang/Documents/week5"
    defaultDir = "~/Documents/apps"

    def initR(self):
        curDir = os.getcwd()
        robjects.r.source("vern.R")
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

    def line(self, data_list):

        """Calculate xlim and ylim """
        flatten_data_list_x = sum([item[0] for item in data_list], [])
        flatten_data_list_y = sum([item[1] for item in data_list], [])
        xlim = [min(flatten_data_list_x), max(flatten_data_list_x)]
        ylim = [min(flatten_data_list_y), max(flatten_data_list_y)]
        print(xlim, ylim)

        for data in data_list:
            x = data[0]
            y = data[1]
            robjects.r.plot(x, y, xlim=tuple(xlim), ylim=tuple(ylim))


if __name__ == '__main__':
    rPlot = RPlot('tt1')
    x = [i for i in range(1, 7)]
    y = [i*i for i in x]
    y1 = [i*i*i for i in x]
    rPlot.line([[x, y], [x, y1]])
    input("hehe")