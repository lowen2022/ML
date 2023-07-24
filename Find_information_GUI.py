import sys
sys.path.append("C:/Users/Asus/anaconda3/lib/site-packages")

import pubchempy as pcp
import tkinter as tk
from tkinter import filedialog
import subprocess


class Find_information_GUI:
    def __init__(self,master):
        self.master = master
        master.title("User Platform")
        self.type_label=tk.Label(master, text="Select the format:")
        self.type_label.pack()
        #choose the type
        self.type_label_var = tk.StringVar(value="cid")
        self.type_label_radio1 = tk.Radiobutton(master, text="cid", variable=self.type_label_var, value="cid")
        self.type_label_radio1.pack()

        self.type_label_radio2 = tk.Radiobutton(master, text="smiles", variable=self.type_label_var, value="smiles")
        self.type_label_radio2.pack()

        self.type_label_radio3 = tk.Radiobutton(master, text="name", variable=self.type_label_var, value="name")
        self.type_label_radio3.pack()
        #input and output
        self.input_label = tk.Label(master, text="Input:")
        self.input_label.pack()

        self.input_text = tk.Text(master, height=5, width=50)
        self.input_text.pack()

        self.output_text = tk.Text(master, height=25, width=100)
        self.output_text.pack()

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

        type = self.type_label_var.get()
        values = self.input_text.get("1.0", "end").split("\n")
        smiles_list = []  # initialize empty list to store SMILES

        for value in values:
            if not value.strip():
                continue
            if type == 'cid':
                c = pcp.Compound.from_cid(int(value))
                smiles = c.isomeric_smiles
                cid = int(value)
                name = c.iupac_name
                molecular_formula = c.molecular_formula
                self.output_text.insert(tk.END, f"The smiles of {value} is {smiles}.\n")
                self.output_text.insert(tk.END, f"The cid of {value} is {cid}.\n")
                self.output_text.insert(tk.END, f"The name of {value} is {name}.\n")
                self.output_text.insert(tk.END, f"The molecular formal of {value} is {molecular_formula}.\n\n")
            elif type == 'name':
                compound = pcp.get_compounds(value, 'name')
                cid = ""
                for char in str(compound):
                    if char.isdigit():
                        cid += char
                cidnum = int(cid)
                c = pcp.Compound.from_cid(int(cidnum))
                smiles = c.isomeric_smiles
                cid = cidnum
                name = c.iupac_name
                molecular_formula = c.molecular_formula
                self.output_text.insert(tk.END, f"The smiles of {value} is {smiles}.\n")
                self.output_text.insert(tk.END, f"The cid of {value} is {cid}.\n")
                self.output_text.insert(tk.END, f"The name of {value} is {name}.\n")
                self.output_text.insert(tk.END, f"The molecular formal of {value} is {molecular_formula}.\n")
            elif type == 'smiles':
                compound = pcp.get_compounds(value, 'smiles')
                cid = ""
                for char in str(compound):
                    if char.isdigit():
                        cid += char
                cidnum = int(cid)
                c = pcp.Compound.from_cid(int(cidnum))
                smiles = c.isomeric_smiles
                cid = cidnum
                name = c.iupac_name
                molecular_formula = c.molecular_formula
                self.output_text.insert(tk.END, f"The smiles of {value} is {smiles}.\n")
                self.output_text.insert(tk.END, f"The cid of {value} is {cidnum}.\n")
                self.output_text.insert(tk.END, f"The name of {value} is {name}.\n")
                self.output_text.insert(tk.END, f"The molecular formal of {value} is {molecular_formula}.\n")

            tokenizer = smi_tokenizer(smiles)
            smiles_list.append(smiles)  # append SMILES to list

        # Output SMILES list with periods as separators
        output_data = ".".join(smiles_list)

            # Insert SMILES list into output_text widget
        self.output_text.insert(tk.END, f"All SMILES:\n{output_data}\n")


                # with open(f"C:\Users\hydro1\lowen\MolecularTransformer-master\data\TEST\cid_{cidnum}.txt", "w") as f:
                #     f.write(f"{tokenizer}\n")
                #
                # with open(f"C:\Users\hydro1\lowen\MolecularTransformer-master\data\TEST\cid_{cidnum}.txt", "r") as f:
                #     content=f.read()
                # print(content)


root = tk.Tk()
my_gui = Find_information_GUI(root)
root.mainloop()