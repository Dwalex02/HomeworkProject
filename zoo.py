# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 17:50:59 2022

@author: azenk
"""
import animal
import datetime
from animal import Enclosure, Employee

class Zoo: 
    def __init__ (self): 
        self.animals = []
        self.cleaning_plan = {}
        self.all_enclosures= []
        self.all_employees=[]
        self.cleaning_plan = []
        self.medical_plan = []
        self.feeding_plan = []

    def generate_cp(self):
        if len(self.cleaning_plan) == 0:
            self.cleaning_plan.append(datetime.datetime.now()) # if the plan is empty take today's date
        else:
            self.cleaning_plan.append(self.cleaning_plan[-1] + datetime.timedelta(days=3)) # take the previous date in
            #the list and append it with 3 days after it

    def generate_mp(self):
        if len(self.medical_plan) == 0:
            self.medical_plan.append(datetime.datetime.now())
        else:
            self.medical_plan.append(self.medical_plan[-1] + datetime.timedelta(days=3))

    def generate_fp(self):
        if len(self.feeding_plan) == 0:
            self.feeding_plan.append(datetime.datetime.now())
        else:
            self.feeding_plan.append(self.feeding_plan[-1] + datetime.timedelta(days=3))

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

    def removeEnclosure(self, enclosure):
        self.all_enclosures.remove(enclosure)

    def addEmployee(self,employee):
        self.all_employees.append(employee)

    def getEmployee(self, employee_id):
        for e in self.all_employees:
            if e.employee_id == employee_id:
                return e

    def removeEmployee(self, employee):
        self.all_employees.remove(employee)