import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from plagiarism_engine import PlagiarismEngine
class PlagiarismGUI:
    def __init__(self, root):
        self.root = root
        root.title("Plagiarism Detection Engine")
        root.geometry("900x600")
        self.engine = None

        # Top frame for n-gram size and initialization
        frame_top = tk.Frame(root)
        frame_top.pack(pady=10)
        tk.Label(frame_top, text="n-gram size:").pack(side=tk.LEFT)
        self.ngram_entry = tk.Entry(frame_top, width=5)
        self.ngram_entry.insert(0, "3")
        self.ngram_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Init Engine", command=self.init_engine).pack(side=tk.LEFT, padx=5)

        # Middle frame for document operations
        frame_mid = tk.Frame(root)
        frame_mid.pack(pady=10)
        tk.Button(frame_mid, text="Add Document", command=self.add_document).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_mid, text="List Documents", command=self.list_documents).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_mid, text="Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5)

        # Bottom frame for comparison operations
        frame_bot = tk.Frame(root)
        frame_bot.pack(pady=10)
        tk.Button(frame_bot, text="Compare Two Docs", command=self.compare_two).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bot, text="Most Similar to...", command=self.most_similar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_bot, text="Report Pairs ≥ threshold", command=self.report_pairs).pack(side=tk.LEFT, padx=5)

        # Output area with scrollbar
        output_frame = tk.Frame(root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.output = tk.Text(output_frame, height=15, width=80, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_output(self):
        self.output.delete(1.0, tk.END)

    def log(self, message):
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.root.update_idletasks()

    def init_engine(self):
        try:
            n = int(self.ngram_entry.get())
            if n < 1:
                raise ValueError("n-gram size must be at least 1")
            # Using chaining with z=257, initial size 101
            self.engine = PlagiarismEngine("Chain", (257, 101), n)
            self.log(f"Engine initialized with n={n}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize engine: {str(e)}")

    def add_document(self):
        if self.engine is None:
            messagebox.showwarning("Warning", "Initialize engine first")
            return
        
        file_path = filedialog.askopenfilename(
            title="Select text file", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return
        
        title = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Simple tokenization: split on whitespace and filter empty strings
            words = [word.strip() for word in text.split() if word.strip()]
            
            if not words:
                messagebox.showwarning("Warning", "Document appears to be empty")
                return
            
            self.engine.add_document(title, words)
            distinct_count = self.engine.get_distinct_count(title)
            self.log(f"Added document: {title}")
            self.log(f"  Words: {len(words)}, Distinct n-grams: {distinct_count}")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        except UnicodeDecodeError:
            messagebox.showerror("Error", "Could not read file - encoding issue")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def list_documents(self):
        if self.engine is None:
            messagebox.showwarning("Warning", "Initialize engine first")
            return
        
        titles = self.engine.titles
        self.log("=== Documents ===")
        if not titles:
            self.log("  (No documents loaded)")
        else:
            for i, t in enumerate(titles, 1):
                count = self.engine.get_distinct_count(t)
                self.log(f"  {i}. {t} ({count} distinct n-grams)")

    def compare_two(self):
        if self.engine is None:
            messagebox.showwarning("Warning", "Initialize engine first")
            return
        
        titles = self.engine.titles
        if len(titles) < 2:
            messagebox.showinfo("Info", "Need at least two documents")
            return
        
        # Create a selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Documents to Compare")
        selection_window.geometry("400x300")
        
        tk.Label(selection_window, text="Select first document:").pack(pady=5)
        var1 = tk.StringVar(selection_window)
        var1.set(titles[0])
        menu1 = tk.OptionMenu(selection_window, var1, *titles)
        menu1.pack(pady=5)
        
        tk.Label(selection_window, text="Select second document:").pack(pady=5)
        var2 = tk.StringVar(selection_window)
        var2.set(titles[1] if len(titles) > 1 else titles[0])
        menu2 = tk.OptionMenu(selection_window, var2, *titles)
        menu2.pack(pady=5)
        
        result = {'done': False}
        
        def compare():
            t1 = var1.get()
            t2 = var2.get()
            if t1 == t2:
                messagebox.showwarning("Warning", "Please select two different documents")
                return
            try:
                score = self.engine.compare_pair(t1, t2)
                self.log(f"Similarity between '{t1}' and '{t2}': {score:.4f}")
                result['done'] = True
                selection_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(selection_window, text="Compare", command=compare).pack(pady=10)
        tk.Button(selection_window, text="Cancel", command=selection_window.destroy).pack(pady=5)

    def most_similar(self):
        if self.engine is None:
            messagebox.showwarning("Warning", "Initialize engine first")
            return
        
        titles = self.engine.titles
        if len(titles) < 2:
            messagebox.showinfo("Info", "Need at least two documents")
            return
        
        t = simpledialog.askstring("Input", f"Enter title from: {titles}")
        if not t or t not in titles:
            messagebox.showerror("Error", "Invalid or missing title")
            return
        
        try:
            best, score = self.engine.find_most_similar(t)
            if best:
                best_str = ", ".join(best)
                self.log(f"Most similar to '{t}': {best_str} (score: {score:.4f})")
            else:
                self.log(f"No other documents to compare with '{t}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def report_pairs(self):
        if self.engine is None:
            messagebox.showwarning("Warning", "Initialize engine first")
            return
        
        if len(self.engine.titles) < 2:
            messagebox.showinfo("Info", "Need at least two documents")
            return
        
        threshold_str = simpledialog.askstring("Input", "Enter threshold (0-1):")
        if not threshold_str:
            return
        
        try:
            thr = float(threshold_str)
            if not (0 <= thr <= 1):
                raise ValueError("Threshold must be between 0 and 1")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        try:
            res = self.engine.report_similar_pairs(thr)
            self.log(f"=== Pairs with similarity ≥ {thr} ===")
            if not res:
                self.log("  (No pairs found above threshold)")
            else:
                for i, (t1, t2, score) in enumerate(res, 1):
                    self.log(f"  {i}. {t1} -- {t2}: {score:.4f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = PlagiarismGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
