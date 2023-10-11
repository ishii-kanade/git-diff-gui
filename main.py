import tkinter as tk
from tkinter import filedialog
import subprocess
import os

class GitDiffApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Git Diff with Tkinter")

        self.configure(bg="white")

        self.repo_button = tk.Button(self, text="Select Repository", command=self.select_repository, bg="white", fg="black")
        self.repo_button.pack(pady=10)

        self.branch1_var = tk.StringVar(self)
        self.branch2_var = tk.StringVar(self)

        self.combo1 = tk.OptionMenu(self, self.branch1_var, "")
        self.combo1.configure(bg="white", fg="black")
        self.combo1["menu"].config(bg="white", fg="black")

        self.combo2 = tk.OptionMenu(self, self.branch2_var, "")
        self.combo2.configure(bg="white", fg="black")
        self.combo2["menu"].config(bg="white", fg="black")

        self.combo1.pack(pady=5)
        self.combo2.pack(pady=5)

        self.diff_button = tk.Button(self, text="Export Diff", command=self.export_diff, bg="white", fg="black")
        self.diff_button.pack(pady=10)

        simple_diff_btn = tk.Button(self, text="Export Simple Diff", command=self.simple_git_diff)
        simple_diff_btn.pack()

        self.text = tk.Text(self, bg="white", fg="black", insertbackground="black", width=80, height=20)
        self.text.pack(padx=10, pady=10)

    def select_repository(self):
        repo_path = filedialog.askdirectory(title="Select Git Repository")
        if repo_path:
            os.chdir(repo_path)
            self.load_branches()

    def load_branches(self):
        branches = subprocess.getoutput("git branch").split("\n")
        branches = [branch.strip().replace("* ", "") for branch in branches]
        self.branch1_var.set("")
        self.branch2_var.set("")
        self.combo1["menu"].delete(0, "end")
        self.combo2["menu"].delete(0, "end")
        for branch in branches:
            self.combo1["menu"].add_command(label=branch, command=tk._setit(self.branch1_var, branch))
            self.combo2["menu"].add_command(label=branch, command=tk._setit(self.branch2_var, branch))

    def simple_git_diff(self):
        branch1 = self.branch1_var.get()
        branch2 = self.branch2_var.get()
        cmd = f"git diff {branch1}..{branch2}"

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        with open("simple_diff_output.txt", "w", encoding="utf-8") as file:
            if error:
                file.write("Error:\n" + error.decode())
            else:
                file.write(output.decode())

        self.text.insert(tk.END, "Simple Git Diff has been saved to simple_diff_output.txt")

    def export_diff(self):
        branch1 = self.branch1_var.get()
        branch2 = self.branch2_var.get()
        cmd = f"git diff $(git merge-base {branch1} {branch2})..{branch2}"

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        with open("diff_output.txt", "w", encoding="utf-8") as file:
            if error:
                file.write("Error:\n" + error.decode())
            else:
                file.write(output.decode())

        self.text.insert(tk.END, "Diff has been saved to diff_output.txt")



if __name__ == "__main__":
    app = GitDiffApp()
    app.mainloop()
