#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np
import xarray as xr

from cdflib import cdfread

# Local imports
from ..pyrf import datetime642iso8601

from .list_files import list_files

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2021"
__license__ = "MIT"
__version__ = "2.3.7"
__status__ = "Prototype"


def _get_energy_dplus_dminus(eis_allt, data_path):
    tint = list(datetime642iso8601(eis_allt.time.data[[0, -1]]))

    name_ = eis_allt.t0.attrs["FIELDNAM"]

    mms_id = int(name_.split("_")[0][-1])

    var = {"inst": "epd-eis", "lev": "l2"}

    if "brst" in name_:
        var["tmmode"] = "brst"
    else:
        var["tmmode"] = "srvy"

    var["dtype"] = name_.split("_")[-5]

    files = list_files(tint, mms_id, var, data_path=data_path)

    with cdfread.CDF(files[0]) as file:
        d_plus = file.varget(eis_allt.t0.energy.attrs["DELTA_PLUS_VAR"])
        d_minus = file.varget(eis_allt.t0.energy.attrs["DELTA_MINUS_VAR"])

    return d_plus, d_minus


def eis_combine_proton_spec(phxtof_allt, extof_allt):
    r"""Combine ExTOF and PHxTOF proton energy spectra into a single combined
    Dataset.

    Parameters
    ----------
    phxtof_allt : xarray.Dataset
        Dataset containing the PHxTOF energy spectrum of the 6 telescopes.
    extof_allt : xarray.Dataset
        Dataset containing the ExTOF energy spectrum of the 6 telescopes.

    Returns
    -------
    comb_allt : xarray.Dataset
        Dataset containing the combined PHxTOF and ExTOF energy spectrum of
        the 6 telescopes.

    """

    scopes_phxtof = list(filter(lambda x: x[0] == "t", phxtof_allt))
    scopes_extof = list(filter(lambda x: x[0] == "t", extof_allt))
    assert scopes_extof == scopes_phxtof

    data_path = extof_allt.attrs["data_path"]
    dp_phxtof, dm_phxtof = _get_energy_dplus_dminus(phxtof_allt, data_path)
    dp_extof, dm_extof = _get_energy_dplus_dminus(extof_allt, data_path)

    out_dict = {}

    for scope in scopes_phxtof:
        proton_phxtof = phxtof_allt[scope]
        proton_extof = extof_allt[scope]

        nt_phxtof, nt_extof = [len(proton_phxtof.time), len(proton_extof.time)]

        phxtof_data = proton_phxtof.data.copy()
        extof_data = proton_extof.data.copy()

        en_phxtof, en_extof = [proton_phxtof.energy.data,
                               proton_extof.energy.data]
        idx_phxtof = np.where(en_phxtof < en_extof[0])[0]
        cond_ = np.logical_and(en_phxtof > en_extof[0],
                               en_phxtof < en_phxtof[-1])
        idx_phxtof_cross = np.where(cond_)[0]

        idx_extof_cross = np.where(en_extof < en_phxtof[-2])[0]
        idx_extof = np.where(en_extof > en_phxtof[-2])[0]

        n_phxtof = idx_phxtof.size
        n_phxtof_cross = idx_phxtof_cross.size
        n_extof = idx_extof.size

        n_en = n_phxtof + n_phxtof_cross + n_extof

        comb_en, comb_en_low, comb_en_hig = [np.zeros(n_en) for _ in range(3)]

        comb_array = np.zeros((nt_phxtof, n_en))
        comb_array[:, 0:n_phxtof] = phxtof_data[:, idx_phxtof]
        comb_en[0:n_phxtof] = en_phxtof[idx_phxtof]
        comb_en_low[0:n_phxtof] = comb_en[0:n_phxtof] - dm_phxtof[idx_phxtof]
        comb_en_hig[0:n_phxtof] = comb_en[0:n_phxtof] + dp_phxtof[idx_phxtof]

        for (i, i_phx), i_ex in zip(enumerate(idx_phxtof_cross),
                                    idx_extof_cross):
            idx_ = n_phxtof + i
            comb_array[:, idx_] = np.nanmean(np.vstack([phxtof_data[:, i_phx],
                                                        extof_data[:, i_ex]]),
                                             axis=0)
            comb_en_low[idx_] = np.nanmin([en_phxtof[idx_] - dm_phxtof[idx_],
                                           en_extof[i] - dm_extof[i]])
            comb_en_hig[idx_] = np.nanmax([en_phxtof[idx_] + dp_phxtof[idx_],
                                           en_extof[i] + dp_extof[i]])
            comb_en[idx_] = np.sqrt(comb_en_low[idx_] * comb_en_hig[idx_])

        comb_array[:, len(en_phxtof) - 1:] = extof_data[:, idx_extof]
        comb_en[len(en_phxtof) - 1:] = en_extof[idx_extof]

        out_dict[scope] = xr.DataArray(comb_array,
                                       coords=[proton_phxtof.time.data,
                                               comb_en],
                                       dims=["time", "energy"])

    out_dict["spin"] = phxtof_allt.spin

    comb_allt = xr.Dataset(out_dict)

    return comb_allt
