##### Read Geochip GenbankID List
## to build fasta files for each gene. 
## These .fasta files go to KoFamKoala to get KEGG KO numbers 


import sys
from Bio import Entrez

# Tim's magic batch maker
from ibatches import ibatches

Entrez.email = "user@email.www"

gidFile = open("GeochipGenbankIDList.txt","r")
gid = [line.strip() for line in gidFile]

fastaFile = open("GeoID.fasta","w")
#Select Batch size here
for abatch in ibatches(gid, 50):
    print("Fetching", len(abatch), "records")
    handle = Entrez.efetch(db="protein", id=",".join(abatch) , rettype="fasta")

    idx = 0
    for aline in handle:
        aline = aline.rstrip("\n")

        if aline.startswith('>'):
            # Do the results really come back in the right order?
            aline = ">" + abatch[idx] + " " + aline[1:]
            idx += 1

        print(aline, file=fastaFile)


fastaFile.close()
