"""
Visualizer module for the Calorie Tracker application
Handles all chart creation and data visualization
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import logging

# Configure matplotlib for GUI embedding
plt.style.use('default')
plt.rcParams.update({'font.size': 10})

logger = logging.getLogger(__name__)


class Visualizer:
    def __init__(self, data_manager):
        """Initialize the visualizer with a data manager"""
        self.data_manager = data_manager
    
    def create_weight_chart(self, days=30):
        """Create a weight progression chart"""
        try:
            # Get recent data
            df = self.data_manager.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Filter out rows without weight data
            weight_data = df.dropna(subset=['Weight'])
            
            if weight_data.empty:
                return None
            
            # Create the figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Convert dates to datetime
            dates = pd.to_datetime(weight_data['Date'])
            weights = weight_data['Weight']
            
            # Plot the line chart
            ax.plot(dates, weights, marker='o', linewidth=2, markersize=6, color='blue')
            
            # Customize the chart
            ax.set_title(f'Weight Progress - Last {days} Days', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Weight (lbs)', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Format x-axis dates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
            plt.xticks(rotation=45)
            
            # Add trend line if we have enough data points
            if len(weight_data) >= 3:
                x_numeric = np.arange(len(dates))
                z = np.polyfit(x_numeric, weights, 1)
                trend_line = np.poly1d(z)
                ax.plot(dates, trend_line(x_numeric), '--', alpha=0.7, color='red', label='Trend')
                ax.legend()
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create weight chart: {str(e)}")
            return None
    
    def create_calorie_chart(self, days=30):
        """Create a calorie intake chart"""
        try:
            # Get recent data
            df = self.data_manager.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Filter out rows without calorie data
            calorie_data = df[df['Calories'] > 0]
            
            if calorie_data.empty:
                return None
            
            # Create the figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Convert dates to datetime
            dates = pd.to_datetime(calorie_data['Date'])
            calories = calorie_data['Calories']
            
            # Create bar chart
            bars = ax.bar(dates, calories, alpha=0.7, color='green', width=0.8)
            
            # Customize the chart
            ax.set_title(f'Daily Calorie Intake - Last {days} Days', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Calories', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            
            # Format x-axis dates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
            plt.xticks(rotation=45)
            
            # Add average line
            avg_calories = calories.mean()
            ax.axhline(y=avg_calories, color='red', linestyle='--', alpha=0.7, 
                      label=f'Average: {avg_calories:.0f} cal')
            ax.legend()
            
            # Color bars based on calorie ranges
            for i, bar in enumerate(bars):
                cal_value = calories.iloc[i]
                if cal_value < 1200:
                    bar.set_color('red')
                elif cal_value > 2500:
                    bar.set_color('orange')
                else:
                    bar.set_color('green')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create calorie chart: {str(e)}")
            return None
    
    def create_macro_chart(self, days=30):
        """Create a macro nutrients chart"""
        try:
            # Get recent data
            df = self.data_manager.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Filter out rows without macro data
            macro_data = df.dropna(subset=['Protein', 'Carbs', 'Fat'], how='all')
            macro_data = macro_data[
                (macro_data['Protein'] > 0) | 
                (macro_data['Carbs'] > 0) | 
                (macro_data['Fat'] > 0)
            ]
            
            if macro_data.empty:
                return None
            
            # Create the figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Convert dates to datetime
            dates = pd.to_datetime(macro_data['Date'])
            
            # Plot stacked area chart
            ax.fill_between(dates, 0, macro_data['Protein'], alpha=0.7, color='red', label='Protein')
            ax.fill_between(dates, macro_data['Protein'], 
                           macro_data['Protein'] + macro_data['Carbs'], 
                           alpha=0.7, color='blue', label='Carbohydrates')
            ax.fill_between(dates, macro_data['Protein'] + macro_data['Carbs'],
                           macro_data['Protein'] + macro_data['Carbs'] + macro_data['Fat'],
                           alpha=0.7, color='orange', label='Fat')
            
            # Customize the chart
            ax.set_title(f'Macro Nutrients - Last {days} Days', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Grams', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            ax.legend()
            
            # Format x-axis dates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create macro chart: {str(e)}")
            return None
    
    def create_goal_comparison_chart(self, days=30):
        """Create a goal vs actual calorie comparison chart"""
        try:
            # Get recent data
            df = self.data_manager.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Filter out rows without both calories and goals
            goal_data = df.dropna(subset=['Calories', 'Calorie_Goal'])
            goal_data = goal_data[
                (goal_data['Calories'] > 0) & 
                (goal_data['Calorie_Goal'] > 0)
            ]
            
            if goal_data.empty:
                return None
            
            # Create the figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Convert dates to datetime
            dates = pd.to_datetime(goal_data['Date'])
            actual = goal_data['Calories']
            goals = goal_data['Calorie_Goal']
            
            # Create bar chart comparing actual vs goal
            x = np.arange(len(dates))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, actual, width, label='Actual Calories', alpha=0.8)
            bars2 = ax.bar(x + width/2, goals, width, label='Calorie Goal', alpha=0.8)
            
            # Color bars based on goal achievement
            for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                if actual.iloc[i] >= goals.iloc[i]:
                    bar1.set_color('green')  # Goal met
                else:
                    bar1.set_color('red')    # Goal not met
                bar2.set_color('blue')
            
            # Customize the chart
            ax.set_title(f'Calorie Goal vs Actual - Last {days} Days', fontsize=14, fontweight='bold')
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Calories', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            ax.legend()
            
            # Set x-axis labels
            date_labels = [date.strftime('%m/%d') for date in dates]
            ax.set_xticks(x)
            ax.set_xticklabels(date_labels, rotation=45)
            
            # Add success rate text
            success_rate = (actual >= goals).mean() * 100
            ax.text(0.02, 0.98, f'Goal Achievement Rate: {success_rate:.1f}%', 
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create goal comparison chart: {str(e)}")
            return None
    
    def create_weekly_summary_chart(self, weeks=4):
        """Create a weekly summary chart"""
        try:
            # Get recent data
            days = weeks * 7
            df = self.data_manager.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Convert date to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Group by week
            df['Week'] = df['Date'].dt.isocalendar().week
            df['Year'] = df['Date'].dt.year
            
            # Calculate weekly averages
            weekly_data = df.groupby(['Year', 'Week']).agg({
                'Calories': 'mean',
                'Weight': 'mean',
                'Protein': 'mean',
                'Carbs': 'mean',
                'Fat': 'mean'
            }).reset_index()
            
            if weekly_data.empty:
                return None
            
            # Create the figure with subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            
            weeks_labels = [f"W{w}" for w in weekly_data['Week']]
            
            # Weekly calories
            ax1.bar(weeks_labels, weekly_data['Calories'], color='green', alpha=0.7)
            ax1.set_title('Weekly Average Calories')
            ax1.set_ylabel('Calories')
            
            # Weekly weight
            if not weekly_data['Weight'].isna().all():
                ax2.plot(weeks_labels, weekly_data['Weight'], marker='o', color='blue')
                ax2.set_title('Weekly Average Weight')
                ax2.set_ylabel('Weight (lbs)')
            
            # Weekly protein
            ax3.bar(weeks_labels, weekly_data['Protein'], color='red', alpha=0.7)
            ax3.set_title('Weekly Average Protein')
            ax3.set_ylabel('Grams')
            
            # Weekly carbs vs fat
            ax4.bar(weeks_labels, weekly_data['Carbs'], alpha=0.7, label='Carbs')
            ax4.bar(weeks_labels, weekly_data['Fat'], alpha=0.7, bottom=weekly_data['Carbs'], label='Fat')
            ax4.set_title('Weekly Carbs vs Fat')
            ax4.set_ylabel('Grams')
            ax4.legend()
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create weekly summary chart: {str(e)}")
            return None
    
    def create_macro_pie_chart(self, days=7):
        """Create a pie chart showing macro nutrient distribution"""
        try:
            # Get recent data
            df = self.data_manager.get_recent_data(days)
            
            if df.empty:
                return None
            
            # Calculate total macros
            total_protein = df['Protein'].sum()
            total_carbs = df['Carbs'].sum()
            total_fat = df['Fat'].sum()
            
            if total_protein + total_carbs + total_fat == 0:
                return None
            
            # Create the figure
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Data for pie chart
            sizes = [total_protein, total_carbs, total_fat]
            labels = ['Protein', 'Carbohydrates', 'Fat']
            colors = ['red', 'blue', 'orange']
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                             shadow=True, startangle=90)
            
            # Customize the chart
            ax.set_title(f'Macro Nutrient Distribution - Last {days} Days', 
                        fontsize=14, fontweight='bold')
            
            # Add total grams to labels
            for i, (label, size) in enumerate(zip(labels, sizes)):
                texts[i].set_text(f'{label}\n({size:.1f}g)')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create macro pie chart: {str(e)}")
            return None