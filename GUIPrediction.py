import sys
sys.path.append("C:/Users/Asus/anaconda3/lib/site-packages")

import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import re
import pubchempy as pcp
class Prediction_GUI:
    def __init__(self,master):
        self.master = master
        master.title("User Platform")
        self.type_label=tk.Label(master, text="select the format:")
        self.type_label.pack()


        self.type_label_var = tk.StringVar(value="MIT_mixed_augm_model_average_20.pt")
        self.dataset_radio1 = tk.Radiobutton(master, text="MIT_mixed", variable=self.type_label_var, value="MIT_mixed_augm_model_average_20.pt")
        self.dataset_radio1.pack()                                         #variable: stores the value of the user's selection
                                                                           #value :represents the value of the option.
        self.dataset_radio2 = tk.Radiobutton(master, text="STEREO_mixed", variable=self.type_label_var, value="STEREO_mixed_augm_model_average_20.pt")
        self.dataset_radio2.pack()

        self.dataset_radio3 = tk.Radiobutton(master, text="MIT_separated", variable=self.type_label_var, value="MIT_separated_augm_model_average_20.pt")
        self.dataset_radio3.pack()

        self.dataset_radio4 = tk.Radiobutton(master, text="STEREO_separated", variable=self.type_label_var, value="STEREO_separated_augm_model_average_20.pt")
        self.dataset_radio4.pack()

        #input
        self.input_label = tk.Label(master, text="input:")
        self.input_label.pack()

        self.input_entry = tk.Entry(master)
        self.input_entry.pack()
        #parameter
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

        # output
        self.prediction_label = tk.Label(master, text="result:")
        self.prediction_label.pack()
        #run button
        self.run_button = tk.Button(master, text="Run", command=self.run_script)
        self.run_button.pack()


    def run_script(self):
        def smi_tokenizer(smi):
            """
            Tokenize a SMILES molecule or reaction
            """

            pattern = "(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\(|\)|\.|=|#|-|\+|\\\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])"
            regex = re.compile(pattern)
            tokens = [token for token in regex.findall(smi)]
            assert smi == ''.join(tokens)
            return ' '.join(tokens)

        type = self.type_label_var.get()
        smiles= self.input_entry.get()
        batch_size = self.batch_size_entry.get()
        replace_unk = self.replace_unk_entry.get()
        max_length = self.max_length_entry.get()
        fast = self.fast_entry.get()
        tokenizer = smi_tokenizer(smiles)
        with open("src-test", "w") as f:
            f.write(f"{tokenizer}\n")
        #success
        # with open("src-test", "r") as f:
        #     content=f.read()
        # print(content)
        src_file="src-test"
        command = f"python translate.py -model {type} -src {src_file}  -output predictions.txt -batch_size {batch_size} -replace_unk {replace_unk} -max_length {max_length} -fast {fast} "
        subprocess.run(command, shell=True)
        with open("predictions.txt", "r") as f:
            final=f.read().replace(" ","")
            print("findal",final)
        self.prediction_label.config(text=final)

root = tk.Tk()
my_gui = Prediction_GUI(root)
root.mainloop()