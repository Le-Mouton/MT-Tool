import tkinter
import customtkinter
import convert
import re
from PIL import Image
import os
import qrcode
import merge
import save

customtkinter.set_appearance_mode("system")  # Dark ou Light
customtkinter.set_default_color_theme("asset/theme.json")


class MainWindow(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = None
        self.title("MT'Tool")
        self.geometry("400x240")
        self.minsize(400, 240)

        self.iconbitmap('asset/img/logo.ico')

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)  # Important pour `grid`
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WindowHome, WindowConverter, WindowQRCode, WindowMergePDF):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WindowHome)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class WindowHome(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Créer une frame pour les boutons à gauche
        buttons_frame = customtkinter.CTkFrame(self, width=90, height=220)
        buttons_frame.grid(column=0, row=0, sticky="ns", padx=10, pady=10)

        # Créer une frame pour l'image à droite
        image_frame = customtkinter.CTkFrame(self, width=210, height=220)
        image_frame.grid(column=1, row=0, sticky="nesw", padx=10, pady=10)

        # Placer les boutons dans la frame des boutons
        convertButton = customtkinter.CTkButton(buttons_frame,
                                                text="Convertir des fichiers",
                                                command=lambda: self.controller.show_frame(WindowConverter))
        convertButton.pack(pady=10, padx=5, anchor="w", expand=True, fill='x')

        qrcodeButton = customtkinter.CTkButton(buttons_frame,
                                               text="Créer un QRCode",
                                               command=lambda: self.controller.show_frame(WindowQRCode))
        qrcodeButton.pack(pady=10, padx=5, anchor="w", expand=True, fill='x')

        mergePDF = customtkinter.CTkButton(buttons_frame,
                                           text="Fusionner des PDF",
                                           command=lambda: self.controller.show_frame(WindowMergePDF))
        mergePDF.pack(pady=10, padx=5, anchor="w", expand=True, fill='x')


class WindowConverter(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.toConvert = None
        self.filename = None
        self.dirname = None
        self.choice = None

        # Création de l'en-tête
        header_frame = customtkinter.CTkFrame(self)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))

        buttonRetour = customtkinter.CTkButton(header_frame,
                                               text="Retour",
                                               command=lambda: controller.show_frame(WindowHome),
                                               width=100, height=40)
        buttonRetour.pack(side='left')

        pageLabel = customtkinter.CTkLabel(header_frame,
                                           text="CONVERTISSEUR",
                                           width=380,
                                           font=('font', 25))
        pageLabel.pack(side='left', padx=10)

        self.main_frame = customtkinter.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        optionType = customtkinter.CTkOptionMenu(self.main_frame,
                                                 values=["Selectionner un type de fichier", "Images", "Documents",
                                                         "Videos"],
                                                 command=self.optionType_callback,
                                                 width=350)
        optionType.pack(pady=10)
        buttonDirectory = customtkinter.CTkButton(self.main_frame, text="Dossier", command=self.getDirectory)
        buttonDirectory.pack()

        self.buttonFileImage = customtkinter.CTkButton(self.main_frame, text="Images",
                                                       command=self.browseFiles)

        self.buttonFileDocument = customtkinter.CTkButton(self.main_frame, text="Documents",
                                                          command=self.browseFiles)
        self.buttonFileVideo = customtkinter.CTkButton(self.main_frame, text="Videos",
                                                       command=self.browseFiles)
        self.buttonConvert = customtkinter.CTkButton(self.main_frame, text="Convertir",
                                                     command=self.convertCallback)

    def button_function(self):
        print("button pressed")

    def browseFiles(self):
        if self.choice == "Images":
            extension = ".PNG .JPG .JPEG .GIF .webp .pdf .ico"
        if self.choice == "Documents":
            extension = ".docx .docm .dotx .dotm .pdf .xps .rtf .html .htm .mht .txt .xml .odt .doc"
        if self.choice == "Videos":
            extension = ".mp3 .mp4 .mov .gif .avi .mwv .avchd .flv .webm .mkv"

        defaultdir = save.readSave(self.choice) if save.readSave(self.choice) else "/"
        self.filename = tkinter.filedialog.askopenfilenames(initialdir=defaultdir,
                                                            title="Select a File",
                                                            filetypes=((self.choice,
                                                                        f"*{extension}*"),
                                                                       ("Autres",
                                                                        "*.*")))
        self.filename = list(self.filename)

        if self.filename:
            first_file = self.filename[0]
            directory = os.path.dirname(first_file)
            save.appendSave(self.choice, directory)

        # Change label contents
        label = customtkinter.CTkLabel(self.main_frame, text=f"Fichié sélectionné: {self.filename}")
        label.pack()

        extension_list = re.split(" ", extension)

        extension_list.insert(0, "Sélectionnez une extension")

        self.optionToConvert = customtkinter.CTkOptionMenu(self.main_frame,
                                                           values=extension_list,
                                                           command=self.callBack_toConvert)
        self.optionToConvert.pack()

    def getDirectory(self):
        defaultdir = save.readSave("directory") if save.readSave("directory") else "/"
        self.dirname = tkinter.filedialog.askdirectory(initialdir=defaultdir,
                                                       title="Choisissez un dossier", )
        if self.dirname == '':
            self.dirname = defaultdir
        save.appendSave("directory", self.dirname)
        label = customtkinter.CTkLabel(self.main_frame, text=f"Dossier choisit: {self.dirname}")
        label.pack()

    def optionType_callback(self, choice):
        if choice is not None:
            self.buttonFileImage.pack_forget()
            self.buttonFileDocument.pack_forget()
            self.buttonFileVideo.pack_forget()
        self.choice = choice
        if choice == "Images":
            self.buttonFileImage.pack()
        if choice == "Documents":
            self.buttonFileDocument.pack()
        if choice == "Videos":
            self.buttonFileVideo.pack()

    def callBack_toConvert(self, value):
        self.toConvert = value
        self.buttonConvert.pack()

    def convertCallback(self):
        if self.filename and self.dirname and self.toConvert is not None:
            if self.choice == "Images":
                convert.Images(self.filename, self.dirname, self.toConvert)
            if self.choice == "Documents":
                convert.Documents(self.filename, self.dirname, self.toConvert)
            if self.choice == "Videos":
                convert.Videos(self.filename, self.dirname, self.toConvert)


class WindowQRCode(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.dirname = None
        self.controller = controller

        header_frame = customtkinter.CTkFrame(self)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))

        buttonRetour = customtkinter.CTkButton(header_frame,
                                               text="Retour",
                                               command=lambda: controller.show_frame(WindowHome),
                                               width=100, height=40)
        buttonRetour.pack(side='left')

        pageLabel = customtkinter.CTkLabel(header_frame,
                                           text="QRCode",
                                           width=380,
                                           font=('font', 25))
        pageLabel.pack(side='left', padx=10)

        self.main_frame = customtkinter.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        buttonDirectory = customtkinter.CTkButton(self.main_frame, text="Dossier", command=self.getDirectory)
        buttonDirectory.pack()
        self.inputLink = customtkinter.CTkEntry(self.main_frame,
                                                placeholder_text="Copier coller votre lien ici...")
        self.inputLink.pack()

        buttonCreate = customtkinter.CTkButton(self.main_frame,
                                               text="Créer le QRCode",
                                               command=self.create_callback)
        buttonCreate.pack()

    def create_callback(self):
        if self.inputLink.get() and self.dirname is not None:
            img = qrcode.make(self.inputLink.get())
            img.save(f"{self.dirname}/qrcode.png")

            image1 = Image.open(f"{self.dirname}/qrcode.png")
            image = customtkinter.CTkImage(image1, size=(350, 240))
            image_label = customtkinter.CTkLabel(self.main_frame, image=image, text="")
            image_label.pack(padx=10, pady=10)

    def getDirectory(self):
        defaultdir = save.readSave("directory") if save.readSave("directory") else "/"
        self.dirname = tkinter.filedialog.askdirectory(initialdir=defaultdir,
                                                       title="Choisissez un dossier", )
        if self.dirname == '':
            self.dirname = defaultdir
        save.appendSave("directory", self.dirname)
        label = customtkinter.CTkLabel(self.main_frame, text=f"Dossier choisit: {self.dirname}")
        label.pack()


class WindowMergePDF(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.dirname = None
        self.filename = None
        self.controller = controller

        header_frame = customtkinter.CTkFrame(self)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))

        buttonRetour = customtkinter.CTkButton(header_frame,
                                               text="Retour",
                                               command=lambda: controller.show_frame(WindowHome),
                                               width=100, height=40)
        buttonRetour.pack(side='left')

        pageLabel = customtkinter.CTkLabel(header_frame,
                                           text="FUSIONNEUR",
                                           width=380,
                                           font=('font', 25))
        pageLabel.pack(side='left', padx=10)

        self.main_frame = customtkinter.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        buttonDirectory = customtkinter.CTkButton(self.main_frame, text="Dossier", command=self.getDirectory)
        buttonDirectory.pack()

        self.buttonFile = customtkinter.CTkButton(self.main_frame, text="PDF",
                                                  command=self.browseFiles)
        self.buttonFile.pack()
        buttonCreate = customtkinter.CTkButton(self.main_frame,
                                               text="Fusionner des PDF",
                                               command=self.merge_callback)
        buttonCreate.pack()

    def browseFiles(self):
        defaultdir = save.readSave("pdf") if save.readSave("pdf") else "/"
        self.filename = tkinter.filedialog.askopenfilenames(initialdir=defaultdir,
                                                            title="Select a File",
                                                            filetypes=(('PDF',
                                                                        "*.pdf*"),
                                                                       ("Autres",
                                                                        "*.*")))
        self.filename = list(self.filename)

        if self.filename:
            first_file = self.filename[0]
            directory = os.path.dirname(first_file)
            save.appendSave("pdf", directory)

        # Change label contents
        label = customtkinter.CTkLabel(self.main_frame, text=f"Fichié sélectionné: {self.filename}", wraplength=250, fg_color='#2F4548')
        label.pack(pady=5)

    def merge_callback(self):
        merge.mergePDF(self.filename, self.dirname)

    def getDirectory(self):
        defaultdir = save.readSave("directory") if save.readSave("directory") else "/"
        self.dirname = tkinter.filedialog.askdirectory(initialdir=defaultdir,
                                                       title="Choisissez un dossier", )
        save.appendSave("directory", self.dirname)
        if self.dirname == '':
            self.dirname = defaultdir
        label = customtkinter.CTkLabel(self.main_frame, text=f"Dossier choisit: {self.dirname}", wraplength=250, fg_color='#2F4548')
        label.pack(pady=5)
