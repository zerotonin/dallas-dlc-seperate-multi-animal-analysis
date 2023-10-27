import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import SaccadeAnalysis
import seaborn as sns

def butter_lowpass_filter(data, cutoff_freq, sample_rate):
    """Applies a Butterworth low-pass filter to the data.

    Args:
        data (array-like): The data to be filtered.
        cutoff_freq (float): The cutoff frequency of the filter.
        sample_rate (float): The sampling rate of the data.

    Returns:
        array-like: The filtered data.
    """
    # Calculate the Nyquist frequency
    nyquist = 0.5 * sample_rate
    
    # Normalize the cutoff frequency by the Nyquist frequency
    normal_cutoff = cutoff_freq / nyquist
    
    # Design the filter
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    
    # Apply the filter
    y = filtfilt(b, a, data)
    return y

def plot_angles_over_time(df):
    """Plots the head and body yaw angles over time, indicating starts and stops of the identifier.

    Args:
        df (pd.DataFrame): DataFrame containing the angles and identifiers.

    Returns:
        None: Shows the plot.
    """
    
    plt.figure(figsize=(14, 8))
    
    # Plotting angles
    plt.subplot(2, 1, 1)
    plt.title("Head and Body Yaw Angles over Time")
    plt.plot(df['head_yaw_speed'], label='Head Yaw Angle (radians)')
    plt.plot(df['body_yaw_speed'], label='Body Yaw Angle (radians)')
    plt.xlabel("Time")
    plt.ylabel("Angle (radians)")
    plt.legend()

    # Indicating starts and stops of the identifier
    unique_identifiers = df['Identifier'].unique()
    for identifier in unique_identifiers:
        start_idx = df[df['Identifier'] == identifier].index[0]
        end_idx = df[df['Identifier'] == identifier].index[-1]
        
        plt.axvline(x=start_idx, color='r', linestyle='--', alpha=0.6)
        plt.text(start_idx, 0, f"Start {identifier}", rotation=90)
        
        plt.axvline(x=end_idx, color='g', linestyle='--', alpha=0.6)
        plt.text(end_idx, 0, f"End {identifier}", rotation=90)

    plt.tight_layout()
    plt.show()




def calculate_vector_angle(df, point1, point2):
    """Calculates the angle of the vector formed by two points with respect to the x-axis.

    Args:
        df (pd.DataFrame): DataFrame containing the coordinates of the points.
        point1 (str): Name of the first point (e.g., 'neck').
        point2 (str): Name of the second point (e.g., 'beak').

    Returns:
        pd.Series: A Pandas Series containing the angles in radians.
    """
    
    # Calculate the vector components
    dx = df[f'{point2}_x'] - df[f'{point1}_x']
    dy = df[f'{point2}_y'] - df[f'{point1}_y']
    
    # Calculate the angle using arctan2
    angles = np.arctan2(dy, dx)
    
    # Unwrap the angles to avoid discontinuity
    angles = np.unwrap(angles)
    
    return angles

def read_csvs_into_dataframe(target_folder,frame_rate=25):
    """Reads all CSV files in a target folder into a Pandas DataFrame and adds an 'Identifier' field.

    Args:
        target_folder (str): Path to the folder containing the CSV files.

    Returns:
        pd.DataFrame: DataFrame containing all data from the CSV files, with an added 'Identifier' column.
    """
    
    all_data = []
    
    for filename in os.listdir(target_folder):
        if filename.endswith('.csv'):
            filepath = os.path.join(target_folder, filename)
            
            # Extract the first two digits from the filename
            identifier = ''.join(filter(str.isdigit, filename))[:2]
            
            # Read the CSV file into a DataFrame, skipping the first row and combining the next two rows as header
            df = pd.read_csv(filepath, skiprows=[0], header=[0, 1])
            
            # Combine multi-level columns into a single level with underscore
            df.columns = ['_'.join(col).strip() for col in df.columns.values]

            # Calculate the angle for the vector from neck to beak
            df['head_yaw_rad'] = calculate_vector_angle(df, 'neck', 'beak')
            
            # Calculate the angle for the vector from caudal to neck
            df['body_yaw_rad'] = calculate_vector_angle(df, 'caudal', 'neck')
            

            # Apply a simple moving average for smoothing (window size = 5)
            #df['head_yaw_rad_smoothed'] = df['head_yaw_rad'].rolling(window=5).mean()
            #df['body_yaw_rad_smoothed'] = df['body_yaw_rad'].rolling(window=5).mean()
            df['head_yaw_rad'] = butter_lowpass_filter(df['head_yaw_rad'], 0.995, 25)
            df['body_yaw_rad'] = butter_lowpass_filter(df['body_yaw_rad'], 0.995, 25)


            # Convert angles to degrees
            df['head_yaw_deg'] = np.degrees(df['head_yaw_rad'])
            df['body_yaw_deg'] = np.degrees(df['body_yaw_rad'])
            
            # Calculate the first derivative to get the rate of change of the angle
            df['head_yaw_speed'] = df['head_yaw_deg'].diff() * frame_rate
            df['body_yaw_speed'] = df['body_yaw_deg'].diff() * frame_rate
    
            # Add the identifier to a new column
            df['Identifier'] = identifier
            
            all_data.append(df)
    
    # Combine all individual DataFrames into one DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)
    
    return combined_df

def plot_triggered_avg(mean,error,ylabel,time_ax):
    """
    This function creates a line plot of the average (triggered) data over time. 
    It also includes a shaded region indicating the standard error of the mean (SEM) around the line.
    
    Parameters
    ----------
    mean : array-like
        1D array-like object (list, numpy array, etc.) containing the mean data points over time.
        
    error : array-like
        1D array-like object containing the standard error of the mean (SEM) for each data point over time.

    ylabel : str
        The label to be set for the y-axis of the plot.

    Returns
    -------
    None. 
    The function directly generates a plot which displays the mean data with its SEM over time.
    
    Example
    -------
    >>> plot_triggered_avg(mean_data, sem_data, 'Average Value')
    """
    # Create the line plot
    plt.figure(figsize=(10,6))
    plt.plot(time_ax, mean)

    # Add transparent error band
    plt.fill_between(time_ax, mean - error, mean + error, color='blue', alpha=0.2)
    plt.xlabel('time, ms')
    plt.ylabel(ylabel)

# Usage example:
target_folder =  '/home/bgeurten/pengu_head_movies/'
combined_df = read_csvs_into_dataframe(target_folder)


# Initialize SaccadeAnalysis with a threshold of 500
sa = SaccadeAnalysis.SaccadeAnalysis(25)

# Lists to store saccade analysis results
saccades_accumulated = []
pos_angle_matrix_accumulated = []
pos_velocity_matrix_accumulated = []
neg_angle_matrix_accumulated = []
neg_velocity_matrix_accumulated = []

# Group the DataFrame by 'Identifier'
grouped = combined_df.groupby('Identifier')

# Iterate over each group
for name, group in grouped:
    print(f"Processing Identifier: {name}")
    

    # Load the data from the .tra file into a numpy matrix

    
    # Identify saccades and other related parameters using the SaccadeAnalysis object
    saccades, pos_angle_matrix, pos_velocity_matrix, neg_angle_matrix, neg_velocity_matrix = sa.main(group['head_yaw_rad'].to_numpy(),250,25,False)
    
    # Save output
    saccades_accumulated += saccades
    pos_angle_matrix_accumulated.append(pos_angle_matrix)
    pos_velocity_matrix_accumulated.append(pos_velocity_matrix)
    neg_angle_matrix_accumulated.append(neg_angle_matrix)
    neg_velocity_matrix_accumulated.append(neg_velocity_matrix)

# Create a dataframe from the list of saccades for easier visualization
saccades_df = pd.DataFrame(saccades_accumulated)

# Convert saccade duration to milliseconds
saccades_df['saccade_duration_ms'] = saccades_df.saccade_duration_s*1000


# Concatenate matrices for plotting
ang = np.concatenate((np.concatenate(pos_angle_matrix_accumulated),np.concatenate(neg_angle_matrix_accumulated)*-1))
vel = np.concatenate((np.concatenate(pos_velocity_matrix_accumulated),np.concatenate(neg_velocity_matrix_accumulated)*-1))

# Calculate mean and SEM for plotting
mean_ang = np.nanmean(ang, axis=0)
sem_ang = np.nanstd(ang, axis=0) / np.sqrt(ang.shape[0])

mean_vel = np.nanmean(vel, axis=0)
sem_vel = np.nanstd(vel, axis=0) / np.sqrt(vel.shape[0])

# Plot the average angle and velocity with SEM as a transparent area around the line
time_ax =  np.linspace(-500,500,25)
plot_triggered_avg(mean_ang, sem_ang, 'angle, deg',time_ax)
plot_triggered_avg(mean_vel, sem_vel, 'velocity, deg/s',time_ax)
# Plot the distribution of saccade durations
sns.displot(saccades_df, x="saccade_duration_ms", stat="probability", bins= np.linspace(10,100,10))

plt.show()