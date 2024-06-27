"""
Erik Blix

This file contains the Point class. A point is used in the Voronoi diagram to define the diagram.
Each point has a location (an x and a y coordinate) as well as a color which is the color of the region
surrounding the point. 

The constructor takes in 2 required parameters: img_width and img_height which define the bounds for the location.
The constructor also takes in 1 optional parameter: string which allows the point to be defined by a string rather
than being randomly generated. 

This Point class will be used by the Painting class in order to define the Voronoi diagram.
"""

import random

class Point:
    def __init__(self, img_width, img_height, string=None):
        """
        THIS CONSTRUCTOR IS VERY SIMILAR TO THE CONSTRUCTOR FROM THE POST
        https://blog.4dcu.be/programming/2020/02/10/Genetic-Art-Algorithm-2.html
        """
        self.img_width = img_width
        self.img_height = img_height
        # if the optional string argument is included create the point from the string
        # otherwise create the point randomly
        if string:
            self.x, self.y, self.color = self.createFromString(string)
        else:
            self.x = random.randint(0, int(img_width)) # random x
            self.y = random.randint(0, int(img_height)) #random y
            self.color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), 255) # random rgba value

    def mutate(self):
        """
        THE MUTATE FUNCTION IS NEARLY IDENTICAL TO THE CODE FROM THE POST
        https://blog.4dcu.be/programming/2020/02/10/Genetic-Art-Algorithm-2.html

        This function mutates the point. It either shifts the location of the point or the color.
        For more agressive mutations, increase the movement bound and/or the color_bound variables.
        For less agressive mutations, decrease the movement bound and/or the color_bound variables.
        """
        # two types of mutation: change color or change location
        if random.random() < 0.5:
            movement_bound = 10
            # this is the move mutation
            self.x = self.x + random.randint(-movement_bound, movement_bound)
            self.y = self.y + random.randint(-movement_bound, movement_bound)

        else: # this is the color mutation
            color_bound = 25
            self.color = (self.color[0] + random.randint(-color_bound, color_bound), 
                          self.color[1] + random.randint(-color_bound, color_bound), 
                          self.color[2] + random.randint(-color_bound, color_bound), 
                          255)
            # now we need to verify that the color still falls in the range
            self.color = tuple(
                min(max(c, 0), 255) for c in self.color
            )
        pass

    def copy(self):
        # this method allows a copy to be made of a point object
        # creates a new point object and then changes all of its properties to its own properties
        new_point = Point(self.img_width, self.img_height)
        new_point.x = self.x
        new_point.y = self.y
        new_point.color = self.color
        # returns the copy
        return new_point
    
    def toString(self):
        # string representation of a point object
        result = f'{str(self.x)},{str(self.y)},{str(self.color[0])},{str(self.color[1])},{str(self.color[2])};'
        return result
    
    def createFromString(self, string):
        """
        Take in a string representation of a point and return the parameters from the string.
        """
        items = string.split(',')
        x = int(items[0])
        y = int(items[1])
        color = (int(items[2]), int(items[3]), int(items[4]), 255)
        return x, y, color

        
