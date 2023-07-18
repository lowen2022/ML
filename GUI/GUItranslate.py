import tkinter as tk
from tkinter import filedialog
import subprocess

class TranslateGUI:
    def __init__(self, master):
        self.master = master
        master.title("Translate Script")

        self.dataset_label = tk.Label(master, text="Dataset:")
        self.dataset_label.pack()

        self.dataset_var = tk.StringVar(value="MIT_mixed_augm_model_average_20.pt")
        self.dataset_radio1 = tk.Radiobutton(master, text="MIT_mixed", variable=self.dataset_var, value="MIT_mixed_augm_model_average_20.pt")
        self.dataset_radio1.pack()                                         #variable: stores the value of the user's selection
                                                                           #value :represents the value of the option.
        self.dataset_radio2 = tk.Radiobutton(master, text="STEREO_mixed", variable=self.dataset_var, value="STEREO_mixed_augm_model_average_20.pt")
        self.dataset_radio2.pack()

        # second part  file path:scr data,output
        self.src_label = tk.Label(master, text="Source File:")
        self.src_label.pack()

        self.src_button = tk.Button(master, text="Browse", command=self.browse_src)
        self.src_button.pack()

        self.src_path = tk.Label(master, text="")
        self.src_path.pack()


        self.save_data_label = tk.Label(master, text="Save Data Path:")
        self.save_data_label.pack()

        self.save_data_button = tk.Button(master, text="Browse", command=self.browse_save_data)
        self.save_data_button.pack()

        self.save_data_path = tk.Label(master, text="")
        self.save_data_path.pack()

        self.batch_size_label = tk.Label(master, text="batch_size:")
        self.batch_size_label.pack()
        default_batch_size=tk.StringVar(value="64")
        self.batch_size_entry = tk.Entry(master,textvariable=default_batch_size)
        self.batch_size_entry.pack()

        self.replace_unk_label = tk.Label(master, text="replace_unk:any char or not")
        self.replace_unk_label.pack()
        default_replace_unk = tk.StringVar(value="")
        self.replace_unk_entry = tk.Entry(master,textvariable=default_replace_unk)
        self.replace_unk_entry.pack()

        self.max_length_label = tk.Label(master, text="max_length:")
        self.max_length_label.pack()
        default_max_length = tk.StringVar(value="200")
        self.max_length_entry = tk.Entry(master,textvariable=default_max_length)
        self.max_length_entry.pack()

        self.fast_label = tk.Label(master, text="fast:True or False")
        self.fast_label.pack()
        default_vocab_size_entry = tk.StringVar(value="")
        self.fast_entry = tk.Entry(master,textvariable=default_vocab_size_entry)
        self.fast_entry.pack()

        self.share_vocab_var = tk.BooleanVar(value=True)
        self.share_vocab_check = tk.Checkbutton(master, text="Share Vocabulary", variable=self.share_vocab_var)
        self.share_vocab_check.pack()

        self.run_button = tk.Button(master, text="Run", command=self.run_script)
        self.run_button.pack()


    def browse_src(self):
        file_path = filedialog.askopenfilename()
        self.src_path.config(text=file_path)

    def browse_save_data(self):
        folder_path = filedialog.askdirectory()
        self.save_data_path.config(text=folder_path)

    def run_script(self):
        model = self.dataset_var.get()
        src_file = self.src_path.cget("text")

        save_data_path = self.save_data_path.cget("text")
        print(save_data_path)
        batch_size = self.batch_size_entry.get()
        replace_unk = self.replace_unk_entry.get()
        max_length = self.max_length_entry.get()
        fast = self.fast_entry.get()


        command = f"python translate.py -model {model} -src {src_file}  -output {save_data_path}/predictions__{model}.txt -batch_size {batch_size} -replace_unk {replace_unk} -max_length {max_length} -fast {fast} "

        subprocess.run(command, shell=True)

root = tk.Tk()
my_gui = TranslateGUI(root)
root.mainloop()