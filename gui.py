import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from fileMapper import FileMap
import os


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)  # change to a 2 for multiple monitor resolutions (will cause scaling)
except ImportError:
    pass


class FileMapperFrame(ttk.Frame):
    def __init__(self, parent):

        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

        self.parent = parent
        self.large_btn_width = 50

        self.title = tk.StringVar()
        self.title.set("FileMapper")
        self.using_zip = tk.BooleanVar()
        self.using_zip.set(False)

        self.target_prompt = tk.StringVar()
        self.target_prompt.set("Define Directory to FileMap:")

        self.root_dir = tk.StringVar()
        self.json_path = tk.StringVar()

        self.using_omits = True
        self.using_omits_toggle = tk.StringVar()
        self.using_omits_toggle.set("[TOGGLE] Excluding the following extensions:")
        self.ext_omits = tk.StringVar()
        self.ext_omits_list = []
        self.ext_omits_submitted = tk.StringVar()

        self.status = tk.StringVar()
        self.status.set("Status: Awaiting Generation")

        self.has_generated = False

        self.go_to_file_text = tk.StringVar()
        self.go_to_file_text.set("Open FileMap.json")

        self.init_components()

    def init_components(self):
        self.pack()
        self.init_title_frame()
        self.init_main_frame()
        self.init_omit_frame()
        self.init_generate_frame()
        self.init_output_frame()

    def init_title_frame(self):
        window_name = "FileMapper"
        frame = ttk.Frame(self)
        frame.grid(column=0, row=0, padx=2, pady=2)
        ttk.Label(frame, textvariable=self.title, font=("Arial", 28)).grid(column=0, row=0)
        ttk.Checkbutton(frame, text="Map a Zip", variable=self.using_zip,
                        onvalue=True, offvalue=False, command=self.title_toggle).grid(column=2, row=0, sticky=tk.E)
        self.winfo_toplevel().title(window_name)

    def init_main_frame(self):
        frame = ttk.Frame(self)
        frame.grid(column=0, row=1, padx=2, pady=2)

        entry_width = 65

        ttk.Label(frame, textvariable=self.target_prompt).grid(column=0, row=0, sticky=tk.W)
        ttk.Entry(frame, width=entry_width, textvariable=self.root_dir).grid(column=0, row=1, sticky=tk.W)
        ttk.Button(frame, text="Browse", command=self.get_root_dir).grid(column=1, row=1)

        ttk.Label(frame, text="Define Save Path of FileMap .json file:").grid(column=0, row=3, sticky=tk.W)
        ttk.Entry(frame, width=entry_width, textvariable=self.json_path).grid(column=0, row=4, sticky=tk.W)
        ttk.Button(frame, text="Save As", command=self.get_json_path).grid(column=1, row=4)

        ttk.Label(frame, text="Comma Separated List of Extensions to Filter (such as .txt, .py, .etc):") \
            .grid(column=0, row=6, sticky=tk.W)
        ttk.Entry(frame, width=entry_width, textvariable=self.ext_omits).grid(column=0, row=7, sticky=tk.W)
        ttk.Button(frame, text="Submit", command=self.parse_omits).grid(column=1, row=7)

    def init_omit_frame(self):
        frame = ttk.Frame(self)
        frame.grid(column=0, row=2, padx=2, pady=2)

        ttk.Button(frame, textvariable=self.using_omits_toggle, command=self.omit_filter_toggle) \
            .grid(column=0, row=0, sticky=tk.W)
        ttk.Label(frame, textvariable=self.ext_omits_submitted, width=40).grid(column=1, row=0, sticky=tk.W)

    def title_toggle(self):
        if self.using_zip.get():
            self.title.set("ZipMapper")
            self.target_prompt.set("Define a Zipfile to FileMap:")
        else:
            self.title.set("FileMapper")
            self.target_prompt.set("Define Directory to FileMap:")

    def omit_filter_toggle(self):
        if self.using_omits:
            self.using_omits_toggle.set("[TOGGLE] Including the following extensions:")
            self.using_omits = False
        else:
            self.using_omits_toggle.set("[TOGGLE] Excluding the following extensions:")
            self.using_omits = True

    def get_root_dir(self):
        if self.using_zip.get():
            root_dir = filedialog.askopenfilename(defaultextension=".*", filetypes=[("Zip", "*.zip")])
            self.root_dir.set(root_dir)
        else:
            root_dir = filedialog.askdirectory()
            self.root_dir.set(root_dir)

    def get_json_path(self):
        json_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("JSON", "*.json")])
        self.json_path.set(json_path)

    def parse_omits(self):
        o = self.ext_omits.get()
        o = o.replace(' ', '')
        if o != '':
            self.ext_omits_list = o.split(',')
            omit_text = ''
            for omit in self.ext_omits_list:
                if not omit.startswith('.'):
                    omit = f'.{omit}'
                omit_text += omit
                omit_text += ', '
            omit_text = omit_text[:-2]
            self.ext_omits_submitted.set(omit_text)
        else:
            self.ext_omits_list = []
            self.ext_omits_submitted.set("")

    def init_generate_frame(self):
        frame = ttk.Frame(self)
        frame.grid(column=0, row=3, padx=2, pady=5)

        ttk.Button(frame, width=self.large_btn_width, text="Generate FileMap",
                   command=self.generate).grid(column=0, row=0, pady=5)

    def generate(self):
        if (self.root_dir.get() != "") and (self.json_path.get() != ""):
            self.status.set("Status: RUNNING")

            if self.using_omits:
                #file_map = SmartMapper(self.root_dir.get(),
                #                       extensions2omit=self.ext_omits_list)
                file_map = FileMap(self.root_dir.get(),
                                   extensions2omit=self.ext_omits_list)
            else:
                #file_map = SmartMapper(self.root_dir.get(),
                #                       extensions2include=self.ext_omits_list)
                file_map = FileMap(self.root_dir.get(),
                                   extensions2include=self.ext_omits_list)
            if file_map.exists():
                file_map.export_map_to_json(self.json_path.get())
                self.has_generated = True
                self.status.set("Status: DONE!")
                self.go_to_file_text.set(f'Open {os.path.basename(self.json_path.get())}')
            else:
                self.status.set("STATUS: Can\'t Access Root Dir!")
        elif self.root_dir.get() == "":
            self.status.set("Status: Root Dir Undefined!")
        else:
            self.status.set("Status: JSON Path Undefined!")

    def init_output_frame(self):
        frame = ttk.Frame(self)
        frame.grid(column=0, row=4, padx=2, pady=5)
        ttk.Label(frame, textvariable=self.status, font=("Arial", 24)).grid(column=0, row=0)
        ttk.Button(frame, width=self.large_btn_width,
                   text="Go to Output Directory", command=self.go_to_output_dir).grid(column=0, row=1, pady=8)
        ttk.Button(frame, width=self.large_btn_width,
                   textvariable=self.go_to_file_text, command=self.go_to_file).grid(column=0, row=2, pady=8)

    def go_to_output_dir(self):
        if self.has_generated:
            try:
                os.startfile(os.path.dirname(self.json_path.get()))
            except IsADirectoryError:
                self.status.set("Status: Output Dir Not Found!")

    def go_to_file(self):
        if self.has_generated:
            try:
                os.startfile(self.json_path.get())
            except IsADirectoryError:
                self.status.set("Status: Output File Not Found!")


def main():
    root = tk.Tk()
    FileMapperFrame(root)
    if os.path.exists("FileMapper_icon.ico"):
        root.iconbitmap("FileMapper_icon.ico")
    root.mainloop()


if __name__ == "__main__":
    main()
