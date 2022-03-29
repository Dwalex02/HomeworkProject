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

@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal (species, name, age) 
        #add the animal to the zoo
        my_zoo.addAnimal (new_animal)
        return jsonify(new_animal) 
    

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result  = my_zoo.getAnimal(animal_id)
        return jsonify(search_result) # this is automatically jsonified by flask-restx
    
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
class VetAnimal(Resource):
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
        old_enclosure = my_zoo.addecnl(targeted_animal.enclosure)
        if old_enclosure != None:
            old_enclosure.removeAnimal(targeted_animal)
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
        mother_animal = my_zoo.getAnimal(mother_id)
        # create a new animal object
        newAnimal = Animal(mother_animal.species_name, mother_animal.common_name, 1)
        newAnimal.menclosure(mother_animal.enclosure)
        enclosure=my_zoo.getEncl(mother_animal.enclosure)
        enclosure.add_animal(newAnimal)
        if not mother_animal:
            return jsonify(f"Animal with ID {mother_id} was not found")
        # add the animal to the zoo
        my_zoo.addAnimal(newAnimal)
        return jsonify(newAnimal)

@zooma_api.route('/animal/death/')
class AnimalDeath(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        animal_id = args['animal_id']
        animal=my_zoo.getAnimal(animal_id)
        my_zoo.removeAnimal(animal)
        return jsonify(f'Animal with ID {animal_id}is removed successfully')

@zooma_api.route('/animals/stat')
class Stats(Resource):
    def get(self):
        stats = {}
        stats['AnimalsPerSpecie'] = my_zoo.countAnimals()
        stats['AverageAnimalsPerEnclosure'] = my_zoo.averageAnimals()
        stats['EnclosuresWithDifferentAnimalSpecies'] = my_zoo.nEnclosures()
        stats['AvailableSpace']=my_zoo.availableSpace()
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
        new_enclosure_id = args['new_enclosure_id']
        targeted_enclosure = my_zoo.getEncl(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        new_enclosure = my_zoo.getEncl(new_enclosure_id)
        if not new_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        new_enclosure.animals=targeted_enclosure.animals
        for animal in new_enclosure.animals:
            animal.enclosure = new_enclosure.enclosure_id
        my_zoo.removeEnclosure(targeted_enclosure)
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
        if targeted_animal.care_taker != None:
            print(f"Animal with ID {animal_id} already has a caretaker")
        else:
            targeted_animal.assigningCT(employee_id)
            caretaker.takeCare(animal_id)
        return jsonify(targeted_animal, caretaker)

@zooma_api.route('/employee/<employee_id>/care/animals')
class CaringForAnimalsList(Resource):
    def get(self, employee_id):
        caretaker = my_zoo.getEmployee(employee_id)
        if not caretaker:
            return jsonify(f"Employee with ID {employee_id} was not found")
        return jsonify(caretaker.animals)



if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)