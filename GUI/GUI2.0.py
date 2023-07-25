import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import re
import pubchempy as pcp
import cirpy
class GUI2:
    def __init__(self,master):
        self.master = master
        master.title("User Platform")
        self.Type_label = tk.Label(master, text="select the format:")
        self.Type_label.pack()
        self.Type_label2 = tk.Label(master, text="use enter to input next one")
        self.Type_label2.pack()
        # choose the Type
        self.Type_label_var = tk.StringVar(value="cid")
        self.Type_label_radio1 = tk.Radiobutton(master, text="cid", variable=self.Type_label_var, value="cid")
        self.Type_label_radio1.pack()

        self.Type_label_radio2 = tk.Radiobutton(master, text="smiles", variable=self.Type_label_var, value="smiles")
        self.Type_label_radio2.pack()

        self.Type_label_radio3 = tk.Radiobutton(master, text="name", variable=self.Type_label_var, value="name")
        self.Type_label_radio3.pack()

        self.Type_label_radio4 = tk.Radiobutton(master, text="cas", variable=self.Type_label_var, value="cas")
        self.Type_label_radio4.pack()

        #input
        self.input_text = tk.Text(master, height=5, width=50)
        self.input_text.pack()



        # self.share_vocab_var = tk.BooleanVar(value=True)
        # self.share_vocab_check = tk.Checkbutton(master, text="Share Vocabulary", variable=self.share_vocab_var)
        # self.share_vocab_check.pack()

        # output
        self.prediction_label = tk.Label(master, text="result:")
        self.prediction_label.pack()
        self.output_text = tk.Text(master, height=10, width=50)
        self.output_text.pack()
        #run button
        self.run_button = tk.Button(master, text="Run", command=self.run_script)
        self.run_button.pack()


    def run_script(self):
        def smi_tokenizer(smi):
            """
            Tokenize a SMILES molecule or reaction
            """
            import re
            pattern = "(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\(|\)|\.|=|#|-|\+|\\\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])"
            regex = re.compile(pattern)
            tokens = [token for token in regex.findall(smi)]
            assert smi == ''.join(tokens)
            return ' '.join(tokens)
        Type = self.Type_label_var.get()
        values = self.input_text.get("1.0", "end").split("\n")
        smiles_list = []  # initialize empty list to store SMILES
        for value in values:
            if not value.strip():
                continue
            if Type =='cid':
                c = pcp.Compound.from_cid(int(value))
                smiles=c.isomeric_smiles
                cidnum=int(value)
                name=c.iupac_name
                molecular_formula=c.molecular_formula
                cas = cirpy.resolve(smiles, "cas")
            elif Type =='name':
                compound = pcp.get_compounds(value, 'name')
                cid=""
                for char in str(compound):
                    if char.isdigit():
                        cid +=char
                cidnum=int(cid)
                c = pcp.Compound.from_cid(int(cidnum))
                smiles=c.isomeric_smiles
                name=c.iupac_name
                molecular_formula=c.molecular_formula
                cas = cirpy.resolve(smiles, "cas")

            elif Type =='smiles':
                compound = pcp.get_compounds(value, 'smiles')
                cid=""
                for char in str(compound):
                    if char.isdigit():
                        cid +=char
                cidnum=int(cid)
                c = pcp.Compound.from_cid(int(cidnum))
                smiles=c.isomeric_smiles
                name=c.iupac_name
                molecular_formula=c.molecular_formula
                cas = cirpy.resolve(smiles, "cas")

            elif Type =='cas':
                print(value)
                smiles=cirpy.resolve(f'{value}', 'smiles')
                compound = pcp.get_compounds(smiles, 'smiles')
                cid=""
                for char in str(compound):
                    if char.isdigit():
                        cid +=char
                cidnum=int(cid)
                c = pcp.Compound.from_cid(int(cidnum))
                smiles=c.isomeric_smiles
                name=c.iupac_name
                molecular_formula=c.molecular_formula
                cas = cirpy.resolve(smiles, "cas")


            smiles_list.append(smiles)  # append SMILES to list
        # Output SMILES list with periods as separators
        output_data = ".".join(smiles_list)
        input_smilesline=smi_tokenizer(output_data)





        with open("src-test", "w") as f:
            f.write(f"{input_smilesline}\n")
        #success
        # with open("src-test", "r") as f:
        #     content=f.read()
        # print(content)
        src_file="src-test"
        batch_size=64
        replace_unk=''
        max_length=200
        fast=''
        weight_list=['MIT_mixed_augm_model_average_20.pt','STEREO_mixed_augm_model_average_20.pt','MIT_separated_augm_model_average_20.pt','STEREO_separated_augm_model_average_20.pt']
        for Type in weight_list:

            command = f"python translate.py -model {Type} -src {src_file}  -output predictions.txt -batch_size {batch_size} -replace_unk {replace_unk} -max_length {max_length} -fast {fast} "
            subprocess.run(command, shell=True)
            with open("predictions.txt", "r") as f:
                final=f.read().replace(" ","")
                print("findal",final)
                value=final
            print("finalvalue",value)
            compound = pcp.get_compounds(value, 'smiles')
            cid=""
            for char in str(compound):
                if char.isdigit():
                    cid +=char
            if(cid!=''):
                cidnum=int(cid)
                c = pcp.Compound.from_cid(int(cidnum))
                smiles = c.isomeric_smiles
                name = c.iupac_name
                molecular_formula = c.molecular_formula
                if (Type == 'MIT_mixed_augm_model_average_20.pt'):
                    self.prediction_label.config(text=f"finish,result:{final}")
                self.output_text.insert(tk.END, f"The type of {value} is {Type}.\n")
                self.output_text.insert(tk.END, f"The smiles of {value} is {smiles}.\n")
                self.output_text.insert(tk.END, f"The cid of {value} is {cidnum}.\n")
                self.output_text.insert(tk.END, f"The name of {value} is {name}.\n")
                self.output_text.insert(tk.END, f"The molecular formal of {value} is {molecular_formula}.\n")
                self.output_text.insert(tk.END, "\n")
                if (Type == 'STEREO_separated_augm_model_average_20.pt'):
                    self.output_text.insert(tk.END, "------------------\n")
            else:
                self.output_text.insert(tk.END, f"The type of {value} is {Type}.\n")
                self.output_text.insert(tk.END, f"The smiles of {value} is {smiles}.\n")
                self.output_text.insert(tk.END, f"No CID.\n")
                self.output_text.insert(tk.END, "\n")




root = tk.Tk()
my_gui = GUI2(root)
root.mainloop()