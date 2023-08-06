from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='olles_little_data_and_model_pack',
    version='0.0.3',
    description='R Passenger dataset but in list and Pandas format. Will later include time series models (will be added later).',
    py_modules='olles_little_data_and_model_pack',
    #package_dir={'':'src'},
    package_dir=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown"
    )