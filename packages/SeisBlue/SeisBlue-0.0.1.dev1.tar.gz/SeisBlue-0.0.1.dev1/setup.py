"""
SeisBlue - Deep learning seismic phase picking project
"""
import setuptools

version = '0.0.1'
dev_version = version + '.dev1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='SeisBlue',
    packages=['seisblue'],
    version=dev_version,
    description='Deep learning seismic phase picking project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='jimmy',
    author_email='jimmy60504@gmail.com',
    url='https://github.com/SeisBlue/SeisBlue',
    python_requires='>=3.6',
    install_requires=[
        "obspy",
        "SQLAlchemy",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 2 - Pre-Alpha"
    ]
)
