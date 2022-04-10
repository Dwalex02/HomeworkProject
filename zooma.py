from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo

from animal import Animal, Enclosure, Employee

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True, help='The scientific name of the animal, e,g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')

home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True)

birth_parser = reqparse.RequestParser()
birth_parser.add_argument('mother_id', type=str, required=True)

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True)
enclosure_parser.add_argument('area', type=float, required=True)

death_parser = reqparse.RequestParser()
death_parser.add_argument('animal_id', type=str, required=True)

delencl_parser = reqparse.RequestParser()
delencl_parser.add_argument('new_enclosure_id', type=str, required=True)

employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True)
employee_parser.add_argument('address', type=str, required=True)

delemployee_parser = reqparse.RequestParser()
delemployee_parser.add_argument('new_caretaker_id', type=str, required=True)

@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        new_animal = Animal (species, name, age)
        my_zoo.addAnimal (new_animal)
        return jsonify(new_animal) 
    

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result  = my_zoo.getAnimal(animal_id)
        return jsonify(search_result)
    
     def delete(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} was removed")

@zooma_api.route('/animals')
class AllAnimals(Resource):
     def get(self):
        return jsonify( my_zoo.animals)  
    
     
@zooma_api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):
     def post(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)

@zooma_api.route('/animals/<animal_id>/vet')
class VetAnimal(Resource): #very similar to the feed class
     def post(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.vet()
        return jsonify(targeted_animal)

@zooma_api.route('/enclosure')
class CreateEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']
        new_enclosure = Enclosure(name, area)
        my_zoo.addecnl(new_enclosure)
        return jsonify(new_enclosure)

@zooma_api.route('/animal/<animal_id>/home')
class AnimalHome(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        args = home_parser.parse_args()
        enclosure_id = args['enclosure_id']
        targeted_animal = my_zoo.getAnimal(animal_id)
        targeted_enclosure = my_zoo.getEncl(enclosure_id)
        previous_enclosure = my_zoo.addecnl(targeted_animal.enclosure) # specify the previous enclosure
        if previous_enclosure != None: # removing the animal from the previous enclosure
            previous_enclosure.removeAnimal(targeted_animal)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_animal.assignEnc(targeted_enclosure.enclosure_id)
        targeted_enclosure.add_animal(targeted_animal)
        return jsonify(targeted_animal)

@zooma_api.route('/animal/birth/')
class AnimalBirth(Resource):
    @zooma_api.doc(parser=birth_parser)
    def post(self):
        args = birth_parser.parse_args()
        mother_id = args['mother_id']
        motherAnimal = my_zoo.getAnimal(mother_id)
        newAnimal = Animal(motherAnimal.species_name, motherAnimal.common_name, 0)
        #taking its mother's parameters and born at the age of 0

        #dealing with the enclosure of the new family
        newAnimal.menclosure(motherAnimal.enclosure)
        enclosure=my_zoo.getEncl(motherAnimal.enclosure)
        enclosure.add_animal(newAnimal)
        if not motherAnimal:
            return jsonify(f"Animal with ID {mother_id} was not found")
        my_zoo.addAnimal(newAnimal)
        return jsonify(newAnimal)

@zooma_api.route('/animal/death/')
class AnimalDeath(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        animal_id = args['animal_id']
        animal=my_zoo.getAnimal(animal_id)
        if not animal:
            return jsonify(f"Amimal with ID {animal_id} was not found")
        my_zoo.removeAnimal(animal) # remove the animal
        targeted_enclosure = my_zoo.getEncl(animal.enclosure)
        targeted_enclosure.remove_animal(animal) # remove the animal from the enclosure
        return jsonify(f'Animal with ID {animal_id} is removed')

@zooma_api.route('/animals/stat')
class Stats(Resource):
    def get(self):
        stats = {}
        stats['AnimalsPerSpecie'] =
        stats['AverageAnimalsPerEnclosure'] =
        stats['EnclosuresWithDifferentAnimalSpecies'] =
        stats['AvailableSpace']=  # area divided by number of animals
        return jsonify(stats)

@zooma_api.route('/enclosures')
class ListOfEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.all_enclosures)

@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self,enclosure_id):
        targeted_enclosure = my_zoo.getEncl(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_enclosure.cleaning()
        return jsonify(targeted_enclosure)

@zooma_api.route('/enclosures/<enclosure_id>/animals')
class AnimalsInEnclosure(Resource):
    def get(self,enclosure_id):
        targeted_enclosure=my_zoo.getEncl(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        return jsonify(targeted_enclosure.animals)

@zooma_api.route('/enclosures/<enclosure_id>')
class DeleteEnclosure(Resource):
    @zooma_api.doc(parser=delencl_parser)
    def delete(self, enclosure_id):
        args = delencl_parser.parse_args()
        new_enclosure_id = args['new_enclosure_id'] # assigning the id of the enclosure that we transfer the animals in
        targeted_enclosure = my_zoo.getEncl(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        new_enclosure = my_zoo.getEncl(new_enclosure_id)
        if not new_enclosure:
            return jsonify(f"Enclosure with ID {new_enclosure_id} was not found")
        new_enclosure.animals=targeted_enclosure.animals #transfering
        for animal in new_enclosure.animals: # clear unnecessary data
            animal.enclosure = new_enclosure.enclosure_id
        my_zoo.removeEnclosure(targeted_enclosure) # when we are done transfering, we delete the enclosure
        return jsonify(f"Enclosure with ID {enclosure_id} was removed")

@zooma_api.route('/employee')
class AddEmployee(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):
        args = employee_parser.parse_args()
        name = args['name']
        address = args['address']
        new_employee = Employee(name, address)
        my_zoo.addEmployee(new_employee)
        return jsonify(new_employee)

@zooma_api.route('/employee/<employee_id>/care/<animal_id>/')
class TakeCare(Resource):
    def post(self, employee_id, animal_id):
        caretaker = my_zoo.getEmployee(employee_id)
        if not caretaker:
            return jsonify(f"Employee with ID {employee_id} was not found")
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        if targeted_animal.care_taker != None: # making sure the animal has only 1 caretaker
            print(f"Animal with ID {animal_id} already has a caretaker")
        else:
            targeted_animal.assigningCT(employee_id) # if the condition is met we assign the caretaker to the animal
            caretaker.takeCare(animal_id) # same we add the animal to the caretaker's list
        return jsonify(targeted_animal)

@zooma_api.route('/employee/<employee_id>/care/animals')
class CaringForAnimalsList(Resource):
    def get(self, employee_id):
        caretaker = my_zoo.getEmployee(employee_id)
        if not caretaker:
            return jsonify(f"Employee with ID {employee_id} was not found")
        return jsonify(caretaker.animals)

@zooma_api.route('/employee/stats')
class EmployeeStats(Resource):
    def get(self):
        stats={}
        stats['min'] = Employee.minc()
        stats['max'] = Employee.maxc()
        stats['avg'] = Employee.avgc()
        return jsonify(stats)

@zooma_api.route('/employee/<employee_id>')
class DeleteEmployee(Resource):
    @zooma_api.doc(parser=delemployee_parser)
    def delete(self, employee_id):
        args = delemployee_parser.parse_args()
        new_caretaker_id = args['new_caretaker_id'] # provide a new caretaker
        targeted_caretaker = my_zoo.getEmployee(employee_id)
        if not targeted_caretaker:
            return jsonify(f"Employee with ID {employee_id} was not found")
        new_caretaker = my_zoo.getEncl(new_caretaker_id)
        if not new_caretaker:
            return jsonify(f"Employee with ID {new_caretaker_id} was not found")
        new_caretaker.animals = targeted_caretaker.animals # send the animals to the new caretaker
        for animal in new_caretaker.animals: # getting rid of some unnecessary data
            animal.care_taker = new_caretaker.employee_id
        my_zoo.removeEmployee(targeted_caretaker) # finally remove the employee
        return jsonify(f"Employee with ID {employee_id} was removed")

@zooma_api.route('/tasks/cleaning/')
class CleaningTask(Resource):
    def get(self):
        my_zoo.generate_cp() #more details in the zoo file
        return jsonify(my_zoo.cleaning_plan)

@zooma_api.route('/tasks/medical')
class MedicalTask(Resource):
    def get(self):
        my_zoo.generate_mp()
        return jsonify(my_zoo.medical_plan)

@zooma_api.route('/tasks/feeding')
class FeedingTask(Resource):
    def get(self):
        my_zoo.generate_fp()
        return jsonify(my_zoo.feeding_plan)

if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)