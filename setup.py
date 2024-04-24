from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
    
setup (
    name="dspwava",
    version="0.0.10",
    description="A simple package containing signal processing abstracitons",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snhig/DiscreteWAVAnalyzer",
    author="Sean Higley",
    author_email="s_higley@u.pacific.edu",
    license="N/A",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy >= 1.24.2",
                      "pyqtgraph >= 0.13.3",
                      "PySide6 >= 6.5.1",
                      "PySide6_Addons >= 6.5.1",
                      "PySide6_Essentials >= 6.5.1",
                      "scipy >= 1.13.0",
                      "setuptools >= 69.0.3",
                      "soundfile==0.12.1" 
                      ],
    python_requires='>=3.8',
   
)