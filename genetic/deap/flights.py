import numpy
import random
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import plotly.express as px

people = [('Lisbon', 'LIS'),
          ('Madrid', 'MAD'),
          ('Paris', 'CDG'),
          ('Dublin', 'DUB'),
          ('Brussels', 'BRU'),
          ('London', 'LHR')]

destiny = 'FCO'

flights = {}

for row in open('flights.txt'):
  #print(row)
  #print(row.split(','))
  origin, destiny, departure, arrival, price = row.split(',')
  #print(origin, destiny, departure, arrival, price)
  flights.setdefault((origin, destiny), [])
  #print(flights)
  flights[(origin, destiny)].append((departure, arrival, int(price)))

schedule_sample = [1,0, 3,2, 7,3, 6,3, 2,4, 5,3]

def fitness_function_deap(schedule):
  flight_id = -1
  total_price = 0
  for i in range(0, 6):
    origin = people[i][1]
    flight_id += 1
    going = flights[(origin, destiny)][schedule[flight_id]]
    total_price += going[2]
    flight_id += 1
    returning = flights[(destiny, origin)][schedule[flight_id]]
    total_price += returning[2]
  
  return total_price,


def print_schedule(schedule):
  flight_id = -1
  total_price = 0
  for i in range(len(schedule) // 2):
    name = people[i][0]
    #print(name)
    origin = people[i][1]
    #print(origin)
    flight_id += 1
    going = flights[(origin, destiny)][schedule[flight_id]]
    #print(going)
    total_price += going[2]
    flight_id += 1
    returning = flights[(destiny, origin)][schedule[flight_id]]
    total_price += returning[2]
    #print('\n')
    print('%10s%10s %5s-%5s %3s %5s-%5s %3s' % (name, origin, going[0], going[1], going[2],
                                                returning[0], returning[1], returning[2]))                                                
  print('Total price:', total_price)


toolbox = base.Toolbox()
creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)
toolbox.register('attr_int', random.randint, a = 0, b = 9)
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_int, n=12)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('evaluate', fitness_function_deap)
toolbox.register('mate', tools.cxOnePoint)
toolbox.register('mutate', tools.mutFlipBit, indpb = 0.01)
toolbox.register('select', tools.selTournament, tournsize=3)

population = toolbox.population(n=500)
crossover_prob = 1
mutation_prob = 0.3
generations = 100


statistics = tools.Statistics(key = lambda individual: individual.fitness.values)
statistics.register('min', numpy.min)


population, info = algorithms.eaSimple(population, toolbox, crossover_prob, mutation_prob,
                                       generations, statistics)


best_solution = tools.selBest(population,1)

print(best_solution[0].fitness)


