import pandas as pd
import numpy as np

class TransformData:
    
    def __init__(self, player_name):
        self.player_name = player_name
        self.player_info = None
        self.battingstats = None
        self.bowlingstats = None
        self.allroundstats = None
        self.fieldingstats = None
        self.player_id = None
        self.player_url = None

    #transforming data

    def transform_data(self,df):
        
        #STEP 1: Replacing incorrect values. 
        repl_dict = {
            r'\*': '',       
            r'^DNB$': np.nan,  
            r'^TDNB$': np.nan, 
            r'^DNF$': np.nan,  
            r'^TDNF$': np.nan, 
            r'^-$': np.nan,    
            r'^sub$': np.nan   
                    }

        df = df.replace(repl_dict,regex=True)

        #STEP 2: Opposition column
        df['Format'] = df['Opposition'].str.extract(r'(^.*?)\sv\s')
        df['Opposition'] = df['Opposition'].str.extract(r'\sv\s(.*?$)')

        #STEP 3: Ground column
        ground_mapping = {
        "Colombo (SSC)": "Colombo",
        "Colombo (PSS)": "Colombo",
        "Colombo (RPS)": "Colombo",
        "Eden Gardens": "Kolkata",
        "Wankhede": "Mumbai",
        "Brabourne": "Mumbai",
        "Kingston": "Kingston Jamaica",
        "The Oval": "London",
        "Lord's": "London",
        "W.A.C.A": "Perth",
        "Dharamsala": "Dharamshala",
        "Hamilton": "Hamilton Waikato",
        "Fatullah": "Fatullah Dhaka",
        "Providence": "Providence Guyana",
        "Dubai (DICS)": "Dubai",
        "Chattogram": "Chattogram Chittagong"
        }

        df['Ground']=df['Ground'].replace(ground_mapping)
        df = df.rename(columns={'Ground':'Location'})

        #STEP 4: START DATE
        df['Start Date'] = df['Start Date'].astype('datetime64[ns]')

        #STEP 5: MATCH ID
        df['Match id']='#'+df['Match id'].str.extract(r'(\d+$)')
        df = df.rename(columns={'Match id':'Match ID'})

        return df
    
    def final_df(self, df, common_cols, custom_cols):

        dtype_mapping = {

                # Common Columns
                'Match ID': 'string',
                'Start Date': 'datetime64[ns]',
                'Format': 'string',
                'Inns': 'Int64',  # Allows NaN handling
                'Opposition': 'string',
                'Location': 'string',
                
                # Batting Columns
                'Pos': 'Int64',
                'Runs': 'Int64',
                'BF': 'Int64',
                '4s': 'Int64',
                '6s': 'Int64',
                'SR': 'float64',
                'Mins': 'Int64',
                'Dismissal': 'string',

                # Bowling Columns
                'Overs': 'float64',
                'Mdns': 'Int64',
                'Runs': 'Int64',
                'Wkts': 'Int64',
                'Econ': 'float64',

                # Fielding Columns
                'Dis': 'Int64',
                'Ct': 'Int64',

                # Allround Columns
                'Score': 'string',  # Could be runs or DNB, TDNB
                'Conc': 'Int64',
                'St': 'Int64'
            }

        if df is not None:
            df = self.transform_data(df)

            # Select the necessary columns
            df = df[common_cols[:-2] + custom_cols + common_cols[-2:]]

            # Apply type casting
            for col in df.columns:
                if col in dtype_mapping:
                    try:
                        df[col] = df[col].astype(dtype_mapping[col])
                    except Exception as e:
                        print(f"Data type casting failed for column {col}: {e}")

            return df


    def process_data(self,type="all"):

        common = ['Match ID','Start Date','Format','Inns','Opposition','Location']
        batcols = ['Pos','Runs','BF','4s','6s','SR','Mins','Dismissal']
        bowlcols = ['Pos','Overs','Mdns','Runs','Wkts','Econ']
        fieldcols = ['Dis','Ct']
        allroundcols = ['Score','Overs','Conc','Wkts','Ct','St']

        try:
        
            # Process batting stats
            if type == 'all' or type == 'batting':
                print(f"Processing {self.player_name}'s batting stats...")
                self.battingstats = self.final_df(self.battingstats, common, batcols)
                print(f"Batting stats processed successfully.")

            # Process bowling stats
            if type == 'all' or type == 'bowling':
                print(f"Processing {self.player_name}'s bowling stats...")
                self.bowlingstats = self.final_df(self.bowlingstats, common, bowlcols)
                print(f"Bowling stats processed successfully.")

            # Process fielding stats
            if type == 'all' or type == 'fielding':
                print(f"Processing {self.player_name}'s fielding stats...")
                self.fieldingstats = self.final_df(self.fieldingstats, common, fieldcols)
                print(f"Fielding stats processed successfully.")

            # Process allround stats
            if type == 'all' or type == 'allround':
                if self.player_info is not None and 'allround' in self.player_info['PLAYING ROLE'][0].lower():
                    print(f"Processing {self.player_name}'s all-round stats...")
                    self.allroundstats = self.final_df(self.allroundstats, common, allroundcols)
                    print(f"All-round stats processed successfully.")

           
        except Exception as e:
            print(f"Error in processing data for {self.player_name}: ", e)