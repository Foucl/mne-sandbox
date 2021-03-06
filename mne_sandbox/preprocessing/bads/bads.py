# Authors: Denis Engemann <denis.engemann@gmail.com>
#          Marijn van Vliet <w.m.vanvliet@gmail.com>
# License: BSD (3-clause)

import numpy as np
from mne.utils import verbose
from mne.io.pick import pick_info
from mne.io.pick import pick_types
from ...defaults import _handle_default
from . import faster_ as _faster


@verbose
def find_bad_channels(epochs, picks=None, method='faster', method_params=None,
                      return_by_metric=False, verbose=None):
    """Automatically find and mark bad channels.

    This function attempts to automatically mark bad EEG channels. Currently,
    the only supported method is the FASTER algorithm [1], but more methods
    will be added in the future. It operates on epoched data, to make sure only
    relevant data is analyzed.

    Parameters
    ----------
    epochs : Instance of Epochs
        The epochs for which bad channels need to be marked
    picks : list of int | None
        Channels to operate on. Defaults to EEG channels.
    method : {'faster'}
        The detection algorithm.
    method_params : dict | None
        The method parameters in a dict.

        If ``method`` equals 'faster', and ``method_params`` is None,
        defaults to the following parameters. Partial updates are supported.
        use_metrics : list of str
            List of metrics to use. Can be any combination of:
                'variance', 'correlation', 'hurst', 'kurtosis', 'line_noise'
            Defaults to all of them.
        thresh : float
            The threshold value, in standard deviations, to apply. A channel
            crossing this threshold value is marked as bad. Defaults to 3.
        max_iter : int
            The maximum number of iterations performed during outlier detection
            (defaults to 1, as in the original FASTER paper).
        eeg_ref_corr : bool
            If the EEG data has been referenced using a single electrode
            setting this parameter to True will enable a correction factor for
            the distance of each electrode to the reference. If an average
            reference is applied, or the mean of multiple reference electrodes,
            set this parameter to False. Defaults to False, which disables the
            correction.

    return_by_metric : bool
        Whether to return the bad channels as a flat list (False, default) or
        as a dictionary with the names of the used metrics as keys and the
        bad channels found by this metric as values. Is ignored if not
        supported by method.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).
        Defaults to self.verbose.

    Returns
    -------
    bads : list of str
        The names of the bad EEG channels.

    See Also
    --------
    find_bad_epochs
    find_bad_channels_in_epochs

    References
    ----------
    [1] H., Whelan R. and Reilly RB. FASTER: fully automated statistical
    thresholding for EEG artifact rejection. Journal of Neuroscience Methods,
    vol. 192, issue 1, pp. 152-162, 2010.
    """
    if picks is None:
        picks = pick_types(epochs.info, meg=True, eeg=True, exclude=[])
    _method_params = _handle_default('bad_channels' + '_' + method,
                                     method_params)
    if method == 'faster':
        bads = _faster._find_bad_channels(epochs, picks, **_method_params)
    else:
        raise NotImplementedError(
            'Come back later, for now there is only "FASTER"')

    if return_by_metric:
        return bads
    else:
        return _combine_indices(bads)


@verbose
def find_bad_epochs(epochs, picks=None, return_by_metric=False,
                    method='faster', method_params=None, verbose=None):
    """Automatically find and mark bad epochs.

    This function attempts to automatically mark bad epochs. Currently, the
    only supported method is the FASTER algorithm [1], but more methods will be
    added in the future. It operates on epoched data, to make sure only
    relevant data is analyzed.

    Parameters
    ----------
    epochs : Instance of Epochs
        The epochs to analyze.
    picks : list of int | None
        Channels to operate on. Defaults to EEG channels.
    method : {'faster'}
        The detection algorithm.
    method_params : dict | None
        The method parameters in a dict.

        If ``method`` equals 'faster', and ``method_params``is None,
        defaults to the following parameters. Partial updates are supported.
        use_metrics : list of str
            List of metrics to use. Can be any combination of:
            'amplitude', 'variance', 'deviation'. Defaults to all of them.
        thresh : float
            The threshold value, in standard deviations, to apply. A channel
            crossing this threshold value is marked as bad. Defaults to 3.
        max_iter : int
            The maximum number of iterations performed during outlier detection
            (defaults to 1, as in the original FASTER paper).

    return_by_metric : bool
        Whether to return the bad channels as a flat list (False, default) or
        as a dictionary with the names of the used metrics as keys and the
        bad channels found by this metric as values. Is ignored if not
        supported by method.
    verbose : bool, str, int, or None
        If not None, override default verbose level (see mne.verbose).
        Defaults to self.verbose.

    Returns
    -------
    bads : list of int
        The indices of the bad epochs.

    See Also
    --------
    find_bad_channels
    find_bad_channels_in_epochs

    References
    ----------
    [1] H., Whelan R. and Reilly RB. FASTER: fully automated statistical
    thresholding for EEG artifact rejection. Journal of Neuroscience Methods,
    vol. 192, issue 1, pp. 152-162, 2010.
    """
    if picks is None:
        picks = pick_types(epochs.info, meg=True, eeg=True, exclude='bads')
    _method_params = _handle_default('bad_epochs' + '_' + method,
                                     method_params)
    if method == 'faster':
        bads = _faster._find_bad_epochs(epochs, picks, **_method_params)
    else:
        raise NotImplementedError(
            'Come back later, for now there is only "FASTER"')

    if return_by_metric:
        return bads
    else:
        return _combine_indices(bads)


@verbose
def find_bad_channels_in_epochs(epochs, picks=None, method='faster',
                                method_params=None, return_by_metric=False):
    """Automatically find and mark bad channels in each epoch.

    This function attempts to automatically mark bad channels in each epochs.
    Currently, the only supported method is the FASTER algorithm [1], but more
    methods will be added in the future. It operates on epoched data, to make
    sure only relevant data is analyzed.

    Parameters
    ----------
    epochs : Instance of Epochs
        The epochs to analyze.
    picks : list of int | None
        Channels to operate on. Defaults to EEG channels.
    method : {'faster'}
        The detection algorithm.
    method_params : dict | None
        The method parameters in a dict.

        If ``method`` equals 'faster', and ``method_params``is None,
        defaults to the following parameters. Partial updates are supported.
        use_metrics : list of str
            List of metrics to use. Can be any combination of:
            'amplitude', 'variance', 'deviation', 'median_gradient',
            'line_noise'
            Defaults to all of them.
        thresh : float
            The threshold value, in standard deviations, to apply. A channel
            crossing this threshold value is marked as bad. Defaults to 3.
        max_iter : int
            The maximum number of iterations performed during outlier detection
            (defaults to 1, as in the original FASTER paper).
        eeg_ref_corr : bool
            If the EEG data has been referenced using a single electrode
            setting this parameter to True will enable a correction factor for
            the distance of each electrode to the reference. If an average
            reference is applied, or the mean of multiple reference electrodes,
            set this parameter to False. Defaults to False, which disables the
            correction.

    return_by_metric : bool
        Whether to return the bad channels as a flat list (False, default) or
        as a dictionary with the names of the used metrics as keys and the
        bad channels found by this metric as values. Is ignored if not
        supported by method.

    Returns
    -------
    bads : list of lists of int
        For each epoch, the indices of the bad channels.

    See Also
    --------
    find_bad_channels
    find_bad_epochs

    References
    ----------
    [1] H., Whelan R. and Reilly RB. FASTER: fully automated statistical
    thresholding for EEG artifact rejection. Journal of Neuroscience Methods,
    vol. 192, issue 1, pp. 152-162, 2010.
    """
    if picks is None:
        picks = pick_types(epochs.info, meg=True, eeg=True, exclude=[])

    _method_params = _handle_default('bad_channels_in_epochs' + '_' + method,
                                     method_params)
    if method == 'faster':
        bads = _faster._find_bad_channels_in_epochs(epochs, picks,
                                                    **_method_params)
    else:
        raise NotImplementedError(
            'Come back later, for now there is only "FASTER"')

    info = pick_info(epochs.info, picks, copy=True)
    if return_by_metric:
        bads = dict((m, _bad_mask_to_names(info, v)) for m, v in bads.items())
    else:
        bads = np.sum(list(bads.values()), axis=0).astype(bool)
        bads = _bad_mask_to_names(info, bads)

    return bads


def _bad_mask_to_names(info, bad_mask):
    """Remap mask to ch names"""
    bad_idx = [np.where(m)[0] for m in bad_mask]
    return [[info['ch_names'][k] for k in epoch] for epoch in bad_idx]


def _combine_indices(bads):
    """summarize indices"""
    return list(set(v for val in bads.values() if len(val) > 0 for v in val))
