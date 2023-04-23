import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
class TrajectoryProcessor:
    """
    A class to process trajectories from a DataFrame, including interpolating missing data, converting coordinates,
    calculating yaw angles, applying a Gaussian low-pass filter, and plotting a quiver plot.
    """
    def __init__(self, df, image_width, image_height, pix2m,frame_rate, gap = 10, filt_sigma =3):
        """
        Initialize the TrajectoryProcessor with the given DataFrame and parameters.

        Args:
            df (pd.DataFrame): The input DataFrame containing trajectory data.
            image_width (int): The width of the image in pixels.
            image_height (int): The height of the image in pixels.
            pix2m (float): The conversion factor from pixels to meters.
            frame_rate (int): The frame rate of the video from which the trajectory data was extracted.
            gap (int, optional): The maximum gap between frames to consider as the same trajectory segment. Default is 10.
            filt_sigma (int, optional): The sigma value for the Gaussian low-pass filter. Default is 2.
        """
        self.df           = df
        self.image_width  = image_width
        self.image_height = image_height
        self.pix2m        = pix2m
        self.frame_rate   = frame_rate
        self.gap          = gap
        self.min_len      = filt_sigma
        self.filt_sigma   = filt_sigma

    def get_trajectory_segments(self):
        """
        Split the input DataFrame into separate trajectory segments based on the specified gap.

        Returns:
            list: A list of lists containing the frame indices for each trajectory segment.
        """        
        frame_series = pd.Series(self.df.index)
        frame_diff = frame_series.diff()
        split_indices = frame_diff[frame_diff > self.gap].index
        segments = [frame_series.iloc[start:end].tolist() for start, end in zip([0] + list(split_indices), list(split_indices) + [None])]
        segments = [entry for entry in segments if len(entry) >= self.min_len]
        return segments

    def interpolate_trajectory(self, df):
        """
        Interpolate missing data in the input DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing trajectory data.

        Returns:
            pd.DataFrame: The interpolated DataFrame with missing data filled in.
        """
        new_index = pd.RangeIndex(df.index.min(), df.index.max() + 1)
        df_reindexed = df.reindex(new_index)
        df_numeric = df_reindexed.drop(columns=['name'])
        df_interpolated_numeric = df_numeric.interpolate()
        df_interpolated = df_interpolated_numeric.assign(name=df_reindexed['name'])
        df_interpolated['name'].fillna(method='ffill', inplace=True)
        return df_interpolated

    def interpolate_all_segments(self, segments):
        """
        Interpolate missing data for all trajectory segments.

        Args:
            segments (list): A list of lists containing the frame indices for each trajectory segment.

        Returns:
            pd.DataFrame: The interpolated DataFrame with missing data filled in for all segments.
        """
        df_list = list()
        for i in range(len(segments)):
            seg = segments[i]
            df_seg = self.df.loc[seg]
            df_seg['segment'] = i
            df_interp = self.interpolate_trajectory(df_seg)
            df_list.append(df_interp)
        return pd.concat(df_list)
    
    def rel_coord_to_m(self):
        """
        Convert relative coordinates in the input DataFrame to meters.
        """
        self.df.center_of_mass_x = self.df.center_of_mass_x * self.image_width * self.pix2m
        self.df.center_of_mass_y = self.df.center_of_mass_y * self.image_height * self.pix2m
        self.df.bounding_box_x0  = self.df.bounding_box_x0 * self.image_width * self.pix2m
        self.df.bounding_box_y0  = self.df.bounding_box_y0 * self.image_height * self.pix2m
        self.df.bounding_box_x1  = self.df.bounding_box_x1 * self.image_width * self.pix2m
        self.df.bounding_box_y1  = self.df.bounding_box_y1 * self.image_height * self.pix2m
    
    def calc_yaw_from_heading(self, df):
        """
        Calculate yaw angles from heading data in the input DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing trajectory data.

        Returns:
            pd.DataFrame: The input DataFrame with an additional 'yaw_rad' column containing the calculated yaw angles.
        """
        df_list = list()
        for i in range(int(df.segment.max())):
            df_temp = df.loc[df.segment == i,:]
            # get change in x an y position 
            diff_x = df_temp.center_of_mass_x.diff()
            diff_y = df_temp.center_of_mass_y.diff()
            # first valkue becomes nan. Overwrite with first real value
            diff_x.iloc[0] =diff_x.iloc[1]
            diff_y.iloc[0] =diff_y.iloc[1]
            yaw = np.arctan2(diff_y, diff_x)
            # Unwrap the phase angles to avoid jumps when moving over the pi/2 position
            unwrapped_yaw = np.unwrap(yaw)
            # save results
            df_temp['yaw_rad'] = unwrapped_yaw
            df_list.append(df_temp)
        return pd.concat(df_list)
    

    def apply_low_pass_filter(self,df):
        """
        Apply a Gaussian low-pass filter to the numeric columns in the input DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing trajectory data.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        # Find the unique segment numbers
        unique_segments = df['segment'].unique()

        # Initialize an empty DataFrame to store the filtered data
        filtered_df = pd.DataFrame()

        # Apply the Gaussian filter to each numeric column in the DataFrame for each segment separately
        for segment in unique_segments:
            segment_df = df[df['segment'] == segment].copy()
      
            for column in segment_df.select_dtypes(include=[np.number]).columns:
                if column != 'segment':
                    segment_df[column] = gaussian_filter1d(segment_df[column], self.filt_sigma)

            # Append the filtered segment data to the filtered_df DataFrame
            filtered_df = filtered_df.append(segment_df)

        return filtered_df

        
    def calc_speeds(self,df):
        """
        Calculate translational and rotational speeds from position and yaw data in the input DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame containing trajectory data.

        Returns:
            pd.DataFrame: The input DataFrame with additional 'trans_speed_mPs' and 'rot_speed_mPs' columns containing the calculated speeds.
        """
        df_list = list()
        for i in range(int(df.segment.max())):
            df_temp = df.loc[df.segment == i,:]
            # Calculate the norm of the difference vector
            df_temp['trans_speed_mPs'] = np.sqrt(df_temp.center_of_mass_x.diff()**2 + df_temp.center_of_mass_x.diff()**2)*self.frame_rate
            df_temp['rot_speed_degPs'] = np.rad2deg(df_temp.yaw_rad.diff())*self.frame_rate
            df_list.append(df_temp)
        return pd.concat(df_list)


    def main(self):
        """
        Main function to process the input DataFrame and calculate the required values.

        Returns:
            pd.DataFrame: The processed DataFrame with interpolated, filtered, and calculated data.
        """
        self.rel_coord_to_m()
        segments = self.get_trajectory_segments()
        df_interp = self.interpolate_all_segments(segments)
        df_interp = self.apply_low_pass_filter(df_interp)
        df_interp = self.calc_yaw_from_heading(df_interp)
        df_interp = self.calc_speeds(df_interp)
        df_saccades = self.find_saccades(df_interp,180)

        return df_interp,df_saccades
        

    def plot_quiver(self, df, x_col='center_of_mass_x', y_col='center_of_mass_y', yaw_col='yaw_rad',step=2):
        """
        Create a quiver plot of the input DataFrame's yaw angles.

        Args:
            df (pd.DataFrame): The input DataFrame containing trajectory data.
            x_col (str, optional): The name of the column containing the x positions. Default is 'center_of_mass_x'.
            y_col (str, optional): The name of the column containing the y positions. Default is 'center_of_mass_y'.
            yaw_col (str, optional): The name of the column containing the yaw angles. Default is 'yaw'.
            step (int, optional): The step size for selecting data points to display arrows. Default is 2.
        """
        # Extract x, y, and yaw data from the DataFrame
        x   = df[x_col]
        y   = df[y_col]
        yaw = df[yaw_col]

        # Compute the quiver vectors (u, v) from the yaw angles
        u = np.cos(yaw)
        v = np.sin(yaw)

        # Create the quiver plot
        fig, ax = plt.subplots()
        ax.quiver(x[::step], y[::step], u[::step], v[::step], angles='xy', scale_units='xy', scale=10, width =0.0025, color='lightgray')
        ax.plot(x,y,'k')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title('Quiver Plot of Yaw Angles')
        plt.axis('equal')

        return fig
    

    def find_saccades(self, df_interp, threshold):
        """
        Finds the peaks in the signal with a given prominence threshold.

        Parameters
        ----------
        threshold : float
            The prominence threshold for detecting peaks.

        Returns
        -------
        saccade_df : pd.DataFrame
            A DataFrame containing the saccade times, start and stop times, and amplitudes.
        """
        saccade_df_list = list()
        for i in range(int(df_interp.segment.max())):
            df_temp = df_interp.loc[df_interp.segment == i,:]

            peak_pos, peak_data = find_peaks(df_temp['rot_speed_degPs'], prominence=threshold)
            peak_pos_time   = (df_interp.index[peak_pos]/self.frame_rate).to_numpy()
            peak_start_time = (df_interp.index[peak_data['left_bases']]/self.frame_rate).to_numpy()
            peak_end_time   = (df_interp.index[peak_data['right_bases']]/self.frame_rate).to_numpy()
            peak_duration   = peak_end_time - peak_start_time
            peak_amplitude = peak_data['prominences']
            saccade_temp_df = pd.DataFrame(np.stack([peak_pos_time, peak_start_time, peak_end_time, peak_amplitude, peak_duration]).T,
                    columns=['saccade_peak_s', 'saccade_start_s', 'saccade_stop_s', 'amplitude_degPsec', 'saccade_duration_s'])
            saccade_temp_df['segment'] = i
            saccade_df_list.append(saccade_temp_df)
        saccade_df = pd.concat(saccade_df_list)
        saccade_df.reset_index(drop=True,inplace=True)
        return  saccade_df

    




pix2m      = np.array([0.97/124.6,0.3/66,0.4/76.2]).mean()
im_height  = 788
im_width   = 1402
frame_rate = 30


df = pd.read_hdf('/media/anne/Samsung_T5/PHD/penguins/Gentoo/Gentoo_02-03-2021_Dato1.h5','trace')

tp = TrajectoryProcessor(df,im_width,im_height,pix2m,frame_rate)
df_interp,df_saccades = tp.main()
df_temp = df_interp.loc[df_interp.segment == 10,:]
fig = tp.plot_quiver(df_temp)
plt.show()
df_temp.rot_speed_degPs.plot()
plt.show()




'''To extract only the biological relevant saccades detected by the peak finder,
we here define two values as biological limits for a saccade
1 = duration < 1s (30 frames)
2 = amplitude in degPsec < 300
'''

df_realSaccades = df_saccades.drop(df_saccades[(df_saccades.amplitude_degPsec > 300)|(df_saccades.saccade_duration_s > 1)].index)

"""for each saccade in df_realSaccades we need to read out the yaw velocity and yaw angle stored in the df_interp.index"""

for i, row in df_realSaccades.interrows():

    saccade_data = df_interp.loc[df_interp['segment'] == int(df_realSaccades.iloc[[row]].segment)] #take the data from df.interp for segment 
    saccade_data = saccade_data.dropna()
    saccadePeak  = saccade_data.loc[saccade_data['rot_speed_degPs'] == float(df_realSaccades.iloc[[row]].amplitude_degPsec)] #find the frame with the saccadic peak
    oneSecSaccade = saccade_data.loc[np.arange(saccadePeak.index.values[0]-5,saccadePeak.index.values[0]+5)] # create a new dataframe sourrounding the saccadic peak (in total 30frames) currently using 5 as 15 is extending the Dataset
    
    oneSecSaccade['yaw_rad'] = oneSecSaccade.yaw_rad - oneSecSaccade.iloc[[0,1]].yaw_rad.mean() #normalize yaw to basement yaw before start of saccade
    oneSecSaccade.yaw_deg = np.rad2deg(oneSecSaccade.yaw_rad)
    oneSecSaccade.to_csv("/media/anne/Samsung_T5/PHD/saccadicData.csv",index=False) # still needs to be automated for the for loop

    oneSecSaccade.rot_speed_degPs.plot()
    plt.show()
    oneSecSaccade.yaw_deg.plot()
    plt.show()

#######
# here is the code that can be ran in ipython that works already. the for loops still gives to many error since it cant find the saccade peaks
#######

row = 0
saccade_data = df_interp.loc[df_interp['segment'] == int(df_realSaccades.iloc[[row]].segment)] #take the data from df.interp for segment 
saccade_data = saccade_data.dropna()
saccadePeak  = saccade_data.loc[saccade_data['rot_speed_degPs'] == float(df_realSaccades.iloc[[row]].amplitude_degPsec)] #find the frame with the saccadic peak
oneSecSaccade = saccade_data.loc[np.arange(saccadePeak.index.values[0]-5,saccadePeak.index.values[0]+5)] # create a new dataframe sourrounding the saccadic peak (in total 30frames) currently using 5 as 15 is extending the Dataset
    
oneSecSaccade['yaw_rad'] = oneSecSaccade.yaw_rad - oneSecSaccade.iloc[[0,1]].yaw_rad.mean() #normalize yaw to basement yaw before start of saccade
oneSecSaccade.yaw_deg = np.rad2deg(oneSecSaccade.yaw_rad)
oneSecSaccade.to_csv("/media/anne/Samsung_T5/PHD/saccadicData.csv",index=False) # still needs to be automated for the for loop

oneSecSaccade.rot_speed_degPs.plot()
plt.show()
oneSecSaccade.yaw_deg.plot()
plt.show()