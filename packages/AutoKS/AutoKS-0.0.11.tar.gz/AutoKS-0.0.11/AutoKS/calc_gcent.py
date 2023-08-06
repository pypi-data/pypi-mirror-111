#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def calc_gcent(Array):
    ncent_list = []
    gcent_list = []
    for array in range(0, Array.shape[0]):
        node = []
        word = []
        for row in range(0, Array[array].shape[0]):
            for column in range(0, Array[array].shape[1]):
                # [x[0] for x in node]，意为选取node的第一列的内容，放置在一个新列表中
                if not node or Array[array][row, column] not in [x[0] for x in node]:
                    node_deg = 0
                    for r in range(0, Array[array].shape[0]):
                        if Array[array][row, column] in Array[array][r]:
                            node_deg += 1
                    node.append([Array[array][row, column], node_deg])
                    word.append(Array[array][row, column])
        print('\n第', array, '个矩阵\nnode degree：', node)
        # ncent=node_degree/(nodeNum−1))
        ncent = []
        for i in range(0, len(node)):
            ncent.append([node[i][0], node[i][1] / (len(node) - 1)])
        print('ncent：', ncent)
        # gcent=Σ((MAXncent−ncent[i])/(nodeNum−2))
        gcent = 0
        max_ncent = max([x[1] for x in ncent])
        for i in range(0, len(node)):
            gcent += (max_ncent - ncent[i][1]) / (len(node) - 2)
        print('gcent：', float('%.4f' % gcent))
        gcent_list.append(float('%.4f' % gcent))
        ncent_list.append(ncent)
    print('\ngcent列表:', gcent_list)
    return np.array(ncent_list), np.array(gcent_list)
