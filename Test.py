import pytest
from animal import Animal, Enclosure, Employee
from zoo import Zoo


@pytest.fixture
def tiger1 ():
    return Animal ("tiger", "ti", 12)

@pytest.fixture
def tiger2 ():
    return Animal ("tiger2", "ti", 2)

@pytest.fixture
def enclosure1 ():
    return Enclosure ("Eden", 5)

@pytest.fixture
def enclosure2 ():
    return Enclosure ("Utopia", 3)

@pytest.fixture
def employee1 ():
    return Employee ("George", "Sofia")

@pytest.fixture
def employee2 ():
    return Employee ("Alex", "Plovdiv")

@pytest.fixture
def zoo1 ():
    return Zoo ()


def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert (tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)

    assert (len(zoo1.animals)==2)

def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    tiger1.feed()

    assert (len(tiger1.feeding_record)==1)

def test_allAnimals(zoo1):
    assert (type(zoo1.animals)==list)

def test_animalID(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    search_result  = zoo1.getAnimal(tiger1.animal_id)
    assert (search_result.age == 12)
    assert (len(search_result.animal_id) > 0)
    assert (search_result.common_name == "ti")
    assert (search_result.species_name == "tiger")

def test_animalID2(zoo1, tiger1): #remove animals
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)

    zoo1.removeAnimal(tiger2)
    assert (len(zoo1.animals)==1)

def test_vetAnimal(tiger1, tiger2):
    tiger1.feed()
    tiger2.feed()
    tiger2.feed()
    assert (len(tiger1.feeding_record) == 1)
    assert (len(tiger2.feeding_record) == 2)

def test_enclosure(zoo1, enclosure1):
    zoo1.addecnl(enclosure1)
    assert (enclosure1 in zoo1.all_enclosures)
    zoo1.addecnl(enclosure2)

    assert (len(zoo1.all_enclosures)==2)

def test_homeAnimal(zoo1, enclosure1, tiger1):
    zoo1.addecnl(enclosure1)
    tiger1.assignEnc(enclosure1.enclosure_id)
    assert(tiger1.enclosure!= None)

def test_animalBirth(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    for a in zoo1.animals:
        if tiger1.animal_id == a.animal_id: # checks if the parameters are the same
            assert(tiger1.enclosure == a.enclosure)
            assert(tiger1.species_name == a.species_name)
            assert(tiger1.common_name == a.common_name)

def test_animalDeath(zoo1, tiger1, tiger2, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)

    enclosure1.add_animal(tiger2)

    zoo1.removeAnimal(tiger2)
    assert (len(zoo1.animals)==1)

    enclosure1.remove_animal(tiger2) #this line is taken from the code and checks if the animal is removed from the
    #enclosure, too
    assert (len(enclosure1.animals)==0)

def test_listOfEnclosures(zoo1):
    assert (type(zoo1.all_enclosures) == list)

def test_cleanEnclosure(enclosure1, enclosure2):
    enclosure1.cleaning()
    enclosure2.cleaning()
    enclosure2.cleaning()
    assert (len(enclosure1.cleaning_record) == 1)
    assert (len(enclosure2.cleaning_record) == 2)

def test_animalsInEnclosure(enclosure1):
    assert (type(enclosure1.animals == list))

def test_deleteEnclosure(zoo1, enclosure1):
    zoo1.addecnl(enclosure1)
    zoo1.addecnl(enclosure2)

    zoo1.removeEnclosure(enclosure2)
    assert (len(zoo1.all_enclosures)==1)

def test_addEmployee(zoo1, employee1):
    zoo1.addEmployee(employee1)
    assert (employee1 in zoo1.all_employees)
    zoo1.addEmployee(employee2)

    assert (len(zoo1.all_employees) == 2)

def test_takeCare(zoo1, employee1, employee2, tiger1, tiger2):
    if tiger1.care_taker != None: # if the animal has no caretaker (because an animal can't have 2 caretakers)
        employee1.takeCare(tiger1)
        assert (len(employee1.animals)==1)
    if tiger2.care_taker != None:
        employee1.takeCare(tiger2)
        assert (len(employee1.animals)==2)
    if tiger1.care_taker != None: # here I check if the programme lets you assign 2 caretaker to 1 animal)
        employee2.takeCare(tiger1)
        assert (len(employee2.animals)==0)
        #well you cannot

def test_caringForAnimalsList(employee1, tiger1, tiger2):
    employee1.takeCare(tiger1)
    employee1.takeCare(tiger2)
    assert (type(employee1.animals)==list)
    assert (len(employee1.animals)==2)

def test_deletingEmployee(zoo1, employee1):
    zoo1.addEmployee(employee1)
    zoo1.addEmployee(employee2)

    zoo1.removeEmployee(employee2)
    assert(len(zoo1.all_employees)==1)

def test_cleaningTask(zoo1):
    zoo1.generate_cp()
    assert (len(zoo1.cleaning_plan)==1)
    zoo1.generate_cp()
    assert (len(zoo1.cleaning_plan) == 2)

def test_medicalTask(zoo1):
    zoo1.generate_mp()
    assert (len(zoo1.medical_plan)==1)
    zoo1.generate_mp()
    assert (len(zoo1.medical_plan)==2)

def test_feedingTask(zoo1):
    zoo1.generate_fp()
    assert (len(zoo1.feeding_plan)==1)
    zoo1.generate_fp()
    assert (len(zoo1.feeding_plan)==2)