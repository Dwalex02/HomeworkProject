# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 17:50:59 2022

@author: azenk
"""
from animal import Enclosure

class Zoo: 
    def __init__ (self): 
        self.animals = []
        self.cleaning_plan = {}
        self.all_enclosures= []
        self.all_employees=[]
        
    def addAnimal(self, animal): 
        self.animals.append (animal) 
        
    def removeAnimal(self, animal): 
        self.animals.remove(animal) 
    
    def getAnimal(self, animal_id): 
        for animal in self.animals: 
            if animal.animal_id == animal_id:
                return animal

    def getEncl(self, enclosure_id):
        for e in self.all_enclosures:
            if e.enclosure_id == enclosure_id:
                return e

    def addecnl(self,enclosure):
        self.all_enclosures.append(enclosure)

    def countAnimals(self):
        total={}
        for a in self.animals:
            if a.species_name not in total:
                total[a.species_name] = 0
            total[a.species_name] = 1
            total[a.species_name] = total[a.species_name] + 1
        return total

    def nEnclosures(self):
        total = self.countAnimals()
        x=0
        for i in total.values():
            if int(i) > 1:
                x=x+1
        return x
    def averageAnimals(self):
        if len(self.all_enclosures) > 0:
            avg = len(self.animals) / len(self.all_enclosures)
            return avg

    def removeEnclosure(self, enclosure):
        self.all_enclosures.remove(enclosure)

    def addEmployee(self,employee):
        self.all_employees.append(employee)

    def getEmployee(self, employee_id):
        for e in self.all_employees:
            if e.employee_id == employee_id:
                return e