from setuptools import setup, find_packages
setup(name="trading-research-workbench",version="0.2.0",packages=find_packages(),
      python_requires=">=3.10",install_requires=["numpy>=1.26,<3","pandas>=2,<3","scipy>=1.11,<2","statsmodels>=0.14,<1"],
      extras_require={"live":["yfinance>=0.2"]},
      entry_points={"console_scripts":["trading-research=research.workbench:main"]})
