import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os

def select_repository():
    repo_path = filedialog.askdirectory(title="Select Git Repository")
    if repo_path:
        os.chdir(repo_path)
        load_branches()

def load_branches():
    branches = subprocess.getoutput("git branch").split("\n")
    branches = [branch.strip().replace("* ", "") for branch in branches]
    combo1['values'] = branches
    combo2['values'] = branches

def show_diff():
    branch1 = combo1.get()
    branch2 = combo2.get()
    cmd = f"git diff {branch1}..{branch2}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    text.delete(1.0, tk.END)
    text.insert(tk.END, output.decode())

app = tk.Tk()
app.title("Git Diff GUI")

select_repo_button = tk.Button(app, text="Select Repository", command=select_repository)
select_repo_button.pack(pady=10)

combo1 = ttk.Combobox(app)
combo2 = ttk.Combobox(app)
combo1.pack(pady=10)
combo2.pack(pady=10)

button = tk.Button(app, text="Diff表示", command=show_diff)
button.pack(pady=10)

text = tk.Text(app)
text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

app.mainloop()
