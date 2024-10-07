import pandas as pd
import os


DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'security-controls.xlsx')

class SecurityControl:
    def __init__(self):
        self.data = self.load_data()

    def load_data():
        try:
        
            df = pd.read_excel(DATA_FILE_PATH)

        
            df['App Name'] = ['App' + str(i + 1) for i in range(len(df))]

        
            df.rename(columns={
                'Security Level': 'Type',
                'Level': 'Level',
                'Cloud Adoption Framework (CAF) capability': 'Control Areas',
                'Layer 2 Controls (Generic)': 'Layer 2 Controls (Generic)',
                'Controls': 'AWS Controls',
                'AWS-Sub-Controls':'AWS Sub-Controls'
            }, inplace=True)
            print(df.head())
            return df
        except FileNotFoundError:
            print("Data file not found at path:", DATA_FILE_PATH)
            return pd.DataFrame()  
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    def get_essential_controls(self):
        
        if 'Control Type' in self.data.columns:
            return self.data[self.data['Control Type'] == 'Essential'].to_dict(orient='records')
        return []

    def get_all_controls(self):
        
        return self.data.to_dict(orient='records')

    def filter_by_security_level(self, search_query):
        
        search_query = search_query.lower()
        if 'Security Level' in self.data.columns:
            filtered_controls = self.data[self.data['Security Level'].str.lower().str.contains(search_query)]
            return filtered_controls.to_dict(orient='records')
        return []

    def add_control(self, new_control):
        
        new_data = self.data.append(new_control, ignore_index=True)
        self.data = new_data
        
        self.save_data()

    def save_data(self):
        
        self.data.to_excel(DATA_FILE_PATH, index=False)

