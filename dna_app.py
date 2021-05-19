import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

image = Image.open('dna-logo.jpeg')

st.image(image, use_column_width=True)

st.write("""
#DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA

***
""")


st.header('Enter DNA squence')

sequece_input = ">DNA Query 2\nGAACAFDAFASDFSDFSDFSVCXDASFDSADSGSGSG\nDFSAFSFSFSDFSFSFSDFSDFSDFSDFADSAFASDF"

sequece = st.text_area('Sequence input', sequece_input, height=250)

sequece = sequece.splitlines()
sequece = sequece[1:]
sequece = ''.join(sequece)

st.write("""
***
""")

## Print
st.header('Input (DNA Query)')
sequece

## DNA nucleotide Count
st.header('OUTPUT (DNA Nucleotiode Count)')

st.subheader('1. Print dic')
def DNA_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('C', seq.count('C')),
        ('G', seq.count('G')),
        ('F', seq.count('F')),
        ('S', seq.count('S'))
    ])

    return d

X = DNA_nucleotide_count(sequece)
X
st.subheader('2. Print text')

st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')
st.write('There are ' + str(X['T']) + ' thymine (T)')
st.write('There are ' + str(X['G']) + ' guanine (G)')

st.subheader('3. Display dataframe')

df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})

st.write(df)

st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)

p = p.properties(width = alt.Step(100))

st.write(p)