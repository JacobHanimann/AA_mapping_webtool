import streamlit as st

class Streamlit_pop_ups:
    pass

    @staticmethod
    def sidebar_pop_up_parameters():
        '''
        sidebar pop up for the parameters of all functions which can be dynamically adjusted.
        '''
        st.sidebar.markdown("### Function Parameters")
        st.sidebar.write("\n")
        st.sidebar.markdown("#### Minimal Exon Length (AA):")
        exon_length_AA = st.sidebar.number_input("", min_value=None, max_value=None, value=5, step=None,
                                                 format=None, key=None)
        st.sidebar.write("\n")
        st.sidebar.markdown("#### Needleman-Wunsch Algorithm:")
        st.sidebar.write("\n")
        match = st.sidebar.number_input("match:", min_value=None, max_value=None, value=1, step=None, format=None,
                                        key=None)
        mismatch = st.sidebar.number_input("mismatch:", min_value=None, max_value=None, value=-2, step=None,
                                           format=None, key=None)
        open_gap_penalty = st.sidebar.number_input("open gap penalty:", min_value=None, max_value=None, value=-1.75,
                                                   step=None, format=None, key=None)
        gap_extension_penalty = st.sidebar.number_input("gap extension penalty:", min_value=None, max_value=None,
                                                        value=0,
                                                        step=None, format=None, key=None)
        st.sidebar.write("\n")

        return match, mismatch, open_gap_penalty, gap_extension_penalty, exon_length_AA