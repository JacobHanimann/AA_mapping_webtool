from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_caching import Cache
from Visualise_Alignment import *
from Alignment import *
import pickle
from Gene import *
from Protein_isoform import *
import sys
# insert at position 1 in the path, as 0 is the path of this file.
#sys.path.insert(1, '../')
import sys
from Gene import *
from Protein_isoform import *
from Streamlit_community import *
from Input_flow import *
from Streamlit_Pop_ups import *
from Alignment import *
from Visualise_Alignment import *
from User_Input_Preparation import *
from Input_flow import *
from Table_Generation import *
from PIL import Image
from Statistics import *

class Data_processing():
    pass

    @staticmethod
    def align_sequences(input1, input2):
        needleman_mapped = Alignment.map_AA_Needleman_Wunsch_with_exon_check(input1, input2, 1, -2, -1.75, 0, 5)
        isoform_pattern_check, alignment_reference_fasta, alignment_isoform_fasta = needleman_mapped[4:7]
        percentage_reference, percentage_isoform = Visualise_Alignment.calculate_percentage_of_mapped_positions(isoform_pattern_check, input1, input2)
        alignment_string = Visualise_Alignment.visualise_alignment_dynamically(alignment_reference_fasta,alignment_isoform_fasta,isoform_pattern_check,percentage_reference, percentage_isoform)
        return alignment_string

    @staticmethod
    def search_and_generate_nested_dict(ID_to_search, list_of_gene_objects):
        dict_of_IDs = Input_preparation.identify_IDs_from_user_text_input(ID_to_search)
        gene_index = Input_flow.search_through_database_with_known_ID_Type(list_of_gene_objects, dict_of_IDs)
        verified_gene_index = Input_flow.remove_dict_elements_with_no_gene_object_match(gene_index)
        if not verified_gene_index:
            return None
        nested_dict = Input_flow.generate_nested_dictionary_with_index_of_canonical_protein_object(dict_of_IDs,verified_gene_index,list_of_gene_objects)
        return nested_dict

    @staticmethod
    def create_mapping_table_of_two_IDs(list_of_gene_objects,index_gene_object,index_of_reference_transcript,index_of_alternative_transcript,chosen_columns, match, mismatch,open_gap_penalty, gap_extension_penalty,exon_length_AA):
        pass