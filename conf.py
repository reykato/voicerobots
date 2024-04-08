import os
import sys
sys.path.insert(0, os.path.abspath('./app/src'))

project = 'Voice-controlled Robot with Autonomous Navigation'
copyright = '2024, Japheth Beiler, Tyler Lindsay, Gabriel Marx'
author = 'Japheth Beiler, Tyler Lindsay, Gabriel Marx'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon']


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
