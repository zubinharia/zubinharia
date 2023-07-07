import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
#import win32com.client as win32

def connect_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        messagebox.showinfo("Error", "No file selected.")
        return

    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Group data based on user selection
        group_options = list(df.columns)  # Assuming columns are used for grouping
        groupby_var = tk.StringVar()
        groupby_var.set(group_options[0])

        group_label = tk.Label(window, text="Select Group By:")
        group_label.grid(row=1, column=0, padx=10, pady=5)

        group_menu = tk.OptionMenu(window, groupby_var, *group_options)
        group_menu.grid(row=1, column=1, padx=10, pady=5)

        def group_data():
            selected_group = groupby_var.get()
            grouped_data = df.groupby(selected_group).size().reset_index(name='Count')
            messagebox.showinfo("Grouped Data", str(grouped_data))

            # Draft email with grouped data and save to outbox
            email_subject = "Grouped Data"
            email_body = str(grouped_data)

            outlook = win32.Dispatch('Outlook.Application')
            mail = outlook.CreateItem(0)  # 0 represents an email item

            mail.Subject = email_subject
            mail.Body = email_body
            mail.Save()

            messagebox.showinfo("Success", "Email drafted and saved to Outbox.")

        group_button = tk.Button(window, text="Group Data", command=group_data)
        group_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    except Exception as e:
        messagebox.showinfo("Error", f"Error loading Excel file: {str(e)}")

if __name__ == '__main__':
    window = tk.Tk()
    window.title("PRG Receivables")

    connect_button = tk.Button(window, text="Connect to Excel", command=connect_excel)
    connect_button.pack(padx=10, pady=5)

    window.mainloop()
