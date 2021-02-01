import streamlit as st
import base64
import os

class Streamlit_community:
    pass

    @staticmethod #not in use
    def get_binary_file_downloader_html(bin_file, file_label='File', name_button='download'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{name_button} {file_label}</a>'
        return href

    @staticmethod
    def get_table_download_link(df, name_of_file="dataframe.tsv", sep='\t'):
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False, sep=sep)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">' + name_of_file + '</a>'
        return href