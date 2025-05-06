
import pandas as pd

class Aggregator:

    def __init__(self, bucket_name, player_name, player_id):

        """
        Initialize the Aggregator class with the bucket name, player name, and player ID.
        This class is responsible for aggregating player statistics from various dataframes.

        Parameters:
            bucket_name (str): The name of the bucket where data is stored.
            player_name (str): The name of the player.
            player_id (str): The unique identifier for the player.
        """

        self.bucket_name = bucket_name
        self.player_name = player_name
        self.player_id = player_id
        
        # master dataframes
        self.batting_master = None
        self.bowling_master = None
        self.fielding_master = None
        self.allround_master = None
        self.info_master = None

        # dataframes to be concatenated
        self.batting_concat = None
        self.bowling_concat = None
        self.fielding_concat = None
        self.allround_concat = None
        self.info_concat = None

    def prepare_concat_df(self, tf_df, stat_type):

        """
        Prepare the concatenated dataframe for a specific statistic type.
        This function handles the renaming of columns and the addition of new columns
        to the dataframe based on the statistic type.

        Parameters:
            tf_df (pd.DataFrame): The transformed dataframe (downloaded from S3) to be concatenated.
            stat_type (str): The type of statistics ('batting', 'bowling', 'fielding', 'allround', 'personal_info').
        """

        concat_df = tf_df.copy() if tf_df is not None else pd.DataFrame()
        
        if stat_type != 'personal_info':
            concat_df['Player ID'] = self.player_id
            concat_df['Inns ID'] = (concat_df['Player ID'].astype(str)+"_"+
                        concat_df['Format'].astype(str)+
                        concat_df['Match ID'].astype(str)+"_"+
                        concat_df['Inns'].astype(str)
                       ) if tf_df is not None else None

        return concat_df
    
    def merge_df(self, master_df, concat_df, dedup_keys, sort_keys):

        """
        Merge the master dataframe with the concatenated dataframe.
        This function handles the merging of dataframes, dropping duplicates,
        and sorting the resulting dataframe based on specified keys.

        Parameters:
            master_df (pd.DataFrame): The master dataframe to merge with.
            concat_df (pd.DataFrame): The concatenated dataframe to merge.
            dedup_keys (list): The keys to use for dropping duplicates.
            sort_keys (list): The keys to use for sorting the resulting dataframe.
        """

        if concat_df.empty:
            pass
        elif master_df is None:
            master_df = concat_df
        else:
            master_df = pd.concat([master_df, concat_df])\
                            .drop_duplicates(subset=dedup_keys, keep='last')\
                            .sort_values(by=sort_keys)\
                            .reset_index(drop=True)

        return master_df
    

    def run_agg(self, stat_type):
        
        """
        Run the aggregation process for a specific statistic type.
        This function prepares the concatenated dataframe and merges it with the master dataframe.
        It also handles the case where the concatenated dataframe is empty.

        Parameters:
            stat_type (str): The type of statistics ('all','batting', 'bowling', 'fielding', 'allround', 'personal_info').
        """

        if stat_type in ['all','batting']:

            print("Aggregating batting stats...")
            concat_df = self.prepare_concat_df(self.batting_concat,"batting")
            self.batting_master = self.merge_df(self.batting_master, concat_df,
                                                dedup_keys=['Inns ID'],
                                                sort_keys=['Player ID', 'Start Date'])
            print("Batting stats aggregated.")
            
        if stat_type in ['all','bowling']:

            print("Aggregating bowling stats...")
            concat_df = self.prepare_concat_df(self.bowling_concat,"bowling")
            self.bowling_master = self.merge_df(self.bowling_master, concat_df,
                                                dedup_keys=['Inns ID'],
                                                sort_keys=['Player ID', 'Start Date'])
            print("Bowling stats aggregated.")

        if stat_type in ['all','fielding']:
            
            print("Aggregating fielding stats...")
            concat_df = self.prepare_concat_df(self.fielding_concat,"fielding")
            self.fielding_master = self.merge_df(self.fielding_master, concat_df,
                                                 dedup_keys=['Inns ID'],
                                                 sort_keys=['Player ID', 'Start Date'])
            print("Fielding stats aggregated.")     
        
        if stat_type in ['all','allround']:
            
            print("Aggregating allround stats...")
            concat_df = self.prepare_concat_df(self.allround_concat ,"allround")
            self.allround_master = self.merge_df(self.allround_master, concat_df,
                                                 dedup_keys=['Inns ID'],
                                                 sort_keys=['Player ID', 'Start Date'])
            print("Allround stats aggregated.")
        
        if stat_type in ['all','personal_info']:

            print("Aggregating personal info...")
            concat_df = self.prepare_concat_df(self.info_concat, "personal_info")
            self.info_master = self.merge_df(self.info_master, concat_df,
                                             dedup_keys=['Player ID'],
                                             sort_keys=['Player ID']) 
            print("Personal info aggregated.")

