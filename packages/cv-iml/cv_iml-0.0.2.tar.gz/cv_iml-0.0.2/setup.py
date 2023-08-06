import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'IML Computer Vision Library'
LONG_DESCRIPTION = 'cv_iml is a software library written for the IML Lab to reduce the cv_iml redundancy.'

# Setting up
setuptools.setup(
    name="cv_iml",
    version=VERSION,
    author="Qazi Ammar Arshad",
    author_email="<qaziammar.g@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=['opencv-python', 'numpy', 'sklearn', 'matplotlib'],
    keywords=['python', 'image', 'confusion matrix', 'accuracy', 'image parts', ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# For generating the whl file.
# python3.9 setup.py sdist bdist_wheel
# For uploading the file on python page
# twine upload dist/*

