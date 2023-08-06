import mne
from mne.preprocessing import (
    create_ecg_epochs,
    create_eog_epochs,
    ICA,
)
from autoreject import (
    get_rejection_threshold
)

from pymento_meg.utils import _construct_path
from pathlib import Path


def remove_eyeblinks_and_heartbeat(raw,
                                   subject,
                                   figdir,
                                   events,
                                   eventid):
    """
    Find and repair eyeblink and heartbeat artifacts in the data.
    Data should be filtered.
    Importantly, ICA is fitted on artificially epoched data with reject
    criteria estimates via the autoreject package - this is done to reject high-
    amplitude artifacts to influence the ICA solution.
    The ICA fit is then applied to the raw data.
    :param raw: Raw data
    :param subject: str, subject identifier, e.g., '001'
    :param figdir:
    """
    # prior to an ICA, it is recommended to high-pass filter the data
    # as low frequency artifacts can alter the ICA solution. We fit the ICA
    # to high-pass filtered (1Hz) data, and apply it to non-highpass-filtered
    # data
    filt_raw = raw.copy()
    filt_raw.load_data().filter(l_freq=1., h_freq=None)
    # evoked eyeblinks and heartbeats for diagnostic plots
    eog_evoked = create_eog_epochs(filt_raw).average()
    eog_evoked.apply_baseline(baseline=(None, -0.2))
    ecg_evoked = create_ecg_epochs(filt_raw).average()
    ecg_evoked.apply_baseline(baseline=(None, -0.2))
    # make sure that we actually found sensible artifacts here
    eog_fig = eog_evoked.plot_joint()
    for i, fig in enumerate(eog_fig):
        fname = _construct_path(
            [
                Path(figdir),
                f"sub-{subject}",
                "meg",
                f"evoked-artifact_eog_sub-{subject}_{i}.png",
            ]
        )
        fig.savefig(fname)
    ecg_fig = ecg_evoked.plot_joint()
    for i, fig in enumerate(ecg_fig):
        fname = _construct_path(
            [
                Path(figdir),
                f"sub-{subject}",
                "meg",
                f"evoked-artifact_ecg_sub-{subject}_{i}.png",
            ]
        )
        fig.savefig(fname)
    # define the actual events (7 seconds from fixation cross onset).
    epochs = mne.Epochs(filt_raw, events, event_id=eventid,
                        tmin=0, tmax=7,
                        picks='meg', baseline=None)
    # First, estimate rejection criteria for high-amplitude artifacts
    reject = get_rejection_threshold(epochs)
    # run an ICA to capture heartbeat and eyeblink artifacts.
    # 15 components are hopefully enough to capture them.
    # set a seed for reproducibility
    ica = ICA(n_components=30, max_iter='auto', random_state=42)
    ica.fit(epochs, reject=reject)#, tstep=tstep)

    # use the EOG channel to select ICA components:
    ica.exclude = []
    # find which ICs match the EOG pattern
    eog_indices, eog_scores = ica.find_bads_eog(filt_raw)
    ica.exclude = eog_indices

    # barplot of ICA component "EOG match" scores
    scores = ica.plot_scores(eog_scores)
    fname = _construct_path(
        [
            Path(figdir),
            f"sub-{subject}",
            "meg",
            f"ica-scores_artifact-eog_sub-{subject}.png",
        ]
    )
    scores.savefig(fname)
    # plot diagnostics
    figs = ica.plot_properties(filt_raw, picks=eog_indices)
    for i, fig in enumerate(figs):
        fname = _construct_path(
            [
                Path(figdir),
                f"sub-{subject}",
                "meg",
                f"ica-property{i}_artifact-eog_sub-{subject}.png",
            ]
        )
        fig.savefig(fname)
    # plot ICs applied to the averaged EOG epochs, with EOG matches highlighted
    sources = ica.plot_sources(eog_evoked)
    fname = _construct_path(
        [
            Path(figdir),
            f"sub-{subject}",
            "meg",
            f"ica-sources_artifact-eog_sub-{subject}.png",
        ]
    )
    sources.savefig(fname)
    # find ECG components
    ecg_indices, ecg_scores = ica.find_bads_ecg(filt_raw, method='ctps',
                                                threshold='auto')
    ica.exclude.extend(ecg_indices)

    scores = ica.plot_scores(ecg_scores)
    fname = _construct_path(
        [
            Path(figdir),
            f"sub-{subject}",
            "meg",
            f"ica-scores_artifact-ecg_sub-{subject}.png",
        ]
    )
    scores.savefig(fname)

    figs = ica.plot_properties(filt_raw, picks=ecg_indices)
    for i, fig in enumerate(figs):
        fname = _construct_path(
            [
                Path(figdir),
                f"sub-{subject}",
                "meg",
                f"ica-property{i}_artifact-ecg_sub-{subject}.png",
            ]
        )
        fig.savefig(fname)

    # plot ICs applied to the averaged ECG epochs, with ECG matches highlighted
    sources = ica.plot_sources(ecg_evoked)
    fname = _construct_path(
        [
            Path(figdir),
            f"sub-{subject}",
            "meg",
            f"ica-sources_artifact-ecg_sub-{subject}.png",
        ]
    )
    sources.savefig(fname)
    # apply the ICA to the raw data
    raw.load_data()
    ica.apply(raw)
    return raw
