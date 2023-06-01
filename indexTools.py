"""
This module contains a collection of utility functions used to manipulate indices related to frame data in videos.
Typically, these indices represent certain events or states in the video, such as start and end times of particular actions or scenes.
"""

import numpy as np
import copy

def bool2indice(boolList):
    """
    Convert boolean list to a list of indices where value is True.

    Parameters:
    boolList (list): List of boolean values.

    Returns:
    np.array: Indices where value is True.
    """
    return np.array([i for i, x in enumerate(boolList) if x])


def indiceSeq2startEnd(indiceList):
    """
    Convert a sequence of indices to a list of start and end points.

    Parameters:
    indiceList (list): List of indices.

    Returns:
    np.array: Start and end points of sequences in the list.
    """
    indDiff = np.diff(indiceList)
    starts = [indiceList[0]]
    ends = list()
    for i in range(1,len(indiceList)):
        if indDiff[i-1] !=1:
            ends.append(indiceList[i-1])
            starts.append(indiceList[i])
    ends.append(indiceList[-1])
    return np.array(list(zip(starts,ends)))


def boolSequence2startEndIndices(boolList):
    """
    Convert a boolean sequence to start and end indices.

    Parameters:
    boolList (list): List of boolean values.

    Returns:
    np.array: Start and end points of sequences in the list.
    """
    indices = bool2indice(boolList)
    return indiceSeq2startEnd(indices)


def bracket_Bools(boolList):
    """
    Expand True values in a boolean list to include the previous and next indices.

    Parameters:
    boolList (list): List of boolean values.

    Returns:
    list: Expanded list.
    """
    returnList = copy.deepcopy(boolList)
    for i in range(1,len(returnList)-1):
        if boolList[i] == 1:
            returnList[i-1],returnList[i+1] = (True,True)
    return returnList


def bracket_StartsEndOfSequence(startEndSequenceInd,seqLen):
    """
    Expand start and end of sequence by 1.

    Parameters:
    startEndSequenceInd (list): List of start and end sequence indices.
    seqLen (int): Sequence length.

    Returns:
    list: Expanded list.
    """
    returnList = copy.deepcopy(startEndSequenceInd)
    for seqI in range(returnList.shape[0]):
        
        if returnList[seqI,0] != 0 and returnList[seqI,1] >= seqLen:
            returnList[seqI,0] = returnList[seqI,0]-1
            returnList[seqI,1] = returnList[seqI,1]+1
    return returnList


def getDurationFromStartEnd(startEndInd):
    """
    Get duration from start and end indices.

    Parameters:
    startEndInd (list): List of start and end indices.

    Returns:
    np.array: List of durations.
    """
    return np.diff(startEndInd)

    
