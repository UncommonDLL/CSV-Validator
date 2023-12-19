import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import re
import socket

# Disposable email domains list and common domain typos
DISPOSABLE_EMAIL_DOMAINS = [
    '10minutemail.com', 'tempmail.com', 'mohmal.com', 'throwawaymail.com',
    'guerrillamail.com', 'mailinator.com', 'yopmail.com', 'getnada.com',
    'dispostable.com', 'maildrop.cc', 'mintemail.com', 'burnermail.io',
    'spam4.me', 'tempmailaddress.com', 'mailcatch.com', 'tempail.com'
]

COMMON_DOMAIN_MISTAKES = {
    'gmial.com': 'gmail.com', 'gamil.com': 'gmail.com', 'gmail.con': 'gmail.com',
    'hotmai.com': 'hotmail.com', 'hotmal.com': 'hotmail.com', 'hotnail.com': 'hotmail.com',
    'hotmail.con': 'hotmail.com', 'yhoo.com': 'yahoo.com', 'yaho.com': 'yahoo.com',
    'yahooo.com': 'yahoo.com', 'yahoocom': 'yahoo.com', 'outlok.com': 'outlook.com',
    'outlok.con': 'outlook.com', 'outloook.com': 'outlook.com', 'aol.con': 'aol.com',
    'rocketmaol.com': 'rocketmail.com', 'zoho.con': 'zoho.com'
}


# Function to upload CSV file
def upload_file():
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=(("CSV files", "*.csv"),))
    if file_path:
        file_path_var.set(file_path)
        process_btn['state'] = tk.NORMAL
        update_column_dropdowns(file_path)

def enhanced_load_data(file_path, first_name_column, last_name_column, email_column):
    try:
        df = pd.read_csv(file_path)
        missing_columns = [col for col in [first_name_column, last_name_column, email_column] if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Expected columns not found in CSV: {', '.join(missing_columns)}")
        df = df[[email_column, first_name_column, last_name_column]]
        return df
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def clean_data(df, first_name_column, last_name_column, email_column):
    split_names = df[last_name_column].str.split(' ', n=1, expand=True)
    df[first_name_column] = df[first_name_column].combine_first(split_names[0])
    df[last_name_column] = split_names[1].combine_first(df[last_name_column])
    df = df.dropna(subset=[email_column])
    return df

def enhanced_validate_emails(df, email_column):
    # Improved regex pattern
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    valid_emails = df[email_column].str.contains(pattern)
    
    # Domain verification
    for _, email in df.loc[valid_emails, email_column].items():
        domain = email.split('@')[1]
        try:
            socket.gethostbyname(domain)
        except socket.gaierror:
            valid_emails.loc[valid_emails.index == _] = False
            continue

        # Check against disposable email domains
        if domain in DISPOSABLE_EMAIL_DOMAINS:
            valid_emails.loc[valid_emails.index == _] = False
            continue

        # Check and correct common domain typos
        if domain in COMMON_DOMAIN_MISTAKES:
            corrected_domain = COMMON_DOMAIN_MISTAKES[domain]
            df.loc[df.index == _, email_column] = email.replace(domain, corrected_domain)
            
    invalid_count = (~valid_emails).sum()
    df = df[valid_emails]
    return df, invalid_count

def save_to_csv(df):
    file_path = filedialog.asksaveasfilename(title="Save as", defaultextension=".csv", filetypes=(("CSV files", "*.csv"),))
    if file_path:
        try:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving CSV file: {str(e)}")

def display_in_ui(df, feedback_box):
    feedback_box.delete(1.0, tk.END)
    feedback_box.insert(tk.END, df.to_string())

def process_csv():
    df = enhanced_load_data(file_path_var.get(), first_name_col.get(), last_name_col.get(), email_col.get())
    if df is not None:
        df = clean_data(df, first_name_col.get(), last_name_col.get(), email_col.get())
        df, invalid_count = enhanced_validate_emails(df, email_col.get())  # Updated the function call here
        desired_order = [email_col.get(), first_name_col.get(), last_name_col.get()]
        df = df[desired_order]
        save_option = messagebox.askyesno("Save Data", "Would you like to save the cleaned data to a new CSV file?")
        if save_option:
            save_to_csv(df)
        else:
            display_in_ui(df, feedback_box)
        valid_count = len(df)
        feedback = f"{valid_count} valid entries processed. {invalid_count} invalid email addresses found."
        feedback_box.insert(tk.END, "\n\n" + feedback)


def update_column_dropdowns(file_path):
    try:
        sample_df = pd.read_csv(file_path, nrows=5)
        columns = sample_df.columns.tolist()
        first_name_col['values'] = columns
        last_name_col['values'] = columns
        email_col['values'] = columns
        if "First Name" in columns:
            first_name_col.set("First Name")
        if "Last Name" in columns:
            last_name_col.set("Last Name")
        if "Email" in columns:
            email_col.set("Email")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading CSV columns: {str(e)}")

# Main application window
window = tk.Tk()
window.title("Email Validator")

file_path_var = tk.StringVar()
tk.Label(window, text="Upload CSV file:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
tk.Entry(window, textvariable=file_path_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(window, text="Browse", command=upload_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(window, text="First Name Column:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
first_name_col = ttk.Combobox(window)
first_name_col.grid(row=1, column=1, padx=10, pady=10)

tk.Label(window, text="Last Name Column:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
last_name_col = ttk.Combobox(window)
last_name_col.grid(row=2, column=1, padx=10, pady=10)

tk.Label(window, text="Email Column:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
email_col = ttk.Combobox(window)
email_col.grid(row=3, column=1, padx=10, pady=10)

process_btn = tk.Button(window, text="Process CSV", state=tk.DISABLED, command=process_csv)
process_btn.grid(row=5, column=1, padx=10, pady=20)

feedback_box = tk.Text(window, height=10, width=50)
feedback_box.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

window.mainloop()
