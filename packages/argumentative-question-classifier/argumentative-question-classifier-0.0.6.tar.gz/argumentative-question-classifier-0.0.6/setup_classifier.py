
import setuptools
import pkg_resources

#version = pkg_resources.require("sklearn_esa")[0].version
#ver, rev_1, rev_2 = version.split('.')
#new_version = ver + '.' + rev_1 +"." + str(int(rev_2)+1)

new_version= '0.0.6'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    py_modules=['argumentative_question_classifier'],
    name = "argumentative-question-classifier",
    version = new_version,
    author = "Yamen Ajjour",
    author_email = "yajjour@hotmail.com",
    description = "question classifier for argumentative questions in python.",
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    install_requires =["scikit-learn==0.23.1", 'spacy==3.0.5','pickle'],
)
