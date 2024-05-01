import customtkinter as ctk

from header_frame import HeaderFrame
from similarities_frame import SimilaritiesFrame
from ontologies_frame import OntologiesFrame
from alignment_frame import AlignmentFrame


class OntolyAlignmentApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Ontology Alignment")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        self.create_header()
        self.create_similarities()
        self.create_ontologies()
        self.create_alignment()

    
    def create_header(self):
        self.headerFrame = HeaderFrame(self.root)
        self.headerFrame.pack()

    def create_similarities(self):
        self.similaritiesFrame = SimilaritiesFrame(self.root)
        self.similaritiesFrame.pack()


    def create_ontologies(self):
        self.ontologiesFrame = OntologiesFrame(self.root)
        self.ontologiesFrame.pack()

    def create_alignment(self):
        self.alignmentFrame = AlignmentFrame(self.root)
        self.alignmentFrame.pack()



if __name__ == "__main__":
    root = ctk.CTk()
    app = OntolyAlignmentApp(root)
    root.mainloop()