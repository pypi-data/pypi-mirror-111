from setuptools import setup

setup(name='gaussian_binomial_dist_test',
      version='0.1',
      description='Gaussian distributions',
      packages=['gaussian_binomial_dist_test'],
      author = 'Tran Nguyen',
      code_source = 'Udacity',
      zip_safe=False) # package can't be run directly from a zip file since data files need to be unzipped for use

