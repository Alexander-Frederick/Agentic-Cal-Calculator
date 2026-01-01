# Agentic Coding Practice

This project was meant to test the limitations and uses of Agentic Coding.

## Thoughts

The agent was able to complete the code easily. I picked this project because I thought it would be simple enough and I'd get some value out of it.
There were some oddities with getting the code to initally run. Such as, putting all the code into a text file that I would have to sift through. Instead, I put the time
into learning more about how to Agentically Code that's where I heard about tool use. Using Tool made it to where the AI could create the files on my machine itselft without my intervention.
Overall this first iteration of the project took about 2 hours to make. With most of those two hours learning the intial steps.

## Future Use

I will be using agentic coding in the future, especially for prototyping.

# Calorie Tracker Desktop Application

A standalone desktop application for tracking daily calorie intake, macro nutrients, weight, and calorie goals. All data is stored in a spreadsheet format and includes visualization capabilities.

## Features

### ✅ Core Features Implemented:

- **Data Tracking**: Track calories, protein, carbs, fat, weight, and calorie goals for each day
- **Incremental Updates**: Add calories and macros to existing daily totals
- **Data Persistence**: All data stored in Excel format (`calorie_data.xlsx`)
- **Data Visualization**: Multiple chart types for tracking progress over time
- **Date Selection**: Add data for any date (current or historical)
- **Auto File Creation**: Automatically creates data file if it doesn't exist

### 📊 Visualization Features:

- **Weight Progress Chart**: Line chart showing weight changes over time
- **Calorie Intake Chart**: Bar chart with color coding and average line
- **Macro Nutrients Chart**: Stacked area chart showing protein, carbs, and fat
- **Goal vs Actual Chart**: Comparison chart with achievement rate
- **Configurable Time Periods**: View data for 7, 14, 30, 60, or 90 days

### 💾 Data Management:

- **Excel Storage**: Data stored in `calorie_data.xlsx` in the application directory
- **Data Validation**: Input validation for all numeric fields
- **Error Handling**: Graceful handling of missing or corrupted data
- **Backup Functionality**: Built-in data backup capabilities

## Installation & Setup

### Option 1: Run the Executable (Recommended)

1. Download the application files
2. Run the build script to create an executable:
   ```bash
   python build.py
   ```
3. Choose option 1 for full executable build
4. Run the executable from the `dist` folder: `CalorieTracker.exe`

### Option 2: Run with Python

1. Ensure Python 3.7+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Option 3: Simple Runner

1. Run the build script:
   ```bash
   python build.py
   ```
2. Choose option 2 for simple build
3. Use the generated batch/shell file to run the application

## Usage Guide

### Data Entry Tab

1. **Select Date**: Use the date field to select which day you want to update (defaults to today)
2. **View Current Data**: See existing totals for the selected date
3. **Add Data**:
   - **Calories/Macros**: Enter amounts to ADD to existing totals
   - **Weight**: Enter weight to SET (replaces previous value)
   - **Goal**: Enter calorie goal to SET (replaces previous value)
4. **Update**: Click "Update Data" to save changes

### View Data Tab

- **Data Table**: View all entered data in chronological order
- **Refresh**: Update the display with latest data

### Charts Tab

1. **Select Time Period**: Choose how many days to display (7-90 days)
2. **Choose Chart Type**:
   - **Weight**: Shows weight progression with trend line
   - **Calories**: Daily calorie intake with color coding
   - **Macros**: Stacked area chart of protein, carbs, and fat
   - **Goal vs Actual**: Compare actual calories to goals
3. **Update Charts**: Refresh charts with current selection

## Data Structure

The application stores data in an Excel file (`calorie_data.xlsx`) with the following columns:

| Column | Description | Type |
|--------|-------------|------|
| Date | Date of entry (YYYY-MM-DD) | String |
| Calories | Total calories for the day | Number |
| Protein | Protein in grams | Number |
| Carbs | Carbohydrates in grams | Number |
| Fat | Fat in grams | Number |
| Weight | Body weight (lbs) | Number |
| Calorie_Goal | Target calories for the day | Number |

## File Locations

- **Data File**: `calorie_data.xlsx` (created in application directory)
- **Application Files**: All Python files in the same directory
- **Executable**: `dist/CalorieTracker.exe` (after building)

## Tips for Use

### Quick Daily Entry
1. Open application
2. Data entry defaults to today's date
3. Add your meal calories and macros throughout the day
4. Set your weight and goal as needed

### Data Tracking Tips
- **Calories**: Add individual meals (e.g., breakfast: 300, lunch: 450)
- **Macros**: Add macros for each meal to get daily totals
- **Weight**: Enter once per day for consistent tracking
- **Goals**: Set realistic daily calorie targets

### Visualization Tips
- Use 7-day view for weekly progress
- Use 30-day view for monthly trends
- Weight chart shows trend lines for long-term progress
- Goal vs Actual helps track adherence to calorie targets

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure all required files are present
- Try running `python main.py` directly
- Check that dependencies are installed

**Data not saving:**
- Check file permissions in application directory
- Ensure `calorie_data.xlsx` is not open in Excel
- Try running application as administrator

**Charts not displaying:**
- Ensure matplotlib is installed: `pip install matplotlib`
- Check that you have data for the selected time period
- Try reducing the time period (fewer days)

**Missing data file:**
- Application will automatically create `calorie_data.xlsx`
- If issues persist, manually create an empty Excel file with the column headers

### Error Messages

- **"Invalid date format"**: Use YYYY-MM-DD format (e.g., 2024-01-15)
- **"Invalid numeric value"**: Enter only numbers for calories, macros, weight
- **"No data available"**: Add some data before viewing charts
- **"Failed to save data"**: Check file permissions and disk space

## Technical Details

### Dependencies
- Python 3.7+
- pandas 2.0.3
- matplotlib 3.7.2
- openpyxl 3.1.2
- numpy 1.24.3
- tkinter (included with Python)

### Architecture
- **main.py**: Application entry point
- **gui.py**: User interface components
- **data_manager.py**: Data storage and retrieval
- **visualizer.py**: Chart creation and visualization
- **build.py**: Executable creation script

### Data Safety
- Data is automatically saved after each update
- Excel format allows manual editing if needed
- Built-in backup functionality available
- No data is stored online or transmitted

## License

This application is provided as-is for personal use. Feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all files are present and requirements are installed
3. Try running with Python directly: `python main.py`

---

**Version**: 1.0  
**Created**: 2025 
**Platform**: Windows, macOS, Linux (Python required)
