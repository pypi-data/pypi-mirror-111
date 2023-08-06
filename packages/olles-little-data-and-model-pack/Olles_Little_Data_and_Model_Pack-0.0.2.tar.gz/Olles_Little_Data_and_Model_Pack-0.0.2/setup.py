from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Olles_Little_Data_and_Model_Pack',
    version='0.0.2',
    description='R Passenger dataset but in list and Pandas format. Will later include time series models (will be added later).',
    py_modules='olles_little_data_and_model_pack',
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown"
    )