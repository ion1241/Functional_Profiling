setwd("/path/to/WorkingDir")
REFPATH = "/path/to/Tax4FunDatabase"

library(Tax4Fun2)

# Functional prediction using the representative SV sequences

runRefBlast(path_to_otus = "SWARM_OTUs_curated.fasta", path_to_reference_data = REFPATH, 
            path_to_temp_folder = "Tax4Fun_Ref99NR", database_mode = "Ref99NR",
            use_force = T, num_threads = 16)

makeFunctionalPrediction(path_to_otu_table = "SWARM_table_filtered.tsv", 
                         path_to_reference_data = REFPATH, 
                         path_to_temp_folder = "Mandala_Ref99NR", database_mode = "Ref99NR", 
                         normalize_by_copy_number = T, min_identity_to_reference = 0.97, 
                         normalize_pathways = F)
