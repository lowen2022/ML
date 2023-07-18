import tkinter as tk
from tkinter import filedialog
import subprocess

class PreprocessGUI:
    def __init__(self, master):
        self.master = master
        master.title("Preprocess Script")

        self.dataset_label = tk.Label(master, text="Dataset:")
        self.dataset_label.pack()

        self.dataset_var = tk.StringVar(value="MIT_mixed_augm")
        self.dataset_radio1 = tk.Radiobutton(master, text="MIT_mixed_augm", variable=self.dataset_var, value="MIT_mixed_augm")
        self.dataset_radio1.pack()                                         #variable: stores the value of the user's selection
                                                                           #value :represents the value of the option.
        self.dataset_radio2 = tk.Radiobutton(master, text="STEREO_mixed_augm", variable=self.dataset_var, value="STEREO_mixed_augm")
        self.dataset_radio2.pack()

        self.train_src_label = tk.Label(master, text="Training Source File:")
        self.train_src_label.pack()

        self.train_src_button = tk.Button(master, text="Browse", command=self.browse_train_src)
        self.train_src_button.pack()

        self.train_src_path = tk.Label(master, text="")
        self.train_src_path.pack()

        self.train_tgt_label = tk.Label(master, text="Training Target File:")
        self.train_tgt_label.pack()

        self.train_tgt_button = tk.Button(master, text="Browse", command=self.browse_train_tgt)
        self.train_tgt_button.pack()

        self.train_tgt_path = tk.Label(master, text="")
        self.train_tgt_path.pack()

        self.valid_src_label = tk.Label(master, text="Validation Source File:")
        self.valid_src_label.pack()

        self.valid_src_button = tk.Button(master, text="Browse", command=self.browse_valid_src)
        self.valid_src_button.pack()

        self.valid_src_path = tk.Label(master, text="")
        self.valid_src_path.pack()

        self.valid_tgt_label = tk.Label(master, text="Validation Target File:")
        self.valid_tgt_label.pack()

        self.valid_tgt_button = tk.Button(master, text="Browse", command=self.browse_valid_tgt)
        self.valid_tgt_button.pack()

        self.valid_tgt_path = tk.Label(master, text="")

        self.save_data_label = tk.Label(master, text="Save Data Path:")
        self.save_data_label.pack()

        self.save_data_button = tk.Button(master, text="Browse", command=self.browse_save_data)
        self.save_data_button.pack()

        self.save_data_path = tk.Label(master, text="")

        self.src_seq_length_label = tk.Label(master, text="Source Sequence Length:")
        self.src_seq_length_label.pack()
        default_src_seq_length=tk.StringVar(value="1000")
        self.src_seq_length_entry = tk.Entry(master,textvariable=default_src_seq_length)
        self.src_seq_length_entry.pack()

        self.tgt_seq_length_label = tk.Label(master, text="Target Sequence Length:")
        self.tgt_seq_length_label.pack()
        default_tgt_seq_length = tk.StringVar(value="1000")
        self.tgt_seq_length_entry = tk.Entry(master,textvariable=default_tgt_seq_length)
        self.tgt_seq_length_entry.pack()

        self.src_vocab_size_label = tk.Label(master, text="Source Vocabulary Size:")
        self.src_vocab_size_label.pack()
        default_src_vocab_size = tk.StringVar(value="1000")
        self.src_vocab_size_entry = tk.Entry(master,textvariable=default_src_vocab_size)
        self.src_vocab_size_entry.pack()

        self.tgt_vocab_size_label = tk.Label(master, text="Target Vocabulary Size:")
        self.tgt_vocab_size_label.pack()
        default_vocab_size_entry = tk.StringVar(value="1000")
        self.tgt_vocab_size_entry = tk.Entry(master,textvariable=default_vocab_size_entry)
        self.tgt_vocab_size_entry.pack()

        self.share_vocab_var = tk.BooleanVar(value=True)
        self.share_vocab_check = tk.Checkbutton(master, text="Share Vocabulary", variable=self.share_vocab_var)
        self.share_vocab_check.pack()

        self.run_button = tk.Button(master, text="Run", command=self.run_script)
        self.run_button.pack()

    def browse_train_src(self):
        file_path = filedialog.askopenfilename()
        self.train_src_path.config(text=file_path)

    def browse_train_tgt(self):
        file_path = filedialog.askopenfilename()
        self.train_tgt_path.config(text=file_path)

    def browse_valid_src(self):
        file_path = filedialog.askopenfilename()
        self.valid_src_path.config(text=file_path)

    def browse_valid_tgt(self):
        file_path = filedialog.askopenfilename()
        self.valid_tgt_path.config(text=file_path)

    def browse_save_data(self):
        folder_path = filedialog.askdirectory()
        self.save_data_path.config(text=folder_path)

    def run_script(self):
        dataset = self.dataset_var.get()
        train_src_file = self.train_src_path.cget("text")
        train_tgt_file = self.train_tgt_path.cget("text")
        valid_src_file = self.valid_src_path.cget("text")
        valid_tgt_file = self.valid_tgt_path.cget("text")
        save_data_path = self.save_data_path.cget("text")
        src_seq_length = self.src_seq_length_entry.get()
        tgt_seq_length = self.tgt_seq_length_entry.get()
        src_vocab_size = self.src_vocab_size_entry.get()
        tgt_vocab_size = self.tgt_vocab_size_entry.get()
        share_vocab = "-share_vocab" if self.share_vocab_var.get() else ""

        command = f"python preprocess.py -train_src {train_src_file} -train_tgt {train_tgt_file} -valid_src {valid_src_file} -valid_tgt {valid_tgt_file} -save_data {save_data_path}/{dataset} -src_seq_length {src_seq_length} -tgt_seq_length {tgt_seq_length} -src_vocab_size {src_vocab_size} -tgt_vocab_size {tgt_vocab_size} {share_vocab}"

        subprocess.run(command, shell=True)

root = tk.Tk()
my_gui = PreprocessGUI(root)
root.mainloop()