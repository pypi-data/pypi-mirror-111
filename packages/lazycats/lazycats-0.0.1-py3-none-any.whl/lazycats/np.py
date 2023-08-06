"""NumPy utility functions"""
import numpy as np

def top_k_indices(arr, k):
    """Get top `k` indices in INNERMOST axis"""
    temp = np.array(arr).astype(float) # copy
    if k > temp.shape[-1]:
        k = temp.shape[-1]

    top_ixs = np.flip(np.argsort(arr, axis=-1), axis=-1)
    top_k_ixs = np.take(top_ixs, range(k), axis=-1)
    return top_k_ixs


def contiguous_lengths(arr):
    """Get lengths of contiguous elements"""
    arr = np.array(arr)
    assert(len(arr.shape) == 1)
    change_points = np.where(arr[1:]-arr[:-1])[0] + 1 # find where values change
    if len(arr) not in change_points:
        change_points = np.append(change_points, len(arr))

    # compute change point relative to previous change point; this essentially computes
    # the length before the value changes
    return np.concatenate(([change_points[0]], change_points[1:]-change_points[:-1]))


def squash_consecutive_duplicates(arr):
    """Squash contiguous sections into single elements"""
    arr = np.array(arr)
    assert(len(arr.shape) == 1)
    # find where values change
    # this is the first index of any consecutive sequence of same values (except element 0)
    change_points = np.where(arr[1:]-arr[:-1])[0] + 1
    return np.concatenate((arr[0:1], arr[change_points]))


def divide_to_subsequences(seq, sub_len, pad=None, pre_pad=True):
    """
    Divide a sequence array into subsequences across outermost axis,
    padding the last subsequence as needed (default pad is zeroes)
    """
    seq = np.array(seq)
    if not pad: # default pad values
        pad = np.zeros(seq.shape[1:])
    else:
        pad = np.array(pad)

    assert(pad.shape == seq.shape[1:])

    pad_len = 0
    rem = len(seq)%sub_len
    if rem > 0:
        pad_len = sub_len - rem

    n_subseq_nopads = int(len(seq)/sub_len) # num. of subseq. that need no pads
    n_nopads = sub_len*n_subseq_nopads
    subseq = seq[:n_nopads].reshape((n_subseq_nopads, sub_len, *seq.shape[1:]))

    if pad_len > 0:
        if pre_pad:
            padded_subseq = np.append(np.array([pad]*pad_len),
                seq[n_nopads:], axis=0)
        else:
            padded_subseq = np.append(seq[n_nopads:],
                np.array([pad]*pad_len), axis=0)

        subseq = np.append(subseq, padded_subseq[np.newaxis, :], axis=0)

    return subseq
