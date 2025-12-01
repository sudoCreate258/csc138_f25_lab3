import os
from pypdf import PdfReader

class BaseLab:
    def __init__(self, lab_number, file_path):
        self.lab_number = lab_number
        self.file_path = file_path
        self.text = ""
        self.github_user = None
        self.commit_hash = None

    def parse(self):
        reader = PdfReader(self.file_path)
        pages = [page.extract_text() or "" for page in reader.pages]
        self.text = "\n".join(pages)

        self._extract_github_fields()
        return self

    def _extract_github_fields(self):
        for line in self.text.splitlines():
            l = line.lower()
            if "username" in l:
                self.github_user = line.split(":")[-1].strip()
            if "hash" in l:
                self.commit_hash = line.split(":")[-1].strip()

    def __str__(self):
        return (
            f"Lab {self.lab_number}\n"
            f"  GitHub Username: {self.github_user}\n"
            f"  Commit Hash:     {self.commit_hash}\n"
            f"  Summary Length:  {len(self.text)} characters"
        )

class Lab0(BaseLab):
    def contains_image(self):
        reader = PdfReader(self.file_path)
        for page in reader.pages:
            resources = page.get('/Resources', {})
            xobj = resources.get('/XObject', {})
            if hasattr(xobj, "keys"):
                for name in xobj.keys():
                    obj = xobj[name]
                    if obj.get("/Subtype") == "/Image":
                        return True
        return False

    def __str__(self):
        base = super().__str__()
        return (
            f"Lab0 Special:    Image Detected = " + {str(self.contains_image()} 
            f"  Summary Length:  {len(self.text)} characters"
        )

def load_lab(pdf_path):
    filename = os.path.basename(pdf_path)
    name = os.path.splitext(filename)[0]

    try:
        lab_num = int(name[3:])
    except:
        raise AssertionError(f"Invalid filename (expected labN.pdf): {filename}")

    if lab_num == 0:
        return Lab0(lab_num, pdf_path)
    return BaseLab(lab_num, pdf_path)
