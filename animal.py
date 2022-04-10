import uuid 
import datetime 
class Animal: 
    def __init__ (self, species_name, common_name, age): 
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = []
        self.vetting_recorded = []
        self.enclosure = None
        self.care_taker = None

    def feed(self): 
        self.feeding_record.append (datetime.datetime.now())
    def vet(self):
        self.vetting_recorded.append(datetime.datetime.now())
    def menclosure(self,encl): # mother enclosure
        self.enclosure=encl
    def assignEnc(self, enclosure):
        self.enclosure=enclosure
    def assigningCT(self, care_taker):
        self.care_taker = care_taker
class Enclosure:
    def __init__(self,name,space):
        self.enclosure_id = str(uuid.uuid4())
        self.name=name
        self.animals= []
        self.space = space
        self.cleaning_record = []
    def cleaning(self):
        self.cleaning_record.append(datetime.datetime.now())
    def add_animal(self,animal):
        self.animals.append(animal)
        self.space -= 1
    def remove_animal(self,animal):
        self.animals.remove(animal)
class Employee:
    def __init__(self, name, address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = [] # taking care of animal
        self.employees = {} # for stats
        self.employees[self.employee_id] = len(self.animals)

    def takeCare(self, animal):
        self.animals.append(animal)

    def minc(self):
        x=min(self.employees)
        return x
    def maxc(self):
        x=max(self.employees)
        return x
    def avgc(self):
        avgList = []
        for k, v in self.employees.items():
            avgList.append(sum(v) / float(len(v)))
        return avgList
