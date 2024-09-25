import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import csv
import re

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotator")

        
        self.root.geometry("800x800")
        self.root.resizable(False, False)  

       
        self.image_dir = filedialog.askdirectory(initialdir="C:/Users/user/Desktop", title="Select Image Folder")
        if not self.image_dir:
            exit()

       
        self.image_files = sorted([f for f in os.listdir(self.image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))], key=self.natural_key)

        
        self.scores = {}

       
        self.csv_file = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                       filetypes=[("CSV Files", "*.csv")],
                                                       initialdir="C:/Users/user/Desktop", 
                                                       title="Save CSV File")
        if not self.csv_file:
            exit()

       
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Image Name', 'Value'])

       
        self.current_image_index = self.find_last_processed_image()
        
        self.create_widgets()
        self.show_image()

       
        self.root.bind('<Return>', lambda event: self.save_and_next())

    def natural_key(self, text):
        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', text)]

    def find_last_processed_image(self):
        
        last_image = None
        try:
            with open(self.csv_file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader) 
                for row in reader:
                    last_image = row[0]
        except FileNotFoundError:
            pass

        if last_image:
            try:
                return self.image_files.index(last_image) + 1 
            except ValueError:
                return 0 
        else:
            return 0  

    def create_widgets(self):
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10) 
        self.image_name_label = tk.Label(self.root, text="")
        self.image_name_label.pack()
        self.value_entry = tk.Entry(self.root)
        self.value_entry.pack()
        self.value_entry.focus()

        self.prev_button = tk.Button(self.root, text="Previous", command=self.previous_image)
        self.prev_button.place(relx=0.2, rely=0.95, anchor="center")  # Alt tarafa sabitliyoruz.

        self.next_button = tk.Button(self.root, text="Next", command=self.regular_next)
        self.next_button.place(relx=0.5, rely=0.95, anchor="center")  # Alt tarafa sabitliyoruz.

        self.save_next_button = tk.Button(self.root, text="Save and Next", command=self.save_and_next)
        self.save_next_button.place(relx=0.8, rely=0.95, anchor="center")  # Alt tarafa sabitliyoruz.

    def show_image(self):
        if self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.image_dir, self.image_files[self.current_image_index])
            image = Image.open(image_path)
            max_width, max_height = 750, 600 
            original_size = image.size
            aspect_ratio = original_size[0] / original_size[1]

            if original_size[0] > max_width or original_size[1] > max_height:
                if aspect_ratio > 1: 
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)
                    
                else: 
                    
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  

          
            self.image_name_label.config(text=self.image_files[self.current_image_index])
            current_score = self.scores.get(self.image_files[self.current_image_index], "")
            self.value_entry.delete(0, tk.END)  
            self.value_entry.insert(0, str(current_score))  
            self.value_entry.focus() 
            
        else: 
            
            self.image_label.config(text="All images have been processed.")
            self.image_name_label.config(text="")
            self.value_entry.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.prev_button.config(state=tk.DISABLED)
            self.save_next_button.config(state=tk.DISABLED)

    def save_and_next(self):
        value = self.value_entry.get()
        if value:
            try:
                float_value = float(value)

                if 0 <= float_value <= 10:
                    if self.image_files[self.current_image_index] in self.scores:
                        self.remove_previous_score(self.image_files[self.current_image_index])
                    self.scores[self.image_files[self.current_image_index]] = float_value

                    with open(self.csv_file, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([self.image_files[self.current_image_index], float_value])

                    self.current_image_index += 1
                    self.show_image()
                else:
                    print("Please enter a value between 0 and 10.")
                    self.value_entry.delete(0, tk.END)  
                    self.value_entry.focus()  
            except ValueError:
                self.value_entry.delete(0, tk.END)
                print("Please enter a float value.")

    def remove_previous_score(self, image_name):
        with open(self.csv_file, 'r', newline='') as csvfile:
            rows = list(csv.reader(csvfile))

        with open(self.csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                if row[0] != image_name:
                    writer.writerow(row)

    def regular_next(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_image()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()
