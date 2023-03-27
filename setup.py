# from setuptools import setup

# setup(
#     name="james",
#     version="0.1",
#     py_modules=["james"],
#     include_package_data=True,
#     install_requires=["click"],
#     entry_points="""
#         [console_scripts]
#         james=james:cli
#     """,
# )

import os        
from setuptools import setup, find_packages
  
# Load README content         
with open("README.md", "r") as fh:         
    long_description = fh.read()           
  
def read_requirements():      
    """Parse requirements.txt."""          
    with open("requirements.txt") as f:    
        return [dep.strip() for dep in f.read().split("\n") if dep.strip()]         
  
setup(
    name="james",
    version="0.1.0",
    author="Guarilha",
    description="A package to automate daily tasks for software developers using ChatGPT via voice and text",
    long_description=long_description,     
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/james",          
    packages=find_packages(), 
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        james=james:cli
    """,
)   