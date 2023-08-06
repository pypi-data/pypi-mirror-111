from setuptools import setup

long_description = 'bin-gauss-distributions_kb is a Python library for calculating and visualizing Binomial and Gaussian distributions.  The package calculates the mean, standard deviation, probability density function of a distribution and sums distributions.  The package can read in a distribution from a file.'

setup(name='binomial_gaussian_distributions_kb',
      version='1.0.2',
      description='Binomial and Gaussian distributions',
      packages=['binomial_gaussian_distributions_kb'],
      zip_safe=False,
      author = 'Kenneth Bundy',
      author_email = 'kennybcuz@gmail.com',
      long_description = long_description,
      long_description_content_type = 'text/markdown')
