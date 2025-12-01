# main.py
import os
from lab import load_lab

def run_labs(path):
    """
    Accepts either:
        - a single PDF file path
        - a directory containing multiple lab PDFs
    Returns:
        list of parsed lab objects
    """
    if os.path.isfile(path):
        lab = load_lab(path).parse()
        return [lab]

    labs = []
    if os.path.isdir(path):
        for filename in sorted(os.listdir(path)):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(path, filename)
                lab = load_lab(pdf_path).parse()
                labs.append(lab)

    return labs

def main():
    # TODO:
    #   Replace this with an input with a loop:
    #   For now, we use hard-coded paths so TDD can run.
    option = 1
    match option:
      case 1:  
        example_single_file = "labs/lab1.pdf"
        path_to_process = example_single_file
      case _:
        example_folder = "labs/"
        path_to_process = example_folder   
    
    labs = run_labs(path_to_process)

    for lab in labs:
      print(lab)

if __name__ == "__main__":
    main()
