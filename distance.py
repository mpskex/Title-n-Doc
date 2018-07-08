#coding: utf-8
import numpy as np

""" Calculating distance between two sets

"""

def euclid_dist(pa, pb):
    """ Euclidean Distance
    Args:
        pa: vector a to (numpy array)
        pb: vector b to (numpy array)
    """
    return np.linalg.norm(pa - pb)

def cosine(a, b):
    """ Calculate cosine simliarity
    Args:
        a:  vec a (numpy array)
        b:  vec b (numpy array)
    """
    return np.dot(a, b) / (np.linalg.norm(a), np.linalg.norm(b))

def hausdorff_dist(set_a, set_b):
    """ Calculation of Hausdorff distance
    Args:
        set_a:  a set of arbitary size (2-dim numpy array)
        set_b:  a set of arbitary size
    """
    set_dis = np.zeros((set_a.shape[0], set_b.shape[0]), np.float)
    #   calculate dist for both set a and set b
    for ridx in range(set_a.shape[0]):
        for idx in range(set_b.shape[0]):
            set_dis[ridx, idx] = np.linalg.norm(set_a[ridx]-set_b[idx])
    a_b = np.max(np.min(set_dis, axis=1), axis=0)
    b_a = np.max(np.min(set_dis, axis=0), axis=0)
    return max(a_b, b_a)

def mean(a):
    return np.mean(a, axis=1)

def var(a):
    return np.var(a, axis=1)

if __name__ == '__main__':
    A = np.array([[4,0], [1,0], [2,0], [3,0], [4,0]])
    B = np.array([[0,3], [1,3], [2,3], [3,3], [3,2], [4,2]])
    print hausdorff_dist(A, B)
    
