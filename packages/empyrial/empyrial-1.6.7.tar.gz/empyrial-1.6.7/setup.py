from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='empyrial',
    version='1.6.7',
    description='AI and data-driven quantitative portfolio management for risk and performance analytics',
    py_modules=['empyrial'],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ssantoshp/Empyrial',
    author="Santosh Passoubady",
    author_email="santoshpassoubady@gmail.com",
    license='MIT',
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas_datareader',
        'datetime',
        'empyrical',
        'quantstats',
        'yfinance',
        #'yahoo-fin',
        #'yahoofinancials',
        'pyportfolioopt',
        'ipython'

    ],
)
