# Zooma Zoo REST API

A REST API for managing a virtual zoo, using the Flask and Flask-RESTx frameworks.

  

Endpoints

1. Animals

* `/animal`: POST request for adding a new animal to the zoo.

* `/animal/<animal_id>`: GET request for retrieving an animal by ID, DELETE request for removing an animal.

* `/animals`: GET request for retrieving all animals in the zoo.

* `/animals/<animal_id>/feed`: POST request for feeding an animal.

* `/animals/<animal_id>/vet`: POST request for providing veterinary care to an animal.

2. Enclosures

* `/enclosure`: POST request for adding a new enclosure to the zoo.

* `/enclosure/<enclosure_id>`: GET request for retrieving an enclosure by ID, DELETE request for removing an enclosure.

* `/enclosures`: GET request for retrieving all enclosures in the zoo.

* `/enclosures/<enclosure_id>/assign`: POST request for assigning an animal to an enclosure.

* `/enclosures/<enclosure_id>/release`: POST request for releasing an animal from an enclosure.

3. Employees

* `/employee`: POST request for adding a new employee to the zoo.

* `/employee/<employee_id>`: GET request for retrieving an employee by ID, DELETE request for removing an employee.

* `/employees`: GET request for retrieving all employees in the zoo.

* `/employees/<employee_id>/assign`: POST request for assigning an animal to an employee for care.

* `/employees/<employee_id>/release`: POST request for releasing an animal from an employee's care.

  

Usage

1. Clone the repository.

2. Install the required libraries using pip.

3. Run python app.py to start the API.

  

# Notes for ZooJsonEncoder Class

This code defines a class called `ZooJsonEncoder` that is a subclass of the built-in `JSONEncoder` class from the `json` library. The `ZooJsonEncoder` class is designed to handle serializing custom data types, such as instances of the built-in `date` class, to a JSON-compatible format.