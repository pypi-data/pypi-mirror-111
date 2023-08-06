import setuptools

setuptools.setup(
    name='imblog',
    version='0.2',
    author="hoa",
    author_email="getmoneykhmt3@gmail.com",
    description="A Des of imblog",
    long_description="imblog",
    long_description_content_type="text/markdown",
    url="https://github.com/vtandroid/imblog",
    packages=setuptools.find_packages(),
    py_modules=['imblog'],
    install_requires=[
        'selenium','requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )