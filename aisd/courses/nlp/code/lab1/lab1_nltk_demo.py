"""
Lab 1 Part 1: NLTK Demo

Environment Setup:
    1. Create conda environment:
       conda create -n myenv python=3.10
       conda activate myenv
    
    2. Install libraries:
       conda install numpy
       conda install -c conda-forge matplotlib
       conda install pandas
       conda install -c conda-forge statsmodels
       conda install -c anaconda scikit-learn
       conda install -c anaconda scipy
    
    3. Install NLTK:
       conda install -c anaconda nltk
    
    4. Download NLTK data:
       python
       >>> import nltk
       >>> nltk.download()  # Click Download button in the window
       >>> exit()

Reference: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
"""

import nltk
from nltk.corpus import brown

print(brown.words())
