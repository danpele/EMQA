"""
emqa_quantlet.py -- one Quantlet per chart of the EMQA decks (same layout as the MFM and SFM courses)
=====================================================================================================
Quantlets/Lk/EMQA_Lk_<chart>/
    Metainfo.txt            QuantLet metadata (name, description, keywords, data, output)
    EMQA_Lk_<chart>.ipynb   self-contained notebook, executed: loads the public data, computes, draws the chart
    <chart>.png             the chart it draws

Rules (see Quantlets/README.md):
* the notebook runs on its own, locally or on Google Colab: no import of the lecture modules, only the code needed
  for that chart; data are read from the course repository (raw GitHub URL), or from data/clean on a local copy;
* the numbers printed by the notebook are those on the slide;
* a frame of a deck links the Quantlets of its charts automatically (lectures/common/emqa_build.py, quantlet_name).

Usage in lectures/Lk/make_quantlets_Lk.py:
    from emqa_quantlet import Quantlet
    q = Quantlet(k=2, chart="naive_mae", description="...", keywords="...", datafile="...")
    q.md("# ...").code("...")
    q.write(execute=True)
"""
import datetime
import os

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
QL_ROOT = os.path.join(ROOT, "Quantlets")
RAW = "https://raw.githubusercontent.com/danpele/EMQA/main/"

# first code cell of every Quantlet: where the data are
DATA_CELL = (
    "import os\n"
    "# course data: the local copy of the repository if there is one, else the public repository on GitHub\n"
    "_LOCAL = os.path.join('..', '..', '..', 'data', 'clean')\n"
    "DATA = _LOCAL + os.sep if os.path.isdir(_LOCAL) else '" + RAW + "data/clean/'\n"
    "REPO = os.path.join('..', '..', '..') + os.sep if os.path.isdir(_LOCAL) else '" + RAW + "'"
)


def _today():
    d = datetime.date.today()
    return d.strftime("%A, %d %B %Y")


class Quantlet:
    def __init__(self, k, chart, description, keywords, datafile, title=None, submitted=None):
        self.k, self.chart = k, chart
        self.name = f"EMQA_L{k}_{chart}"
        self.folder = os.path.join(QL_ROOT, f"L{k}", self.name)
        self.description, self.keywords, self.datafile = description, keywords, datafile
        self.title = title or description
        self.submitted = submitted or _today()
        self.cells = []

    def md(self, text):
        self.cells.append(nbformat.v4.new_markdown_cell(text))
        return self

    def code(self, text):
        self.cells.append(nbformat.v4.new_code_cell(text))
        return self

    def metainfo(self):
        q = lambda s: s.replace("'", "’")
        return (f"Name of QuantLet: '{self.name}'\n\n"
                "Published in: 'Energy Markets Quantitative Analysis (EMQA)'\n\n"
                f"Description: '{q(self.description)}'\n\n"
                f"Keywords: '{q(self.keywords)}'\n\n"
                "Author: 'Daniel Traian Pele'\n\n"
                f"Submitted: '{self.submitted}'\n\n"
                f"Datafile: '{q(self.datafile)}'\n\n"
                f"Output: '{self.chart}.png'\n")

    def write(self, execute=True, timeout=1800):
        os.makedirs(self.folder, exist_ok=True)
        nb = nbformat.v4.new_notebook()
        head = [nbformat.v4.new_markdown_cell(
                    f"# {self.name}\n\n**{self.title}**\n\n"
                    "Energy Markets Quantitative Analysis (EMQA)" + (f", Lecture {self.k}" if self.k else "")
                    + " · Daniel Traian Pele, Bucharest University of Economic Studies\n\n"
                    "[Open in Colab](https://colab.research.google.com/github/danpele/EMQA/blob/main/"
                    + os.path.relpath(self.folder, ROOT).replace(os.sep, "/") + f"/{self.name}.ipynb)"),
                nbformat.v4.new_code_cell(DATA_CELL)]
        nb.cells = head + self.cells
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        if execute:
            ExecutePreprocessor(timeout=timeout, kernel_name="python3").preprocess(nb, {"metadata": {"path": self.folder}})
        with open(os.path.join(self.folder, self.name + ".ipynb"), "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        with open(os.path.join(self.folder, "Metainfo.txt"), "w", encoding="utf-8") as f:
            f.write(self.metainfo())
        if execute and not os.path.isfile(os.path.join(self.folder, self.chart + ".png")):
            raise RuntimeError(f"{self.name}: the notebook did not save {self.chart}.png")
        print("Quantlet", self.name, "written" + (" and executed" if execute else ""))
        return self
