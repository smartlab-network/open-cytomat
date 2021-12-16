from setuptools import setup, find_packages

setup(
    name='cytomat-python',
    version='0.0.1',
    description='Python library to control Thermo Cytomat devices',
    author='Niklas Mertsch',
    author_email='niklas.mertsch@stud.uni-goettingen.de',
    license='MIT',
    python_requires='>=3.7',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pyserial",
        "bitarray",
    ],
    zip_safe=False
)
