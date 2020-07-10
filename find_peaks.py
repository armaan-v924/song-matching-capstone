#!/usr/bin/env python
# coding: utf-8

# ### Finding local maximums above threshold

# In[34]:


from numba import njit
import numpy as np
from scipy.ndimage.morphology import generate_binary_structure

@njit
def _peaks(data_2d, rows, cols, amp_min):
    """
    A Numba-optimized 2-D peak-finding algorithm.
    
    Parameters
    ----------
    data_2d : numpy.ndarray, shape-(H, W)
        The 2D array of data in which local peaks will be detected.

    rows : numpy.ndarray, shape-(N,)
        The 0-centered row indices of the local neighborhood mask
    
    cols : numpy.ndarray, shape-(N,)
        The 0-centered column indices of the local neighborhood mask
        
    amp_min : float
        All amplitudes at and below this value are excluded from being local 
        peaks.
    
    Returns
    -------
    List[Tuple[int, int]]
        (row, col) index pair for each local peak location. 
    """
    peaks = []
    
    # iterate over the 2-D data in col-major order
    for c, r in np.ndindex(*data_2d.shape[::-1]):
        if data_2d[r, c] <= amp_min:
            continue

        for dr, dc in zip(rows, cols):
            # don't compare element (r, c) with itself
            if dr == 0 and dc == 0:
                continue

            # mirror over array boundary
            if not (0 <= r + dr < data_2d.shape[0]):
                dr *= -1

            # mirror over array boundary
            if not (0 <= c + dc < data_2d.shape[1]):
                dc *= -1

            if data_2d[r, c] < data_2d[r + dr, c + dc]:
                break
        else:
            peaks.append((r, c))
    return peaks


# In[2]:


def local_peak_locations(data_2d, neighborhood, amp_min):
    """
    From 
    Defines a local neighborhood and finds the local peaks
    in the spectrogram, which must be larger than the specified `amp_min`.
    
    Parameters
    ----------
    data_2d : numpy.ndarray, shape-(H, W)
        The 2D array of data in which local peaks will be detected
    
    neighborhood : numpy.ndarray, shape-(h, w)
        A boolean mask indicating the "neighborhood" in which each
        datum will be assessed to determine whether or not it is
        a local peak. h and w must be odd-valued numbers
        
    amp_min : float
        All amplitudes at and below this value are excluded from being local 
        peaks.
    
    Returns
    -------
    List[Tuple[int, int]]
        (row, col) index pair for each local peak location.
    
    Notes
    -----
    The local peaks are returned in column-major order.
    """
    rows, cols = np.where(neighborhood)
    assert neighborhood.shape[0] % 2 == 1
    assert neighborhood.shape[1] % 2 == 1

    # center neighborhood indices around center of neighborhood
    rows -= neighborhood.shape[0] // 2
    cols -= neighborhood.shape[1] // 2
    
    return _peaks(data_2d, rows, cols, amp_min=amp_min)


# ### Finding the fingerprints of the peaks

# In[3]:


def compute_distance(point1, point2):
    """
    Computes distance between 2 points
    
    Parameters
    ----------
    point 1, point 2 : tuples (t, freq)
        
    Returns
    -------
    float: Distance between 2 points on the graph 
    """
    return np.sqrt(np.abs((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))


# In[4]:


def find_closest(peak_locations, index, fanout_size):
    """
    Returns a list of the (number) closest points
    
    Parameters
    ----------
    peak_locations: list
        Locations of peaks in the format [(x1,y1), (x2, y2), ...]
    index: integer
        index of current maximum location
    fanout_size: integer
        number of neighbors to look at  
        
    Returns
    -------
    list
        indexes of the fanout_size closest neighbors in peak_locations
    """
    dists = []
    for i in range(len(peak_locations)):
        dists.append(compute_distance(peak_locations[index], peak_locations[i]))
    dists = np.argsort(dists)
    return dists[1:fanout_size + 1]


# In[46]:


def create_fingerprints(peak_locations, sampling_rate, num_freqs):
    """
    Returns a list of the (number) closest points
    
    Parameters
    ----------
    peak_locations: list
        Locations of peaks in the format [(x1,y1), (x2, y2), ...]
    sampling_rate: integer
        
    Returns
    -------
    list of fingerprints
        In the format: [(f1, f2, delta t), ...]
    """
    fingerprints = []
    for i in range(len(peak_locations)):
        closest_points = find_closest(peak_locations, i, 4) #for testing, fanout_size is 4
        print("current point: ", peak_locations[i])
        for pt in closest_points:
            #tuple (fi, fj, delta t)
            print("     comparing to: ", peak_locations[pt])
            fingerprint = (num_freqs - 1 - peak_locations[i][0], num_freqs - 1 - peak_locations[pt][0], np.abs(peak_locations[i][1] - peak_locations[pt][1]))
            fingerprints.append(fingerprint)
    return fingerprints


# ### Testing functions

# In[48]:


#for testing, data is a 6 x 6 array of randomly generated numbers
data = np.floor(np.random.rand(6,10) * 30)
sampling_rate = 44100
num_freqs = len(data) #total num freqs (used to flip data vertically)
print("data:\n", data)
fp = generate_binary_structure(2, 1)
threshold = np.percentile(data, 75) #75th percentile amplitude
peaks = local_peak_locations(data, fp, threshold)

print("\npeaks: ", peaks, "\n")

fingerprints = create_fingerprints(peaks, sampling_rate, num_freqs)

print("\nfingerprints: \n", fingerprints)


# In[ ]:





# In[ ]:




