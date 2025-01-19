"""
PINGU_unified_ingestion.py

This module provides functionality to unify two different sources of penguin trajectory data 
into a single "trajectory table". The module handles:

1) **Open Dataset (HDF5)** - Processed using :class:`TrajectoryProcessor` from peguin_ana01:
   - Reads HDF5 files.
   - Preserves original segment numbers stored in `df_interp["segment"]`.
   - Preserves frame indices as they appear in the data index (or you may adapt to a custom column).
   - Fills head-angle columns with ``NaN``, as the open dataset only provides body yaw.

2) **Closed Dataset (CSV)** - Processed using functions from PINGU_HEAD_saccadeTypeSpecific_trigAvg:
   - Reads CSV files grouped by an "Identifier" field (converted to `segment_id`).
   - Increments segment IDs for each file.
   - Provides both head and body yaw data, plus translational velocity where applicable.

All data are merged into a single, unified trajectory table containing the following columns:

- segment_id : int
  The unique segment identifier. In the open dataset, it is read from the "segment" column.
  In the closed dataset, it is incremented per CSV file or Identifier.
- frame_index : int
  The unaltered frame index from each dataset (taken from the DataFrame index or a dedicated frame column).
- body_yaw_rad : float
  Body yaw in radians.
- body_yaw_speed_degPs : float
  Body yaw speed in degrees per second.
- head_yaw_rad : float
  Head yaw in radians (``NaN`` for the open dataset).
- head_yaw_speed_degPs : float
  Head yaw speed in degrees per second (``NaN`` for the open dataset).
- translational_velocity_mPs : float
  Translational velocity in metres per second (calculated or read, if available).
- x_position_m, y_position_m : float
  Position in metres along the x and y axes (if available). Typically absent (``NaN``) for the closed dataset.
- species : str
  Penguin species, e.g. "gentoo" or "rockhopper".
- dataset : str
  A label indicating "open" or "closed" data origin.

The final unified trajectory DataFrame is saved as a CSV file in the specified output path.
"""

import os
import glob
import numpy as np
import pandas as pd

from peguin_ana01 import TrajectoryProcessor
from PINGU_HEAD_saccadeTypeSpecific_trigAvg import read_cvs_into_dataframe, calculate_translational_velocity

# -----------------------------------------------------------------------------
# Configuration Constants
# -----------------------------------------------------------------------------

#: Directory containing the open HDF5 dataset.
PATH_OPEN_DATA = "/home/geuba03p/Penguin_Rostock/penguins/sorted_and_filtered/"

#: Directory containing the closed CSV dataset.
PATH_CLOSED_DATA = "/home/geuba03p/Penguin_Rostock/pengu_head_movies/"

#: Output directory for the unified CSV file.
OUTPUT_PATH = "/home/geuba03p/Penguin_Rostock/unified_outputs/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

#: Image width in pixels (for open dataset).
IM_WIDTH = 1402

#: Image height in pixels (for open dataset).
IM_HEIGHT = 788

#: Frame rate (frames per second) for the open dataset.
FRAME_RATE_OPEN = 30

#: Mean pixel-to-metre conversion factor for the open dataset.
PIX2M = np.array([0.97 / 124.6, 0.3 / 66, 0.4 / 76.2]).mean()

#: Frame rate (frames per second) for the closed dataset.
FRAME_RATE_CLOSED = 25

#: Columns that the final unified trajectory DataFrame must contain.
REQUIRED_COLS = [
    "segment_id",
    "frame_index",
    "body_yaw_rad",
    "body_yaw_speed_degPs",
    "head_yaw_rad",
    "head_yaw_speed_degPs",
    "translational_velocity_mPs",
    "x_position_m",
    "y_position_m",
    "species",
    "dataset"
]

def create_empty_unified_df() -> pd.DataFrame:
    """
    Create an empty DataFrame with the columns in :data:`REQUIRED_COLS`.

    Returns
    -------
    pd.DataFrame
        Empty DataFrame containing the required columns.
    """
    return pd.DataFrame(columns=REQUIRED_COLS)

def ingest_open_data(path_to_open: str) -> pd.DataFrame:
    """
    Ingests the open (HDF5) dataset by:
    - Scanning all `.h5` files recursively in the given directory.
    - Processing each file with :class:`TrajectoryProcessor`.
    - Preserving segment numbers from the `segment` column (renamed to `segment_id`).
    - Preserving original frame indices from the DataFrame index.
    - Renaming yaw- and speed-related columns to unify them with the final schema.
    - Filling missing columns with `NaN`.

    Parameters
    ----------
    path_to_open : str
        Base directory where `.h5` files for the open dataset are located.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the unified trajectory data for the open dataset.
    """
    pattern = os.path.join(path_to_open, "**", "*.h5")
    file_list = glob.glob(pattern, recursive=True)
    all_dfs = []

    for file_path in file_list:
        df_raw = pd.read_hdf(file_path)
        if df_raw.empty:
            continue

        tp = TrajectoryProcessor(
            df_raw,
            IM_WIDTH,
            IM_HEIGHT,
            PIX2M,
            FRAME_RATE_OPEN
        )
        df_interp, _ = tp.main()

        if df_interp is None or df_interp.empty:
            continue

        # If 'segment' column is present, rename it to 'segment_id'. Otherwise default to 0.
        if "segment" in df_interp.columns:
            df_interp.rename(columns={"segment": "segment_id"}, inplace=True)
        else:
            df_interp["segment_id"] = 0

        # Keep the original frame indexing:
        df_interp["frame_index"] = df_interp.index

        # Rename columns to match the final schema
        if "yaw_rad" in df_interp.columns:
            df_interp.rename(columns={"yaw_rad": "body_yaw_rad"}, inplace=True)
        if "rot_speed_degPs" in df_interp.columns:
            df_interp.rename(columns={"rot_speed_degPs": "body_yaw_speed_degPs"}, inplace=True)
        if "trans_speed_mPs" in df_interp.columns:
            df_interp.rename(columns={"trans_speed_mPs": "translational_velocity_mPs"}, inplace=True)
        if "center_of_mass_x" in df_interp.columns:
            df_interp.rename(columns={"center_of_mass_x": "x_position_m"}, inplace=True)
        if "center_of_mass_y" in df_interp.columns:
            df_interp.rename(columns={"center_of_mass_y": "y_position_m"}, inplace=True)

        # Insert missing head columns as NaN
        df_interp["head_yaw_rad"] = np.nan
        df_interp["head_yaw_speed_degPs"] = np.nan

        # Infer species from the file name
        species = "gentoo"  # fallback
        if "Rockhopper" in file_path:
            species = "rockhopper"
        elif "Gentoo" in file_path:
            species = "gentoo"
        df_interp["species"] = species

        df_interp["dataset"] = "open"

        # Ensure all required columns exist
        for col in REQUIRED_COLS:
            if col not in df_interp.columns:
                df_interp[col] = np.nan

        df_final = df_interp[REQUIRED_COLS].copy()
        all_dfs.append(df_final)

    if not all_dfs:
        return create_empty_unified_df()

    df_open = pd.concat(all_dfs, ignore_index=True)
    return df_open

def ingest_closed_data(path_to_closed: str) -> pd.DataFrame:
    """
    Ingests the closed (CSV) dataset by:
    - Scanning CSV files grouped by 'Identifier'.
    - Renaming body and head yaw speed columns to match the final schema.
    - Interpreting each 'Identifier' group as a unique `segment_id`.
    - Preserving original frame indices from the DataFrame index.
    - Setting x/y positions to NaN for the closed dataset.
    - Assigning species="gentoo" and dataset="closed".

    Parameters
    ----------
    path_to_closed : str
        Base directory where `.csv` files for the closed dataset are located.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the unified trajectory data for the closed dataset.
    """
    df_all = read_cvs_into_dataframe(path_to_closed, frame_rate=FRAME_RATE_CLOSED)
    if df_all.empty:
        return create_empty_unified_df()

    grouped = df_all.groupby("Identifier")
    all_files = []

    for identifier, df_sub in grouped:
        df_sub = df_sub.copy()

        # Keep raw index as frame_index
        df_sub["frame_index"] = df_sub.index

        # Rename speed columns
        if "body_yaw_speed" in df_sub.columns:
            df_sub.rename(columns={"body_yaw_speed": "body_yaw_speed_degPs"}, inplace=True)
        if "head_yaw_speed" in df_sub.columns:
            df_sub.rename(columns={"head_yaw_speed": "head_yaw_speed_degPs"}, inplace=True)

        # Convert 'Identifier' -> 'segment_id'
        if "Identifier" in df_sub.columns:
            df_sub.rename(columns={"Identifier": "segment_id"}, inplace=True)

        # No x/y positions in the closed dataset
        df_sub["x_position_m"] = np.nan
        df_sub["y_position_m"] = np.nan

        # Only gentoo in the closed dataset
        df_sub["species"] = "gentoo"
        df_sub["dataset"] = "closed"

        # Ensure all required columns exist
        for col in REQUIRED_COLS:
            if col not in df_sub.columns:
                df_sub[col] = np.nan

        df_final = df_sub[REQUIRED_COLS].copy()
        all_files.append(df_final)

    if not all_files:
        return create_empty_unified_df()

    df_closed = pd.concat(all_files, ignore_index=True)
    return df_closed

def main() -> None:
    """
    Main entry point for unifying the open (HDF5) and closed (CSV) datasets into
    a single trajectory table, saved as a CSV file.

    Steps:
    1. Ingest open data using :func:`ingest_open_data`.
    2. Ingest closed data using :func:`ingest_closed_data`.
    3. Concatenate both DataFrames.
    4. Save the final unified trajectory data to :data:`OUTPUT_PATH`.

    Returns
    -------
    None
        The function saves the output CSV to disk and prints a confirmation message.
    """
    # 1) Ingest open data
    df_open = ingest_open_data(PATH_OPEN_DATA)

    # 2) Ingest closed data
    df_closed = ingest_closed_data(PATH_CLOSED_DATA)

    # 3) Combine DataFrames
    df_trajectories = pd.concat([df_open, df_closed], ignore_index=True)

    # 4) Save
    out_path = os.path.join(OUTPUT_PATH, "unified_trajectories_head_body.csv")
    df_trajectories.to_csv(out_path, index=False)
    print(f"Unified trajectory data saved to: {out_path}")

    # Summarize final columns
    print("Final columns:", df_trajectories.columns.tolist())

if __name__ == "__main__":
    main()
