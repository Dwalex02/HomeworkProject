# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 17:50:59 2022

@author: azenk
"""

class Zoo: 
    def __init__ (self): 
        self.animals = [] 
        
    def addAnimal(self, animal): 
        self.animals.append (animal) 
        
    def removeAnimal(self, animal): 
        self.animals.remove(animal) 
    
    def getAnimal(self, animal_id): 
        for animal in self.animals: 
            if animal.animal_id == animal_id: 
                return animal 