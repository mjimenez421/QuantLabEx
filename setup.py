import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name = "QuantLabEx-Marie-Jimenez",
    version = "0.0.1",
    author = "Marie Jimenez", 
    author_email = "mariemoya99@gmail.com",
    description = "QuantLab SPX",
    long_description = long_desc,
    long_description_content_type = "text",
    url = "https://github.com/mjimenez421/QuantLabEx.git",
    packages = setuptools.find_packages(),
    python_requires='>=3.5',
)
    
