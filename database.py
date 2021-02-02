import pandas as pd
from functions_old import * #import all functions from the functions_old.py file
from collections.abc import Iterable
import pickle
from Gene import *
from Protein_isoform import *


def add_HCGN_information_to_gene_objects(file_of_gene_names,list_of_gene_objects):
    '''complement list of gene objects
    input: list of gene objects
    output: list of gene objects with added attribute values
    '''
    df = pd.read_csv(file_of_gene_names, sep='\t')
    for index in range(0,80):
        print(index)
        found = False
        for gene in list_of_gene_objects:
            HGNC = df.loc[index, 'HGNC']
            HGNC_gene_symbol = df.loc[index, 'approved_symbol']
            previous_symbols = df.loc[index, 'previous_symbols']
            refseq_gene_ID = df.loc[index, 'NCBI Gene ID']
            alias_symbols = df.loc[index, 'alias_symbols']
            uniprot_ID = df.loc[index, 'UniProt ID']  # check if it the same ID as in the Protein_isoform classes
            if type(previous_symbols) != float:  # None values are type float
                if "," in previous_symbols:
                    previous_symbols = previous_symbols.split(', ')
                else:
                    previous_symbols = [previous_symbols]  # either way create a list because it facilitates later search functions
            if type(alias_symbols) != float:
                if "," in alias_symbols:
                    alias_symbols = alias_symbols.split(', ')
                else:
                    alias_symbols = [alias_symbols]
            if gene.ENSG == df.loc[index,'Ensembl gene ID']:
                  found = True
                  gene.HGNC = HGNC
                  gene.HGNC_gene_symbol = HGNC_gene_symbol
                  gene.previous_symbols = previous_symbols
                  gene.refseq_gene_ID = refseq_gene_ID
                  gene.alias_symbols = alias_symbols
                  gene.uniprot_ID = uniprot_ID #check if it the same ID as in the Protein_isoform classes

        if found == False:
            list_of_gene_objects.append(Gene(df.loc[index,'Ensembl gene ID'],'no HGNC_ensembl match',HGNC=HGNC, HGNC_gene_symbol = HGNC_gene_symbol, previous_symbols = previous_symbols, alias_symbols = alias_symbols, refseq_gene_ID=refseq_gene_ID))

    return list_of_gene_objects


def get_ensembl_fasta_sequences_and_IDs_and_create_gene_objects(file):
    '''extract fasta files one by one and add them to the gene objects'''
    with open(file, "r") as f:
        expenses_txt = f.readlines()
    # Put all the lines into a single string
    whole_txt = "".join(expenses_txt)
    splittext = re.split(">", whole_txt)
    fasta_count = 0
    matches = 0
    list_of_gene_objects =[]
    for fasta in splittext[1:25000]:
        fasta_count += 1
        found = False
        gene_name = get_bio_IDs_with_regex_ensembl_fasta('gene_name',fasta)
        # create Protein_isoform object to add to the gene_object
        sequence_object = Protein_isoform(gene_name, extract_only_AA_of_Fasta_file(fasta.split('\n', 1)[1]),
                                          get_bio_IDs_with_regex_ensembl_fasta('ensembl_ensg', fasta),
                                          get_bio_IDs_with_regex_ensembl_fasta('ensembl_ensg_version', fasta),
                                          get_bio_IDs_with_regex_ensembl_fasta('ensembl_enst', fasta),
                                          get_bio_IDs_with_regex_ensembl_fasta('ensembl_enst_version', fasta),
                                          get_bio_IDs_with_regex_ensembl_fasta('ensembl_ensp', fasta),
                                          get_bio_IDs_with_regex_ensembl_fasta('ensembl_ensp_version', fasta),
                                          uniprot_accession=get_bio_IDs_with_regex_ensembl_fasta(
                                               'uniprot_accession',
                                               fasta),
                                          uniprot_uniparc=get_bio_IDs_with_regex_ensembl_fasta('uniprot_uniparc',fasta))
        for gene in list_of_gene_objects:
            if found:
                break
            if gene.ENSG == sequence_object.ENSG:
                if type(gene.protein_sequence_isoform_collection)==list:
                    gene.protein_sequence_isoform_collection.append(sequence_object)
                else:
                    gene.protein_sequence_isoform_collection = [sequence_object]
                found=True
        if found ==False:
            list_of_gene_objects.append(Gene(sequence_object.ENSG,gene_name,protein_sequence_isoform_collection=[sequence_object]))


        print('Fasta files processed: ' + str(fasta_count) + '/' + str(len(splittext)))
    print('Fasta files matched: ' + str(matches))
    return list_of_gene_objects

#Idea store fasta files that weren't a match also in list_of_gene_objects as Hugo unmatch labeled

def find_gene_objects_that_are_the_same_and_group_together(list_of_gene_objects):
    '''hardcore aligne sequences and check if these are isoforms
    make criteria what counts a isoform
    could also be done with all sequences, would be the most precise method at the beginning of reading fasta files
    also add gene name to the gene object to alias symbols'''

def get_refseq_fasta_sequences_and_IDs(file, list_of_objects):
    'also get refseq data'

    def check_if_IDs_can_be_mapped():
        'before creating new Protein_isoform, check if it already exists'


def get_bio_IDs_with_regex_ensembl_fasta(ID_type,string):
    'generic functions to extract certain ID types from different databases'
    version = False
    #Ensembl
    if ID_type=='ensembl_ensg':
        pattern = 'ENSG\d{11}'
    elif ID_type == 'ensembl_ensg_version':
        pattern = 'ENSG\d+\.\d+'
        version = True
    elif ID_type == 'ensembl_enst':
         pattern = 'ENST\d{11}'
    elif ID_type == 'ensembl_enst_version':
         pattern = 'ENST\d+\.\d+'
         version = True
    elif ID_type == 'ensembl_ensp':
         pattern = 'ENSP\d{11}'
    elif ID_type == 'ensembl_ensp_version':
        pattern = 'ENSP\d+\.\d+'
        version = True

    #Refseq
    elif ID_type=='refseq_rna':
         pattern = 'NM_\d+'
    elif ID_type=='refseq_rna_version':
         pattern = 'NM_\d+\.\d+'
         version = True
    elif ID_type=='refseq_prot':
         pattern = 'NP_\d+'
    elif ID_type=='refseq_prot_version':
        version = True
        pattern = 'NP_\d+\.\d+'

    #Uniprot IDs
    elif ID_type == 'uniprot_accession':
         pattern = '\|[OPQ][0-9][0-9A-Z]{3}[0-9]\||\|[A-NR-Z][0-9][A-Z][A-Z,0-9]{2}[0-9]\||\|[A-N,R-Z][0-9][A-Z][A-Z,0-9]{2}[0-9][A-Z][A-Z,0-9]{2}[0-9]\|'
    elif ID_type == 'uniprot_uniparc':
        pattern = 'UPI[0-9A-F]+'

    if ID_type == "gene_name":
        pattern = "\|[^\|\n]+\n"
        match_list = re.findall(pattern,string)
        if not match_list:  # if list is empty
            return 'not found'
        else:
            #remove \n with regex
            return match_list[0][1:-1] #remove \n

#execute regular expression
    match_list = re.findall(pattern,string)
    if not match_list: #if list is empty
        return 'not found'
    elif len(match_list)==1:
        if ID_type == "uniprot_accession":
            return match_list[0][1:-1]
        else:
            return match_list[0]
    else:
        if version == False:
            return match_list[0]
        else:
            return match_list


def select_canonical_sequence(isoforms):
 'function that can be dynamically applied to a set of isoform sequences'

def save_all_data_in_pickle_style():
    'see if this method is fast enough with streamlit'


def map_isoforms_with_canonical_sequence():
    'I dont know if this makes sense'


def save_results_to_tsv_file(dictionary):
    'to be pre-computed values'



#Execution

list_of_gene_objects = get_ensembl_fasta_sequences_and_IDs_and_create_gene_objects('/Users/jacob/Desktop/Isoform Mapper Webtool/ensembl_fasta_IDs_gene_name.txt')

count = 0
for gene in list_of_gene_objects:
    if len(gene.protein_sequence_isoform_collection) >1:
        print(gene.ensembl_gene_symbol,len(gene.protein_sequence_isoform_collection))
        print(gene.protein_sequence_isoform_collection[0].protein_sequence)
        print(gene.HGNC,gene.alias_symbols)
    if len(gene.protein_sequence_isoform_collection) >=1:
        for sequence in gene.protein_sequence_isoform_collection: #muss man noch verbessern
            if sequence.protein_sequence ==None:
                count +=1
print('could not match protein sequence:',count)

add_HCGN_information_to_gene_objects('/Users/jacob/Desktop/Isoform Mapper Webtool/HGNC_protein_coding_ensembl.txt',list_of_gene_objects)


#save list of gene objects to import to the subsequent script
with open("/Users/jacob/Desktop/Isoform Mapper Webtool/list_of_gene_objects_with_fasta.txt", "wb") as fp:  # Pickling
    pickle.dump(list_of_gene_objects, fp)


for gene in list_of_gene_objects:
    print(gene.HGNC, 'hello',gene.alias_symbols,'well',gene.previous_symbols)