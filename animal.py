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
        # add more as required here 
        
    # simply store the current system time when this method is called    
    def feed(self): 
        self.feeding_record.append (datetime.datetime.now())
    def vet(self):
        self.vetting_recorded.append(datetime.datetime.now())
    def menclosure(self,encl):
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
        self.cleaningRecording = []
    def cleaning(self):
        self.cleaningRecording.append(datetime.datetime.now())
    def add_animal(self,animal):
        self.animals.append(animal)
    def remove_animal(self,animal):
        self.animals.remove(animal)

class Employee:
    def __init__(self, name, address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = [] # taking care of animal
    def takeCare(self, animal):
        self.animals.append(animal)


            

    
