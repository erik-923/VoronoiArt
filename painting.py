"""
Erik Blix and Anthony Mozloom

This file contains the Painting class. This class represents an image/Voronoi diagram. A Painting object will be used as an
individual of the population in the Darwin class. Each painting contains a background color, height, width, and an array of
point objects. 

The constructor takes in 3 required parameters: num_points which can either be an int that specifies the number of points it 
should randomly generate, or a string representing a specific painting. It also take in img_width and img_height which will
be the height and width of the painting. 
The constructor takes in one optional parameter: background_color which is the background color of the painting.
"""

from scipy.spatial import Voronoi
from PIL import Image, ImageDraw
import random
from point import Point


class Painting:
    def __init__(self, num_points, img_width, img_height, background_color=(0, 0, 0)):
        """
        THIS CONSTRUCTOR IS VERY SIMILAR TO THE CONSTRUCTOR FROM THE POST
        https://blog.4dcu.be/programming/2020/02/10/Genetic-Art-Algorithm-2.html
        """
        self.img_width, self.img_height = img_width, img_height # get the width and height
        # this allows num_points to either represent a number of randomly generated points
        # or it can be a string representing the specific points
        if type(num_points) == int:
            self.points = [Point(self.img_width, self.img_height) for _ in range(num_points)] # create random list of points
        else:
            self.points = self.createFromString(num_points)
        self.background_color = (*background_color, 255) # unpack color tuple and add alpha value

    def getImage(self):
        """
        This function returns the image representation of the Painting class. Is used to compare to the 
        target image as well as to view an image using pillow.
        """
        vor = Voronoi([(point.x, point.y) for point in self.points])

        # create a blank image with the background color 
        image = Image.new('RGBA', (self.img_width, self.img_height), self.background_color)
        draw = ImageDraw.Draw(image)

        # plot diagram on the image
        for point, region in zip(self.points, vor.regions):
            if -1 not in region and len(region) > 0:
                # use the color associated with the point to draw the polygon representation of the region onto the blank image
                fill_color = point.color
                polygon = [vor.vertices[i] for i in region]
                flat_polygon = [coord for sublist in polygon for coord in sublist]
                draw.polygon(flat_polygon, fill=fill_color)

        return image
    
    def removePoints(self, num_removed):
        """
        This function takes in an int representing the number of points to remove.
        It then randomly removes that many points from the painting.
        This is used in the Darwin function if you want to add steps where points are removed.

        num_removed: this should be an integer representing the number of points to remove.
        """
        if num_removed > len(self.points):
            return
        # choose random indices where points will be removed
        indices = random.sample(range(0, len(self.points)), num_removed)
        new_points = []
        # remove each of these indices from the points
        for i in range(len(self.points)):
            if i not in indices:
                new_points.append(self.points[i])
        self.points = new_points
        pass

    
    def doublePoints(self):
        """
        This function doubles the number of points in the image.
        This is used in the darwin class if you want to start with fewer points
        and double them later on.
        """
        new_points = []
        for point in self.points:
            new_points.append(point.copy())
        for point in self.points:
            new_points.append(point.copy())
        # shuffle the order of the points so that we maximize the effect of mutations
        random.shuffle(new_points)
        self.points = new_points
        pass
    
    def mutate(self, prob=0.005):
        """
        This function mutates the image. It goes through each point and with the probability supplied, mutates the point.
        If you want to define your own probability it should generally be a very small number.

        prob: optional paramter, should be a float between 0 and 1.
        """
        for i in range(len(self.points)):
            if random.random() < prob:
                self.points[i].mutate()
        pass

    def toString(self):
        # generates a string representation of the Painting
        result = ''
        for point in self.points:
            result += point.toString()
        return result
    
    def createFromString(self, string):
        """
        This function takes in a string representation of the Painting and sets all of the variables equal to the
        ones from the string.
        """
        point_strings = string.split(';')
        points = []
        for i in range(len(point_strings) - 1):
            point = Point(self.img_height, self.img_width, point_strings[i])
            points.append(point)
        return points
        

if __name__ == '__main__':
    pass
