from pysam import VariantFile
import numpy as np
from sklearn import decomposition
import pandas as pd
from tqdm import tqdm

vcf_filename = "ALL.chr22.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz"
panel_filename = "phase1_integrated_calls.20101123.ALL.panel"

genotypes = []
samples = []
variant_ids = []
# Parse the VCF
with VariantFile(vcf_filename) as vcf_reader:
    for record in tqdm(vcf_reader):
        alleles = [record.samples[x].allele_indices for x in record.samples] # extract alleles
        samples = [sample for sample in record.samples] # extract samples
        genotypes.append(alleles)
        variant_ids.append(record.id)

# Extract population codes from the panel file
with open(panel_filename) as panel_file:
    labels = {}  # {sample_id: population_code}
    for line in panel_file:
        line = line.strip().split('\t')
        labels[line[0]] = line[1]

# print(variant_ids)
# genotypes = np.array(genotypes)
# print(genotypes.shape)

# matrix = np.count_nonzero(genotypes, axis=2)

# matrix = matrix.T
# print(matrix.shape)

# pca = decomposition.PCA(n_components=2)
# pca.fit(matrix)
# print(pca.singular_values_)
# to_plot = pca.transform(matrix)
# print(to_plot.shape)

# Convert to dataframe
df = pd.DataFrame(matrix, columns=variant_ids, index=samples)
df['Population code'] = df.index.map(labels) # add in population codes
df.to_csv("matrix.csv")