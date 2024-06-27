"""

This file containes the Darwin class. This class containes the logic for the genetic algorithm which tries
to replicate a supplied image using a Voronoi diagram. 

This class takes in 3 required parameters: target_image which is the image you want to replicate, population_size
which is how large you want the population to be (larger populations will have more potential diversity but will take more time)
and num_points which represents the number of points each painting should have.

If this file is run this will create a new Darwin object with a population size of 200 and 500 points per image that
will try to replicate the image at 'Testing Images/original_image.png'.
"""

from painting import Painting
from PIL import Image
from imgcompare import image_diff_percent
import random
import sys
import os


class Darwin:
    def __init__(self, target_image, population_size, num_points):
        """
        Sets the image width and height to the width and height of the target image.
        Creates a random new population of paintings.
        numGenerations represents how many generations the population should evolve for.
        This process takes a long time, usually greater than 5000 generations.   
        """
        self.img_width, self.img_height = target_image.size
        self.population = [Painting(num_points, self.img_width, self.img_height) for _ in range(population_size)]
        self.target_image = target_image
        self.numGenerations = 12000

    def evolve(self):
        # Main Logic for the Evolution Process
        # takes the population, selectively breeds, and mutates the children
        if os.path.exists('checkpoint.txt'):
            gen = self.loadPopulation()
        else:
            gen = 0
        for generation in range(gen + 1, self.numGenerations + 1):
            # sort the population by fitness
            sorted_population, sorted_fitness = self.sortByFitness()
            # this creates a new population
            self.createNewPopulation(sorted_population, generation)
            # in order to view the progress
            print(generation)
            if generation % 10 == 0:
                # every 10 generations it should save the population and update the output file
                self.savePopulation(generation, 'checkpoint.txt')
                self.writeOutputFile(sorted_fitness, sorted_population, generation)

            # this section is for if you want to include steps where the points are doubled or removed
            # change False to True if you want to include these steps.
            if False:
                if generation == 2001:
                    # save the current population
                    self.savePopulation(generation, f'saved_checkpoints/checkpoint_{generation}.txt')
                    # double the genes at generation provided
                    self.doubleGenes()
                    print(len(self.population[0].points))
                if generation == 4001:
                    # remove 100 points from each painting
                    self.removePoints(100)
                    print(len(self.population[0].points))
        pass

    def createNewPopulation(self, sorted_population, generation):
        """
        This method takes in the sorted population and uses it to create a new population.

        sorted_population: a list of Painting objects sorted in ascending order by their fitness value
        """
        new_pop = []
        for _ in range(len(self.population) // 2):
            children = self.createChildren(sorted_population, generation)
            new_pop.append(children[0])
            new_pop.append(children[1])
        # once the length of the new population is the same as the old population
        # set the population to the new population
        if len(new_pop) != len(self.population):
            sys.exit()
        self.population = new_pop
        pass

    def removePoints(self, num_points):
        """
        This method removes a specified number of points from each painting in the population.
        This is used when including point removal steps in the evolution process.

        num_points: an integer representing the number of points to remove
        """
        # removes points from each painting
        for painting in self.population:
            painting.removePoints(num_points)
        pass

    def doubleGenes(self):
        # this function takes each chromosome and doubles the number of genes
        # this is used when including point doubling steps in the evolution process.
        for painting in self.population:
            painting.doublePoints()
        pass

    def createChildren(self, sorted_population, generation):
        """
        This method creates two new children given the sorted population.

        sorted_population: a list of Painting objects sorted in ascending order based on fitness
        """
        parents = self.selectParents(sorted_population)
        children = self.crossover(*parents)
        for child in children:
            # this decreases the probability of mutation
            # if you want to remove this feature change the True to False
            if generation >= 4500 and True:
                child.mutate(prob=0.001)
            else:
                child.mutate()
        return children

    def selectParents(self, sorted_population):
        """
        This function selects two parents (paintings) from the osrted population. Selects paintings with better
        fitness with a higher probability than those with a lower fitness.

        sorted_population: a list of Painting objects sorted in ascending order based on fitness
        """
        # select two parents with a higher likelihood of selecting more fit parents
        weight = [n for n in range(len(self.population))]
        parents = random.choices(sorted_population, weight, k=2)
        return parents

    def fitness(self, painting):
        """
        Returns the similarity in percent which is a value between 0 and 100 with 100 meaning identical images

        painting: a Painting object
        """
        return 100 - image_diff_percent(self.target_image, painting.getImage())
    
    def sortByFitness(self):
        # sorting the paintings based on their fitness
        tuples = [(self.fitness(p), p) for p in self.population]
        tuples = sorted(tuples, key=lambda x: x[0])
        sortedFitnessValues = [fitness for (fitness, painting) in tuples]
        sortedPaintings = [painting for (fitness, painting) in tuples]
        return sortedPaintings, sortedFitnessValues
    
    def crossover(self, parent1, parent2):
        """
        Takes in two parents (Painting objects) and combines points from each.
        Swaps points from the two parents with a probability that is randomly generated.

        parent1: Painting object
        parent2: Painting object
        """
        # generating the probability that any given point is swapped 
        prob = random.random()
        child_one_points = []
        child_two_points = []
        for i in range(len(parent1.points)):
            if random.random() < prob:
                child_one_points.append(parent2.points[i].copy())
                child_two_points.append(parent1.points[i].copy())
            else:
                child_one_points.append(parent1.points[i].copy())
                child_two_points.append(parent2.points[i].copy())
        # set num_points on child to 0 initially, to avoid making 250 random points (saves a little time I think)
        # then set the points to the created list
        child_one = Painting(0, self.img_width, self.img_height)
        child_one.points = child_one_points
        child_two = Painting(0, self.img_width, self.img_height)
        child_two.points = child_two_points

        return child_one, child_two

    def savePopulation(self, generation, filename):
        """
        This function saves the current population and generation to a txt file to allow pausing the process.

        generation: int representing the current generation
        filename: a string representing the name of the txt file you want to save the population to.
        """
        # saves the population as well as the generation to a file
        with open(filename, "w") as file:
            file.write(f'Generation: {generation}\n')
            for painting in self.population:
                file.write(f'{painting.toString()}\n')
        pass

    def loadPopulation(self):
        # Read population data from the file and set it to self.population
        population = []
        with open('checkpoint.txt', "r") as file:
            for line in file:
                # Parse the data from the file and append it to the population list
                painting_string = line.strip()
                if not painting_string.startswith('G'):
                    painting = Painting(painting_string, self.img_width, self.img_height)
                    population.append(painting)
                else:
                    generation = int(line.strip().split(' ')[1])
        
        self.population = population
        # return the generation
        return generation
    
    def writeOutputFile(self, sorted_fitness, sorted_population, generation):
        """
        This function saves the progress of the population. This will append the generation, average fitness, best fitness,
        and the string representation of the best painting to a txt file. This allows the user to track the progress of the
        evolution.

        sorted_fitness: a list of floats which represent the fitness of the population. Sorted in ascending order.
        sorted_population: a list of Painting objects sorted in ascending order by fitness.
        generation: an integer representing the generation the algorithm is currently on.
        """
        # write the generation, average fitness, best fitness, and best strategy
        average_fitness = sum(sorted_fitness) / len(sorted_fitness)
        best_fitness = sorted_fitness[-1]
        best_painting = sorted_population[-1].toString()
        with open('GAOutput.txt', 'a') as file:
            file.write(f'{generation } {average_fitness} {best_fitness} {best_painting}\n')
        pass





if __name__ == '__main__':
    # creates a new darwin object with 200 paintings with 500 points each trying to replicate the image at 
    # Update the filename to match your target image
    original_image_filename = 'original_image.png'

    original = Image.open(f'Testing Images/{original_image_filename}')

    darwin = Darwin(original, 200, 500)
    darwin.evolve()
