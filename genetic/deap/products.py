import numpy
import random
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import plotly.express as px


class Product():
    def __init__(self, name, space, price):
        self.name = name
        self.space = space
        self.price = price

products_list = []
products_list.append(Product("Refrigerator A", 0.751, 999.90))
products_list.append(Product("Cell phone", 0.0000899, 2911.12))
products_list.append(Product("TV 55' ", 0.400, 4346.99))
products_list.append(Product("TV 50' ", 0.290, 3999.90))
products_list.append(Product("TV 42' ", 0.200, 2999.00))
products_list.append(Product("Notebook A", 0.00350, 2499.90))
products_list.append(Product("Ventilator", 0.496, 199.90))
products_list.append(Product("Microwave A", 0.0424, 308.66))
products_list.append(Product("Microwave B", 0.0544, 429.90))
products_list.append(Product("Microwave C", 0.0319, 299.29))
products_list.append(Product("Refrigerator B", 0.635, 849.00))
products_list.append(Product("Refrigerator C", 0.870, 1199.89))
products_list.append(Product("Notebook B", 0.498, 1999.90))
products_list.append(Product("Notebook C", 0.527, 3999.00))
spaces = []
prices = []
names = []

for product in products_list:
  spaces.append(product.space)
  prices.append(product.price)
  names.append(product.name)
limit = 3
population_size = 20
mutation_probability = 0.01
number_of_generations = 100 

def fitness(solution):
  cost = 0
  sum_space = 0
  for i in range(len(solution)):
    if solution[i] == 1:
      cost += prices[i]
      sum_space += spaces[i]
  if sum_space > limit:
    cost = 1
  return cost,

toolbox = base.Toolbox()
creator.create('FitnessMax', base.Fitness, weights=(1.0,)) #it is a maximization problem
creator.create('Individual', list, fitness=creator.FitnessMax) #create the list of individuals
#register all the objects ( type of our solution = chromosome )
toolbox.register('attr_bool', random.randint, 0, 1) #initialize the chromosome
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_bool, n=14) #individual component
toolbox.register('population', tools.initRepeat, list, toolbox.individual) #initRepat = random , create the populaiton in here 
toolbox.register('evaluate', fitness) #define how we are going to evaluate the population
toolbox.register('mate', tools.cxOnePoint) # define the crossover with 1 cutoff point
toolbox.register('mutate', tools.mutFlipBit, indpb = 0.05) #bolean mutation, with mutation probability 0.01
toolbox.register('select', tools.selRoulette) #define how we gonna select the best individuals ( roulette -> probabilistic approach )

population = toolbox.population(n = 20)
crossover_probability = 1.0
number_of_generations = 100

statistics = tools.Statistics(key = lambda individual: individual.fitness.values)
statistics.register('max', numpy.max)
statistics.register('min', numpy.min)
statistics.register('med', numpy.mean)
statistics.register('std', numpy.std)


population, info = algorithms.eaSimple(population, toolbox, crossover_probability, mutation_probability,
                                       number_of_generations, statistics)
"""

best_solution = tools.selBest(population,5)

print(best_solution[0].fitness)
print(best_solution)

"""

figure = px.line(x = range(0,101), y = info.select('max'), title = 'Genetic algorithm results')
figure.show()
