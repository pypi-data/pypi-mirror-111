
from setuptools import setup, find_packages

setup(
  name = 'SCALECAST',
  version = '0.1.5',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  short_description = 'A flexible, minimal-code forecasting object.',
  long_description=open('README.md','r',encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author = 'Michael Keith',
  author_email = 'mikekeith52@gmail.com',
  packages=find_packages('src'),
  package_dir={'': 'src'},
  url = 'https://github.com/mikekeith52/scalecast',
  keywords = ['FORECAST', 'SCALE', 'FLEXIBLE'],
  install_requires = [
    'scikit-learn',
    'statsmodels',
    'scipy',
    'eli5',
    'numpy',
    'pandas',
    'scipy',
    'matplotlib',
    'seaborn',
    'xgboost',
    'openpyxl'
  ],
)
