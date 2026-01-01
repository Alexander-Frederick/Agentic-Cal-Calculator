"""
Configuration file for the Calorie Tracker application
Contains application settings and constants
"""

import os
from datetime import datetime

# Application Information
APP_NAME = "Calorie Tracker"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# File Settings
DEFAULT_DATA_FILENAME = "calorie_data.xlsx"
BACKUP_PREFIX = "calorie_data_backup"

# Data Validation Settings
MIN_CALORIES = 0
MAX_CALORIES = 10000
MIN_MACROS = 0
MAX_MACROS = 1000
MIN_WEIGHT = 50  # pounds
MAX_WEIGHT = 1000  # pounds
MIN_GOAL = 500
MAX_GOAL = 5000

# UI Settings
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
WINDOW_SIZE = "1000x700"
MIN_WINDOW_SIZE = (800, 600)

# Chart Settings
DEFAULT_CHART_DAYS = 30
CHART_FIGURE_SIZE = (10, 6)
CHART_DPI = 100

# Color Schemes
CHART_COLORS = {
    'protein': '#FF6B6B',     # Red
    'carbs': '#4ECDC4',       # Teal
    'fat': '#45B7D1',         # Blue
    'calories': '#96CEB4',    # Green
    'weight': '#FFEAA7',      # Yellow
    'goal': '#DDA0DD'         # Plum
}

# Date Format
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%m/%d/%Y"

# Default Values
DEFAULT_VALUES = {
    'calories': 0,
    'protein': 0.0,
    'carbs': 0.0,
    'fat': 0.0,
    'weight': None,
    'calorie_goal': None
}

# Excel Column Names
EXCEL_COLUMNS = [
    'Date',
    'Calories',
    'Protein',
    'Carbs',
    'Fat',
    'Weight',
    'Calorie_Goal'
]

# Chart Types
CHART_TYPES = [
    "Weight",
    "Calories", 
    "Macros",
    "Goal vs Actual"
]

# Time Periods for Charts
TIME_PERIODS = [7, 14, 30, 60, 90]

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_data_file_path():
    """Get the full path to the data file"""
    return os.path.join(os.getcwd(), DEFAULT_DATA_FILENAME)

def get_backup_filename():
    """Generate a backup filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{BACKUP_PREFIX}_{timestamp}.xlsx"

def validate_numeric_input(value, field_type):
    """Validate numeric input based on field type"""
    try:
        num_value = float(value)
        
        if field_type == 'calories':
            return MIN_CALORIES <= num_value <= MAX_CALORIES
        elif field_type in ['protein', 'carbs', 'fat']:
            return MIN_MACROS <= num_value <= MAX_MACROS
        elif field_type == 'weight':
            return MIN_WEIGHT <= num_value <= MAX_WEIGHT
        elif field_type == 'goal':
            return MIN_GOAL <= num_value <= MAX_GOAL
        
        return True
    except (ValueError, TypeError):
        return False

def get_validation_message(field_type):
    """Get validation error message for field type"""
    messages = {
        'calories': f"Calories must be between {MIN_CALORIES} and {MAX_CALORIES}",
        'protein': f"Protein must be between {MIN_MACROS}g and {MAX_MACROS}g",
        'carbs': f"Carbs must be between {MIN_MACROS}g and {MAX_MACROS}g",
        'fat': f"Fat must be between {MIN_MACROS}g and {MAX_MACROS}g",
        'weight': f"Weight must be between {MIN_WEIGHT} and {MAX_WEIGHT} lbs",
        'goal': f"Calorie goal must be between {MIN_GOAL} and {MAX_GOAL}"
    }
    return messages.get(field_type, "Invalid value")