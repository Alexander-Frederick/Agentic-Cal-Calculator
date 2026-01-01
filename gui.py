"""
GUI module for the Calorie Tracker application
Handles all user interface components and interactions
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_manager import DataManager
from visualizer import Visualizer


class CalorieTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.data_manager = DataManager()
        self.visualizer = Visualizer(self.data_manager)
        
        # Initialize the GUI
        self.setup_window()
        self.create_widgets()
        self.refresh_display()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Calorie Tracker")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_entry_tab()
        self.create_view_tab()
        self.create_charts_tab()
    
    def create_entry_tab(self):
        """Create the data entry tab"""
        entry_frame = ttk.Frame(self.notebook)
        self.notebook.add(entry_frame, text="Data Entry")
        
        # Date selection frame
        date_frame = ttk.LabelFrame(entry_frame, text="Date Selection", padding="10")
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(date_frame, text="Today", command=self.set_today).pack(side=tk.LEFT, padx=5)
        ttk.Button(date_frame, text="Load Day", command=self.load_selected_day).pack(side=tk.LEFT, padx=5)
        
        # Current day info frame
        info_frame = ttk.LabelFrame(entry_frame, text="Current Day Summary", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="No data for selected date", font=('Arial', 10))
        self.info_label.pack()
        
        # Data entry frame
        entry_data_frame = ttk.LabelFrame(entry_frame, text="Add/Update Data", padding="10")
        entry_data_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create entry fields
        fields = [
            ("Calories to add:", "calories"),
            ("Protein (g) to add:", "protein"),
            ("Carbs (g) to add:", "carbs"),
            ("Fat (g) to add:", "fat"),
            ("Weight (set):", "weight"),
            ("Calorie Goal (set):", "goal")
        ]
        
        self.entry_vars = {}
        
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 3
            
            ttk.Label(entry_data_frame, text=label).grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar()
            self.entry_vars[key] = var
            entry = ttk.Entry(entry_data_frame, textvariable=var, width=10)
            entry.grid(row=row, column=col+1, padx=5, pady=2)
        
        # Buttons frame
        button_frame = ttk.Frame(entry_data_frame)
        button_frame.grid(row=3, column=0, columnspan=6, pady=10)
        
        ttk.Button(button_frame, text="Update Data", command=self.update_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
    
    def create_view_tab(self):
        """Create the data viewing tab"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="View Data")
        
        # Controls frame
        controls_frame = ttk.Frame(view_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Refresh Data", command=self.refresh_display).pack(side=tk.LEFT, padx=5)
        
        # Treeview for data display
        columns = ("Date", "Calories", "Protein", "Carbs", "Fat", "Weight", "Goal")
        self.tree = ttk.Treeview(view_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(view_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        tree_frame = ttk.Frame(view_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_charts_tab(self):
        """Create the charts and visualization tab"""
        charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(charts_frame, text="Charts")
        
        # Controls frame
        chart_controls = ttk.Frame(charts_frame)
        chart_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(chart_controls, text="Days to show:").pack(side=tk.LEFT)
        self.days_var = tk.StringVar(value="30")
        days_combo = ttk.Combobox(chart_controls, textvariable=self.days_var, values=["7", "14", "30", "60", "90"], width=5)
        days_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(chart_controls, text="Update Charts", command=self.update_charts).pack(side=tk.LEFT, padx=5)
        
        # Chart selection
        ttk.Label(chart_controls, text="Chart:").pack(side=tk.LEFT, padx=(20, 5))
        self.chart_var = tk.StringVar(value="Weight")
        chart_combo = ttk.Combobox(chart_controls, textvariable=self.chart_var, 
                                  values=["Weight", "Calories", "Macros", "Goal vs Actual"], width=15)
        chart_combo.pack(side=tk.LEFT, padx=5)
        chart_combo.bind('<<ComboboxSelected>>', lambda e: self.update_charts())
        
        # Chart frame
        self.chart_frame = ttk.Frame(charts_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def set_today(self):
        """Set the date to today"""
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.load_selected_day()
    
    def load_selected_day(self):
        """Load data for the selected day"""
        try:
            date_str = self.date_var.get()
            datetime.strptime(date_str, "%Y-%m-%d")  # Validate date format
            self.refresh_current_day_info()
        except ValueError:
            messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format")
    
    def refresh_current_day_info(self):
        """Refresh the current day information display"""
        date_str = self.date_var.get()
        data = self.data_manager.get_day_data(date_str)
        
        if data is not None:
            info_text = f"Date: {date_str}\n"
            info_text += f"Calories: {data.get('Calories', 0)}\n"
            info_text += f"Protein: {data.get('Protein', 0)}g | "
            info_text += f"Carbs: {data.get('Carbs', 0)}g | "
            info_text += f"Fat: {data.get('Fat', 0)}g\n"
            info_text += f"Weight: {data.get('Weight', 'Not set')}"
            if data.get('Weight') != 'Not set' and data.get('Weight'):
                info_text += " lbs"
            info_text += f" | Goal: {data.get('Calorie_Goal', 'Not set')}"
        else:
            info_text = f"Date: {date_str}\nNo data entered for this date"
        
        self.info_label.config(text=info_text)
    
    def update_data(self):
        """Update data for the selected date"""
        try:
            date_str = self.date_var.get()
            
            # Get values from entry fields
            updates = {}
            
            # Handle additive fields (calories, macros)
            for field in ['calories', 'protein', 'carbs', 'fat']:
                value = self.entry_vars[field].get().strip()
                if value:
                    try:
                        updates[field] = float(value)
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid {field} value: {value}")
                        return
            
            # Handle set fields (weight, goal)
            for field in ['weight', 'goal']:
                value = self.entry_vars[field].get().strip()
                if value:
                    try:
                        updates[field] = float(value)
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid {field} value: {value}")
                        return
            
            if not updates:
                messagebox.showwarning("Warning", "No data to update")
                return
            
            # Update the data
            success = self.data_manager.update_day_data(date_str, updates)
            
            if success:
                messagebox.showinfo("Success", "Data updated successfully!")
                self.clear_fields()
                self.refresh_current_day_info()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Failed to update data")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def clear_fields(self):
        """Clear all entry fields"""
        for var in self.entry_vars.values():
            var.set("")
    
    def refresh_display(self):
        """Refresh the data display"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load all data
        df = self.data_manager.get_all_data()
        
        if df is not None and not df.empty:
            # Sort by date (newest first)
            df = df.sort_values('Date', ascending=False)
            
            # Add data to treeview
            for _, row in df.iterrows():
                values = (
                    row['Date'],
                    f"{row['Calories']:.0f}" if not pd.isna(row['Calories']) else "0",
                    f"{row['Protein']:.1f}" if not pd.isna(row['Protein']) else "0.0",
                    f"{row['Carbs']:.1f}" if not pd.isna(row['Carbs']) else "0.0",
                    f"{row['Fat']:.1f}" if not pd.isna(row['Fat']) else "0.0",
                    f"{row['Weight']:.1f}" if not pd.isna(row['Weight']) else "",
                    f"{row['Calorie_Goal']:.0f}" if not pd.isna(row['Calorie_Goal']) else ""
                )
                self.tree.insert("", tk.END, values=values)
        
        # Also refresh current day info
        self.refresh_current_day_info()
    
    def update_charts(self):
        """Update the charts display"""
        try:
            days = int(self.days_var.get())
            chart_type = self.chart_var.get()
            
            # Clear existing chart
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            # Create new chart based on selection
            if chart_type == "Weight":
                fig = self.visualizer.create_weight_chart(days)
            elif chart_type == "Calories":
                fig = self.visualizer.create_calorie_chart(days)
            elif chart_type == "Macros":
                fig = self.visualizer.create_macro_chart(days)
            elif chart_type == "Goal vs Actual":
                fig = self.visualizer.create_goal_comparison_chart(days)
            else:
                return
            
            if fig:
                # Embed the chart in the GUI
                canvas = FigureCanvasTkAgg(fig, self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                ttk.Label(self.chart_frame, text="No data available for the selected period", 
                         font=('Arial', 12)).pack(expand=True)
                
        except Exception as e:
            messagebox.showerror("Chart Error", f"Failed to create chart: {str(e)}")


# Import pandas here to avoid circular imports
import pandas as pd