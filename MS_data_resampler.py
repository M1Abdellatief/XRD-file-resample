import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import os

def resample_data(input_file, step_size):
    # Read the data file
    data = pd.read_csv(input_file, delim_whitespace=True, comment='#', names=['2th', 'Int'])

    # Define the new 2th range based on the desired step size
    min_2th = data['2th'].min()
    max_2th = data['2th'].max()
    new_2th = np.arange(min_2th, max_2th + step_size, step_size)

    # Resample the data
    resampled_data = pd.DataFrame()
    resampled_data['2th'] = new_2th
    resampled_data['Int'] = np.interp(new_2th, data['2th'], data['Int'])

    # Create output file name
    directory, filename = os.path.split(input_file)
    file_root, file_ext = os.path.splitext(filename)
    output_file = os.path.join(directory, f"{file_root}_resampled{file_ext}")

    # Save the resampled data to a new file
    resampled_data.to_csv(output_file, sep='\t', index=False, header=['#2th', '#Int'], float_format='%.5f')
    return output_file

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        path_var.set(directory)

def run_resampling():
    directory = path_var.get()
    step_size = step_size_var.get()

    if not directory or not step_size:
        messagebox.showerror("Input Error", "Please select a directory and enter a valid step size.")
        return

    try:
        step_size = float(step_size)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric step size.")
        return

    # Process all .dat files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            input_file = os.path.join(directory, filename)
            output_file = resample_data(input_file, step_size)
            messagebox.showinfo("Success", f"Resampled file saved as: {output_file}")

root = tk.Tk()
root.title("MS-Data Resampler")

# Define variables
path_var = tk.StringVar()
step_size_var = tk.StringVar()

# Create the GUI layout
tk.Label(root, text="Select Directory:(where add files.dat aimed to be resampled)").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=path_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_directory).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="New Step Size:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=step_size_var, width=20).grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Run Resampling", command=run_resampling).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
