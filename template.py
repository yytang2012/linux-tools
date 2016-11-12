#!/usr/bin/env python3
# coding=utf-8

"""Upload the contents of your Downloads folder to Dropbox.

This is an example app for API v2.
"""
import math


def func(list_sum, threshold):
    min_delta = 0.1
    if math.fabs(list_sum - threshold) < min_delta:
        return 0
    if list_sum - threshold <= 0:
        return -1
    else:
        return 1


def binary_search(m_list, low=0, high=0):
    high = (high if high != 0 else len(m_list) - 1)
    print(high)
    threshold = 1.8
    list_sum = 0
    while low <= high:
        list_sum = sum(m_list[low:high+1]) / (high - low + 1)
        print("low = {0}, high = {1}, list_sum = {2}".format(low, high, list_sum))
        cond = func(list_sum, threshold)
        if cond == 0:
            print("find it, threshold = {0}".format(list_sum))
            break
        elif cond < 0:
            low = math.floor((low + high) / 2) + 1
        else:
            high = math.ceil((low + high) / 2) - 1

    print("low = {0}, high = {1}, list_sum = {2}".format(low, high, list_sum))

def combine_items(items):
    item_list = [int(i) for i in items.split(',')]
    print(item_list)
    desc = []
    start = 0
    item_list.append(0)
    for i in range(1, len(item_list)):
        if item_list[i-1] + 1 != item_list[i]:
            desc.append((item_list[start], item_list[i-1]))
            start = i

    def print_list(s, t, d=5):
        if t - s < 5:
            out_str = '{0}'.format(s)
            for i in range(s+1, t+1):
                out_str += ', {0}'.format(i)
        else:
            out_str = '{0}-{1}'.format(s, t)
        return out_str

    item_str = print_list(desc[0][0], desc[0][1])
    for ii in desc[1:]:
        item_str += ', ' + print_list(ii[0], ii[1])
    print(item_str)
    return item_str


def main():
    m_list = [i for i in range(0, 8)]
    print(m_list)
    # binary_search(m_list)

    items = '1,2,3,4,5,6, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 26'
    combine_items(items)


if __name__ == '__main__':
    main()
