import os
import tkinter as tk
from tkinter import ttk, messagebox
import json
from flashcard_app import FlashcardApp  # Import your refactored FlashcardApp class

class FlashcardLauncher:
    """A launcher application for selecting and starting different flashcard sets."""
    
    def __init__(self):
        # Set up the main window
        self.window = tk.Tk()
        self.window.title("Flashcard Launcher")
        self.window.geometry("500x400")
        self.window.config(padx=20, pady=20)
        
        # Define the configuration file path
        self.config_file = "flashcard_sets.json"
        
        # Load available flashcard sets
        self.flashcard_sets = self.load_flashcard_sets()
        
        # Set up the UI
        self.setup_ui()
    
    def load_flashcard_sets(self):
        """Load the available flashcard sets from the configuration file."""
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create a default configuration
            default_sets = [
                {
                    "name": "Italian Vocabulary",
                    "data_file": "data/Italian_500 .csv",
                    "front_lang": "Italian",
                    "back_lang": "English"
                },
                {
                    "name": "Example Set (Add your own)",
                    "data_file": "data/your_file.csv",
                    "front_lang": "Front",
                    "back_lang": "Back"
                }
            ]
            
            # Save the default configuration
            with open(self.config_file, "w") as file:
                json.dump(default_sets, file, indent=4)
            
            return default_sets
    
    def save_flashcard_sets(self):
        """Save the current flashcard sets to the configuration file."""
        with open(self.config_file, "w") as file:
            json.dump(self.flashcard_sets, file, indent=4)
    
    def setup_ui(self):
        """Set up the user interface."""
        # Add a title label
        title_label = tk.Label(
            self.window, 
            text="Flashcard Learning System", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Add a subtitle
        subtitle_label = tk.Label(
            self.window, 
            text="Select a flashcard set to study:", 
            font=("Arial", 12)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Create a frame for the listbox and scrollbar
        list_frame = tk.Frame(self.window)
        list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # Configure row and column weights for resizing
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox for flashcard sets
        self.set_listbox = tk.Listbox(
            list_frame,
            width=50,
            height=10,
            font=("Arial", 11),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        self.set_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.set_listbox.yview)
        
        # Populate the listbox
        for flashcard_set in self.flashcard_sets:
            self.set_listbox.insert(tk.END, flashcard_set["name"])
        
        # Select the first item
        if self.flashcard_sets:
            self.set_listbox.selection_set(0)
        
        # Button Frame
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Start button
        start_button = tk.Button(
            button_frame,
            text="Start Learning",
            width=15,
            font=("Arial", 11),
            command=self.start_selected_set
        )
        start_button.grid(row=0, column=0, padx=5)
        
        # Add button
        add_button = tk.Button(
            button_frame,
            text="Add New Set",
            width=15,
            font=("Arial", 11),
            command=self.add_new_set
        )
        add_button.grid(row=0, column=1, padx=5)
        
        # Edit button
        edit_button = tk.Button(
            button_frame,
            text="Edit Set",
            width=15,
            font=("Arial", 11),
            command=self.edit_selected_set
        )
        edit_button.grid(row=0, column=2, padx=5)
        
        # Statistics label
        self.stats_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.stats_label.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="w")
        
        # Update statistics for the selected set
        self.set_listbox.bind('<<ListboxSelect>>', self.update_stats)
    
    def start_selected_set(self):
        """Start the selected flashcard set."""
        selected_indices = self.set_listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("Selection Required", "Please select a flashcard set.")
            return
        
        selected_index = selected_indices[0]
        selected_set = self.flashcard_sets[selected_index]
        
        # Check if the data file exists
        if not os.path.exists(selected_set["data_file"]):
            messagebox.showerror(
                "File Not Found", 
                f"The data file '{selected_set['data_file']}' was not found. "
                "Please edit the set with the correct file path."
            )
            return
        
        # Close the launcher window
        self.window.withdraw()
        
        # Start the flashcard app
        try:
            app = FlashcardApp(
                data_file=selected_set["data_file"],
                front_lang=selected_set["front_lang"],
                back_lang=selected_set["back_lang"]
            )
            
            # When the FlashcardApp closes, show the launcher again
            self.window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable the X button
            app.window.protocol("WM_DELETE_WINDOW", lambda: self.on_flashcard_close(app))
            
            app.run()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.window.deiconify()  # Show the launcher again
    
    def on_flashcard_close(self, app):
        """Handle the flashcard app closing."""
        app.window.destroy()
        self.window.deiconify()  # Show the launcher again
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)  # Re-enable the X button
        self.update_stats()  # Update statistics after studying
    
    def update_stats(self, event=None):
        """Update the statistics for the selected set."""
        selected_indices = self.set_listbox.curselection()
        
        if not selected_indices:
            self.stats_label.config(text="")
            return
        
        selected_index = selected_indices[0]
        selected_set = self.flashcard_sets[selected_index]
        
        # Check if the data file exists
        if not os.path.exists(selected_set["data_file"]):
            self.stats_label.config(text="Warning: Data file not found.")
            return
        
        # Get the known words file path
        data_dir = os.path.dirname(os.path.abspath(selected_set["data_file"]))
        base_name = os.path.splitext(os.path.basename(selected_set["data_file"]))[0]
        known_file = os.path.join(data_dir, f"{base_name}_known_words.json")
        
        # Count total words in the dataset
        try:
            import pandas as pd
            df = pd.read_csv(selected_set["data_file"])
            total_words = len(df)
            
            # Count known words
            known_words = 0
            if os.path.exists(known_file):
                with open(known_file, "r") as file:
                    known_list = json.load(file)
                    known_words = len(known_list)
            
            # Calculate progress percentage
            progress = (known_words / total_words) * 100 if total_words > 0 else 0
            
            # Update the statistics label
            stats_text = (
                f"Statistics for {selected_set['name']}:\n"
                f"Total words: {total_words}\n"
                f"Words learned: {known_words}\n"
                f"Progress: {progress:.1f}%"
            )
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            self.stats_label.config(text=f"Error loading statistics: {str(e)}")
    
    def add_new_set(self):
        """Open a dialog to add a new flashcard set."""
        self.open_set_dialog()
    
    def edit_selected_set(self):
        """Edit the selected flashcard set."""
        selected_indices = self.set_listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("Selection Required", "Please select a flashcard set to edit.")
            return
        
        selected_index = selected_indices[0]
        self.open_set_dialog(edit_index=selected_index)
    
    def open_set_dialog(self, edit_index=None):
        """Open a dialog to add or edit a flashcard set."""
        # Create a new dialog window
        dialog = tk.Toplevel(self.window)
        dialog.title("Add Flashcard Set" if edit_index is None else "Edit Flashcard Set")
        dialog.geometry("400x250")
        dialog.config(padx=20, pady=20)
        dialog.transient(self.window)  # Make the dialog modal
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Set the default values
        if edit_index is not None:
            set_data = self.flashcard_sets[edit_index]
            default_name = set_data["name"]
            default_file = set_data["data_file"]
            default_front = set_data["front_lang"]
            default_back = set_data["back_lang"]
        else:
            default_name = ""
            default_file = "data/"
            default_front = ""
            default_back = ""
        
        # Create form fields
        tk.Label(dialog, text="Set Name:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5)
        name_entry.insert(0, default_name)
        
        tk.Label(dialog, text="Data File Path:").grid(row=1, column=0, sticky="w", pady=5)
        file_entry = tk.Entry(dialog, width=30)
        file_entry.grid(row=1, column=1, sticky="ew", pady=5)
        file_entry.insert(0, default_file)
        
        # Browse button
        def browse_file():
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Select Data File",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            if filename:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, filename)
        
        browse_button = tk.Button(dialog, text="Browse...", command=browse_file)
        browse_button.grid(row=1, column=2, padx=5)
        
        tk.Label(dialog, text="Front Language:").grid(row=2, column=0, sticky="w", pady=5)
        front_entry = tk.Entry(dialog, width=30)
        front_entry.grid(row=2, column=1, sticky="ew", pady=5)
        front_entry.insert(0, default_front)
        
        tk.Label(dialog, text="Back Language:").grid(row=3, column=0, sticky="w", pady=5)
        back_entry = tk.Entry(dialog, width=30)
        back_entry.grid(row=3, column=1, sticky="ew", pady=5)
        back_entry.insert(0, default_back)
        
        # Save function
        def save_set():
            name = name_entry.get().strip()
            file_path = file_entry.get().strip()
            front_lang = front_entry.get().strip()
            back_lang = back_entry.get().strip()
            
            # Validate inputs
            if not name or not file_path or not front_lang or not back_lang:
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
                return
            
            # Create the set data
            set_data = {
                "name": name,
                "data_file": file_path,
                "front_lang": front_lang,
                "back_lang": back_lang
            }
            
            # Update or add the set
            if edit_index is not None:
                self.flashcard_sets[edit_index] = set_data
                self.set_listbox.delete(edit_index)
                self.set_listbox.insert(edit_index, name)
                self.set_listbox.selection_set(edit_index)
            else:
                self.flashcard_sets.append(set_data)
                self.set_listbox.insert(tk.END, name)
                self.set_listbox.selection_set(tk.END)
            
            # Save the configuration
            self.save_flashcard_sets()
            
            # Close the dialog
            dialog.destroy()
            
            # Update statistics
            self.update_stats()
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        save_button = tk.Button(button_frame, text="Save", width=10, command=save_set)
        save_button.grid(row=0, column=0, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", width=10, command=dialog.destroy)
        cancel_button.grid(row=0, column=1, padx=5)
    
    def run(self):
        """Run the launcher application."""
        self.window.mainloop()


if __name__ == "__main__":
    launcher = FlashcardLauncher()
    launcher.run()
