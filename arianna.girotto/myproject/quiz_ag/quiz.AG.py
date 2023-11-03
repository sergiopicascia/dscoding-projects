import pandas as pd

title_basics = pd.read_csv("//Users/ariannagirotto/Documents/GitHub/dscoding-projects/arianna.girotto/myproject"
                           "/myproject/dataset/title.basics.tsv", sep="\t", quoting=3, encoding='latin-1',
                           engine='python')
ratings = pd.read_csv("//Users/ariannagirotto/Documents/GitHub/dscoding-projects/arianna.girotto/myproject"
                      "/myproject/dataset/ratings.tsv", sep="\t", quoting=3, encoding='latin-1',
                      engine='python')
info_person = pd.read_csv("//Users/ariannagirotto/Documents/GitHub/dscoding-projects/arianna.girotto/myproject"
                          "/myproject/dataset/name.tsv", sep="\t", quoting=3, encoding='latin-1',
                          engine='python')
people = pd.read_csv("//Users/ariannagirotto/Documents/GitHub/dscoding-projects/arianna.girotto/myproject"
                     "/myproject/dataset/crew.tsv", sep="\t", quoting=3, encoding='latin-1',
                     engine='python')