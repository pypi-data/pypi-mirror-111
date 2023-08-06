
# Binomial and Gaussian Distributions

binomial_gaussian_distributions_kb is a Python library for calculating and visualizing Binomial and Gaussian distributions.  The package can do the following:
 * calculate the mean
 * calculate the standard deviation
 * calculate the probability density function
 * plots a histogram of the distribution
 * plots the probability density function of the distribution as a histogram
 * adds two distributions
 * read in a file containing a distribution (one element per line in the file)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install binomial_gaussian_distributions_kb.

```bash
pip install binomial_gaussian_distributions_kb
```

## Usage

How to use the binomial distribution class

```python
import binomial_gaussian_distributions_kb

# instantiate a binomial distribution
distribution = Binomial(mean, sample_size)

# binomial distributions mean, standard deviation and histogram
distribution.calculate_mean()
distribution.calculate_stdev()
distribution.plot_bar()

# read a file with a distribution
# one number per line in the file
distribution.replace_stats_with_data(file)

# probability density function calculator
# k is point for calculating the probability density function
distribution.pdf(k)

# plot a bar chart of the probability density function
distribution.plot_bar_pdf()

# add two binomial distributions
distribution1 + distribution2

```
How to use the Gaussian distribution class

```python
import binomial_gaussian_distributions_kb

# instantiate a Gaussian distribution
distribution = Gaussian(mean, standard_deviation)

# Guassian distribution mean
distribution.calculate_mean()

# Gaussian distribution standard deviation
# sample=True indicates that data is a sample of population
# sample=False indicates that data is the population
distribution.calculate_stdev(sample=True)

# Gaussian distribtution histogram
distribution.plot_histogram()

# Gaussian distribution probability density function at point x
distribution.pdf(x)

# Gaussian distribution normalized histogram plot with probability density function on the same range
# number_spaces is the number of data points
distribution.plot_histogram_pdf(number_spaces)

# read a file with a distribution
# one number per line in the file
distribution.replace_stats_with_data(file)

# add two binomial distributions
distribution1 + distribution2
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)

## Latest Release
Latest version is 1.0.1 released 2019-06-29

## Contact the Maintainer
kennybcuz@gmail.com