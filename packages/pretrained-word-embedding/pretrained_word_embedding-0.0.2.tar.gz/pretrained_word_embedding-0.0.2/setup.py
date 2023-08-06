import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pretrained_word_embedding",
    version="0.0.2",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="packages that load pretrained word embeddings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunshu67/pretrained-word-embedding",
    packages=setuptools.find_packages(exclude=["tf_slim*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        
    ],
)
