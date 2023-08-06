import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
            
    """
    
    #       A binomial distribution is defined by two variables: 
    #           the probability of getting a positive outcome
    #           the number of trials
    
    #       If you know these two values, you can calculate the mean and the standard deviation
    #       
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))
    
    #       
    
    def __init__(self, prob=.5, size=20):
        
        #  store the probability of the distribution in an instance variable p
        self.p = prob
        
        #  store the size of the distribution in an instance variable n
        self.n = size
          
        
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        #       calculate the mean of the Binomial distribution. Store the mean
        #       via the self variable and also return the new mean value
                
        self.mean = self.p * self.n
        
        return self.mean



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        #       calculate the standard deviation of the Binomial distribution. Store
        #       the result in the self standard deviation attribute. Return the value
        #       of the standard deviation.
        
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        
        return self.stdev
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
        
        
        # update size attribute of binomial distribution
        self.n = len(self.data)
        
        # update probability attribute of binomial distribution
        self.p = sum(self.data) / len(self.data)
        
        # update mean attribute of distribution
        self.mean = self.calculate_mean()
        
        # update standard deviation attribute of distribution
        self.stdev = self.calculate_stdev() 
        
        return self.p, self.n
    
   
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
            
        #       Use the matplotlib package to plot a bar chart of the data
        #       The x-axis should have the value zero or one
        #       The y-axis should have the count of results for each case

        
        #       Make sure to label the chart with a title, x-axis label and y-axis label
        
        plt.bar(x=['0','1'], height=[len(self.data) - sum(self.data), sum(self.data)])
        plt.title('Histogram of Data')
        plt.xlabel('data')
        plt.ylabel('frequency')
        plt.show()
        
        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        #  Calculate the probability density function for a binomial distribution
        #  For a binomial distribution with n trials and probability p, 
        #  the probability density function calculates the likelihood of getting
        #  k positive outcomes. 

        
        part1 = self.p**k * (1 - self.p)**(self.n - k)
        part2 = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k))
        
        return part1 * part2

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    
        # Use a bar chart to plot the probability density function from
        # k = 0 to k = n
        
        #   label the bar chart with a title, x label and y label

        #   This method will also return the x and y values used to make the chart
        #   The x and y values should be stored in separate lists
        
        # define lists for x and y values of the bar plot
        x = []
        y = []
        
        # for loop to calculate the pdf at each outcome
        for k in range(0, len(self.n + 1)):
            y.append(self.pdf(k))
            x.append(k)
            
            
        plt.bar(x=x, height=y)
        plt.title('Probability Density Function')
        plt.xlabel('Outcomes')
        plt.ylabel('Probability Density')
        plt.show()
        
        return x, y
        
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        # Define addition for two binomial distributions. Assume that the
        # p values of the two distributions are the same. The formula for 
        # summing two binomial distributions with different p values is more complicated,
        # so you are only expected to implement the case for two distributions with equal p.
        
        # the try, except statement above will raise an exception if the p values are not equal

        
        #   When adding two binomial distributions, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions.
                
        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.mean = self.calculate_mean()
        result.stdev = self.calculate_stdev()
        
        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        
        #       Define the representation method so that the output looks like
        #       mean 5, standard deviation 4.5, p .8, n 20
        #
        #       with the values replaced by whatever the actual distributions values are
        #       The method will return a string in the expected format
    
        return f"mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}"
