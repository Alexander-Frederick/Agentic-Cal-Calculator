"""
Data Manager module for the Calorie Tracker application
Handles all spreadsheet operations and data persistence
"""

import pandas as pd
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, filename="calorie_data.xlsx"):
        """Initialize the data manager with the specified filename"""
        self.filename = filename
        self.filepath = os.path.join(os.getcwd(), self.filename)
        self.columns = ['Date', 'Calories', 'Protein', 'Carbs', 'Fat', 'Weight', 'Calorie_Goal']
        
        # Ensure the data file exists
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create the data file if it doesn't exist"""
        if not os.path.exists(self.filepath):
            try:
                # Create empty dataframe with proper columns
                df = pd.DataFrame(columns=self.columns)
                df.to_excel(self.filepath, index=False)
                logger.info(f"Created new data file: {self.filepath}")
            except Exception as e:
                logger.error(f"Failed to create data file: {str(e)}")
                raise
    
    def load_data(self):
        """Load data from the Excel file"""
        try:
            if os.path.exists(self.filepath):
                df = pd.read_excel(self.filepath)
                
                # Ensure all required columns exist
                for col in self.columns:
                    if col not in df.columns:
                        df[col] = None
                
                # Ensure Date column is string format
                if 'Date' in df.columns:
                    df['Date'] = df['Date'].astype(str)
                
                return df
            else:
                # Create empty dataframe if file doesn't exist
                return pd.DataFrame(columns=self.columns)
                
        except Exception as e:
            logger.error(f"Failed to load data: {str(e)}")
            # Return empty dataframe on error
            return pd.DataFrame(columns=self.columns)
    
    def save_data(self, df):
        """Save dataframe to Excel file"""
        try:
            # Ensure Date column is properly formatted
            if 'Date' in df.columns:
                df['Date'] = df['Date'].astype(str)
            
            # Save to Excel
            df.to_excel(self.filepath, index=False)
            logger.info(f"Data saved successfully to {self.filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save data: {str(e)}")
            return False
    
    def get_all_data(self):
        """Get all data from the spreadsheet"""
        return self.load_data()
    
    def get_day_data(self, date_str):
        """Get data for a specific date"""
        try:
            df = self.load_data()
            
            if df.empty:
                return None
            
            # Filter for the specific date
            day_data = df[df['Date'] == date_str]
            
            if day_data.empty:
                return None
            
            # Return the data as a dictionary
            return day_data.iloc[0].to_dict()
            
        except Exception as e:
            logger.error(f"Failed to get day data: {str(e)}")
            return None
    
    def update_day_data(self, date_str, updates):
        """Update data for a specific date"""
        try:
            df = self.load_data()
            
            # Check if date already exists
            existing_row = df[df['Date'] == date_str]
            
            if existing_row.empty:
                # Create new row for this date
                new_row = {col: 0 if col != 'Date' else date_str for col in self.columns}
                new_row['Date'] = date_str
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                row_index = len(df) - 1
            else:
                row_index = existing_row.index[0]
            
            # Apply updates
            for field, value in updates.items():
                if field == 'calories':
                    # Add to existing calories
                    current = df.at[row_index, 'Calories'] if not pd.isna(df.at[row_index, 'Calories']) else 0
                    df.at[row_index, 'Calories'] = current + value
                    
                elif field == 'protein':
                    # Add to existing protein
                    current = df.at[row_index, 'Protein'] if not pd.isna(df.at[row_index, 'Protein']) else 0
                    df.at[row_index, 'Protein'] = current + value
                    
                elif field == 'carbs':
                    # Add to existing carbs
                    current = df.at[row_index, 'Carbs'] if not pd.isna(df.at[row_index, 'Carbs']) else 0
                    df.at[row_index, 'Carbs'] = current + value
                    
                elif field == 'fat':
                    # Add to existing fat
                    current = df.at[row_index, 'Fat'] if not pd.isna(df.at[row_index, 'Fat']) else 0
                    df.at[row_index, 'Fat'] = current + value
                    
                elif field == 'weight':
                    # Set weight (not additive)
                    df.at[row_index, 'Weight'] = value
                    
                elif field == 'goal':
                    # Set calorie goal (not additive)
                    df.at[row_index, 'Calorie_Goal'] = value
            
            # Save the updated data
            return self.save_data(df)
            
        except Exception as e:
            logger.error(f"Failed to update day data: {str(e)}")
            return False
    
    def get_date_range_data(self, start_date, end_date):
        """Get data for a specific date range"""
        try:
            df = self.load_data()
            
            if df.empty:
                return pd.DataFrame()
            
            # Convert dates to datetime for comparison
            df['Date_dt'] = pd.to_datetime(df['Date'])
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # Filter data
            filtered_df = df[(df['Date_dt'] >= start_dt) & (df['Date_dt'] <= end_dt)]
            
            # Remove the temporary datetime column
            filtered_df = filtered_df.drop('Date_dt', axis=1)
            
            return filtered_df.sort_values('Date')
            
        except Exception as e:
            logger.error(f"Failed to get date range data: {str(e)}")
            return pd.DataFrame()
    
    def get_recent_data(self, days=30):
        """Get data for the last N days"""
        try:
            from datetime import datetime, timedelta
            
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days-1)
            
            return self.get_date_range_data(start_date.strftime('%Y-%m-%d'), 
                                          end_date.strftime('%Y-%m-%d'))
            
        except Exception as e:
            logger.error(f"Failed to get recent data: {str(e)}")
            return pd.DataFrame()
    
    def delete_day_data(self, date_str):
        """Delete data for a specific date"""
        try:
            df = self.load_data()
            
            # Remove the row with the specified date
            df = df[df['Date'] != date_str]
            
            return self.save_data(df)
            
        except Exception as e:
            logger.error(f"Failed to delete day data: {str(e)}")
            return False
    
    def get_summary_stats(self, days=30):
        """Get summary statistics for the last N days"""
        try:
            df = self.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Calculate statistics
            stats = {
                'avg_calories': df['Calories'].mean() if not df['Calories'].isna().all() else 0,
                'avg_protein': df['Protein'].mean() if not df['Protein'].isna().all() else 0,
                'avg_carbs': df['Carbs'].mean() if not df['Carbs'].isna().all() else 0,
                'avg_fat': df['Fat'].mean() if not df['Fat'].isna().all() else 0,
                'avg_weight': df['Weight'].mean() if not df['Weight'].isna().all() else 0,
                'weight_change': None,
                'goal_achievement_rate': 0,
                'days_with_data': len(df[df['Calories'] > 0])
            }
            
            # Calculate weight change if we have weight data
            weight_data = df.dropna(subset=['Weight'])
            if len(weight_data) >= 2:
                first_weight = weight_data.iloc[0]['Weight']
                last_weight = weight_data.iloc[-1]['Weight']
                stats['weight_change'] = last_weight - first_weight
            
            # Calculate goal achievement rate
            goal_data = df.dropna(subset=['Calories', 'Calorie_Goal'])
            if not goal_data.empty:
                goals_met = len(goal_data[goal_data['Calories'] >= goal_data['Calorie_Goal']])
                stats['goal_achievement_rate'] = (goals_met / len(goal_data)) * 100
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get summary stats: {str(e)}")
            return None
    
    def backup_data(self, backup_filename=None):
        """Create a backup of the data file"""
        try:
            if backup_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"calorie_data_backup_{timestamp}.xlsx"
            
            backup_path = os.path.join(os.getcwd(), backup_filename)
            
            # Copy the current data file
            import shutil
            shutil.copy2(self.filepath, backup_path)
            
            logger.info(f"Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            return None