from PIL import Image
import win32com.client
from moviepy.editor import VideoFileClip
import os


class Images:
    def __init__(self, pathFile, pathDirectory, convert):
        self.pathFile = pathFile
        self.pathDiretory = pathDirectory
        self.convert = convert
        self.path = []
        for i in range(len(self.pathFile)):
            fichier, extension = os.path.splitext(os.path.basename(self.pathFile[i]))
            self.path.append(fichier)

        self.conversion()

    def conversion(self):
        for i in range(len(self.pathFile)):
            image = Image.open(self.pathFile[i])
            if self.convert.lower() in [".jpg", ".jpeg"]:
                if image.mode == "RGBA":
                    image = image.convert("RGB")
            filepath = os.path.join(self.pathDiretory, self.path[i] + self.convert)
            image.save(filepath)


class Documents:
    def __init__(self, pathFile, pathDirectory, convert):
        self.pathFile = [path.replace("/", "\\") for path in pathFile]
        self.pathDirectory = pathDirectory.replace("/", "\\")
        self.convert = convert
        self.path = []
        for i in range(len(self.pathFile)):
            fichier, extension = os.path.splitext(os.path.basename(self.pathFile[i]))
            self.path.append(fichier)
        self.conversion()

    def conversion(self):
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        for i, filepath in enumerate(self.pathFile):
            doc = None
            try:
                doc = word.Documents.Open(filepath)
                filename = self.path[i] + self.convert
                filepath = os.path.join(self.pathDirectory, filename)
                wd_formats = {
                    ".doc": 0,  # wdFormatDocument
                    ".dot": 1,  # wdFormatTemplate
                    ".txt": 2,  # wdFormatText
                    ".rtf": 6,  # wdFormatRTF
                    ".htm": 8,  # wdFormatHTML
                    ".html": 8,  # wdFormatHTML
                    ".docx": 12,  # wdFormatXMLDocument
                    ".docm": 13,  # wdFormatXMLDocumentMacroEnabled
                    ".dotx": 14,  # wdFormatXMLTemplate
                    ".dotm": 15,  # wdFormatXMLTemplateMacroEnabled
                    ".pdf": 17,  # wdFormatPDF
                    ".xps": 18,  # wdFormatXPS
                    ".xml": 11,  # wdFormatXML
                    ".odt": 23,  # wdFormatOpenDocumentText
                }
                number = wd_formats[self.convert]
                doc.SaveAs2(filepath, FileFormat=number)
            finally:
                if doc is not None:
                    doc.Close(False)
        word.Quit()


class Videos:
    def __init__(self, pathFile, pathDirectory, convert):
        self.pathFile = pathFile
        self.pathDirectory = pathDirectory
        self.convert = convert
        self.conversion()

    def conversion(self):
        for filePath in self.pathFile:
            nameFile, _ = os.path.splitext(os.path.basename(filePath))
            outputPath = os.path.join(self.pathDirectory, f"{nameFile}.{self.convert}").replace('\\', '/')

            clip = VideoFileClip(filePath)
            clip.write_videofile(outputPath, codec='libx264')

            print(f"Converted {filePath} to {outputPath}")