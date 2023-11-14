"""
Data structure for data in CINI format.
"""
import os
import re
import pandas as pd

class CISIData:
    """
    Data structure consisting in three pandas dataframes containing data in CINI format.
    
    Parameters
    ----------
    path: str
        A path pointing to the folder in which the files are stored.
    """
    def __init__(self, path):
        self.path = os.path.join(path, "")

    def _import_data(self, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            data = file.read()
        return data

    @property
    def documents(self):
        """
        A dataframe containing data about the documents.
        """
        data = self._import_data(self.path + "CISI.ALL")
        raw_docs = [
            re.split(r"\.I\n|\.T\n|\.A\n|\.W\n|\.X\n|\n.T +\n|\n.A +\n|\n.W +\n", d)
            for d in data.split(".I ")
            if d
        ]
        docs = []
        for d in raw_docs:
            d = [s.replace('\n', '') for s in d]
            if len(d) != 5:
                d[2] = ' '.join(d[2:len(d)-2]).replace('\n', '')
            docs.append(
                {
                    "id": int(d[0]),
                    "title": d[1].strip(),
                    "author": d[2].strip(),
                    "text": d[-2].strip(),
                    "related_texts": [
                        tuple(rel.split("\t")) for rel in d[-1].split(" ") if rel
                    ],
                }
            )
        docs = pd.DataFrame(docs)
        return docs

    @property
    def queries(self):
        """
        A dataframe containing data about the queries.
        """
        data = self._import_data(self.path + "CISI.QRY")
        raw_q = [
            re.split(r"\.I |\.T |\.A |\.W |\.X |\.B ", q.replace("\n", " "))
            for q in data.split(".I ")
            if q
        ]
        qs = []
        for q in raw_q:
            if len(q) == 2:
                qs.append(
                    {
                        "id": int(q[0]),
                        "title": pd.NA,
                        "author": pd.NA,
                        "text": q[1].strip(),
                        "book": pd.NA,
                    }
                )
            else:
                qs.append(
                    {
                        "id": int(q[0]),
                        "title": q[1].strip(),
                        "author": q[2].strip(),
                        "text": q[3].strip(),
                        "book": q[4].strip(),
                    }
                )
        qs = pd.DataFrame(qs)
        return qs

    @property
    def relations(self):
        """
        A dataframe containing data about the relations between documents and queries.
        """
        data = self._import_data(self.path + "CISI.REL")
        raw_rels = [line.split("\t")[0].strip() for line in data.splitlines()]
        rels = [re.split(r"\s+", line) for line in raw_rels]
        rels = pd.DataFrame(rels, columns=["query", "document"])
        rels['query'] = rels['query'].astype(int)
        rels['document'] = rels['document'].astype(int)
        return rels
