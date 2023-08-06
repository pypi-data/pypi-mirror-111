#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import finditer
import sys
import networkx as nx
from .floyd import *


def text2graph(
        text,
        keyterms,
        read_from_file=True,
        encoding='utf-8',
        pfnet=False,
        max=None,
        min=None,
        r=np.inf
):
    """

    goals:
    - synonym replacement

    :param text:
    :param keyterms:
    :param read_from_file:
    :param encoding:
    :param pfnet:
    :param max:
    :param min:
    :param r:
    :return:
    """

    G = nx.Graph()

    if read_from_file:  # so the object 'text' is a filepath
        f = open(text, "r", encoding=encoding)
        text = f.readline()
        print(text)
    else:  # read_from_file = False, so the object 'text' is a string in Python
        G.name = 'text'  # graph name

    # error information
    for i in keyterms:
        for t in keyterms:
            if i != t and i in t and keyterms.index(i) < keyterms.index(t):
                print('\033[0;31m\nERROR!\n'
                      '"{}" comes before "{}" in key terms list!\n'
                      'this might conduct some error, \n'
                      'because term "{}" in the text would be detected as term "{}".\n'
                      'please re-order your terms list and insure "{}" after "{}".\033[0m'
                      .format(i, t, i, t, i, t))
                sys.exit(1)

    text = text.lower()

    chain = []
    for e in keyterms:  # for each element in key-terms
        if type(e) is str:  # for signle term
            chain = text2chain(e, keyterms, text, chain)
        elif type(e) is list:  # for a sub-list contained synonyms
            for t in e:
                chain = text2chain(t, keyterms, text, chain)

    chain.sort()  # sort by order of occurrence
    chain = list(x[1] for x in chain)  # keep index of terms only

    prx = np.zeros([len(keyterms), len(keyterms)])  # proximity data format
    for i in range(0, len(chain) - 1):
        prx[chain[i], chain[i + 1]] = 1
        prx[chain[i + 1], chain[i]] = 1
        prx[chain[i], chain[i]] = None  # 对角线的元素赋值为NaN

    # Step 4: calculate PFNet (if necessary)
    if pfnet:
        if max is not None and min is not None:  # similarity --> distances (if necessary)
            prx = max - prx + min
            # the value that out of range would be set as inf
            prx = np.where((prx > min) & (prx < max), prx, np.inf)

        prx = floyd(prx, r=r)

    # Step 5: convert it to a graph
    start, end = np.where(np.tril(prx) == True)
    pairs = []
    for i in range(0, len(start)):
        pairs.append([keyterms[start[i]], keyterms[end[i]]])
        print([keyterms[start[i]], keyterms[end[i]]])
    G.add_edges_from(pairs)

    return G


def text2chain(t, keyterms, text, chain, synonym=False):
    for index in finditer(t, text):  # obtain index of terms in the text
        if chain:
            """

            before add the new index into the list "chain", we need to 
            check the index to avoid the error.

            for example, when obtain a index of term "bees" in the text, it 
            would first check whether this index is contain in the span of 
            term "beeswax", if the answer is "True", this index wouldn't 
            be included in the "chain".

            for this purpose, please insure small terms (e.g., "bees") were 
            after bigger terms (e.g., "beeswax") in the terms list.

            """

            check = False
            for i in chain:
                if index.span()[0] >= i[0][0] and index.span()[1] <= i[0][1] and index.span() != i[0]:
                    check = True
                    break
            if not check:
                if synonym:
                    chain.append([index.span(), keyterms.index(synonym)])
                else:
                    chain.append([index.span(), keyterms.index(t)])
        else:
            if synonym:
                chain.append([index.span(), keyterms.index(synonym)])
            else:
                chain.append([index.span(), keyterms.index(t)])

    return chain
