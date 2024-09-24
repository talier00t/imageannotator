import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import csv

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotator")

        
        self.image_dir = filedialog.askdirectory(initialdir="C:/Users/user/Desktop", title="Select Image Folder")
        if not self.image_dir:
            exit()

        
        self.image_files = [f for f in os.listdir(self.image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.current_image_index = 0

        
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

        self.create_widgets()

        
        self.show_image()

    def create_widgets(self):
        
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        
        self.value_entry = tk.Entry(self.root)
        self.value_entry.pack()
        self.value_entry.focus()  

        
        self.next_button = tk.Button(self.root, text="Save and Next", command=self.save_and_next)
        self.next_button.pack()

    def show_image(self):
       
        if self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.image_dir, self.image_files[self.current_image_index])
            image = Image.open(image_path)
            image = image.resize((400, 400))  
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo  
            self.value_entry.delete(0, tk.END)  
            self.value_entry.focus() 
        else:
            
            self.image_label.config(text="All images have been processed.")
            self.value_entry.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)

    def save_and_next(self):
       
        value = self.value_entry.get()
        if value:
            try:
                
                float_value = float(value)

               
                if 0 <= float_value <= 10:
                    
                    with open(self.csv_file, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([self.image_files[self.current_image_index], float_value])

                    
                    self.current_image_index += 1
                    self.show_image()
                else:
                    
                    print("Please enter the value between 0 and 10.")
                    self.value_entry.delete(0, tk.END)  
                    self.value_entry.focus()  
            except ValueError:
                
                self.value_entry.delete(0, tk.END)
                print("Please enter a float value.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()




