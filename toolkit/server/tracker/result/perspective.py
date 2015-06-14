class Perspective(object):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.people_dict = dict()

    def add_person(self, person):
        self.people_dict[person.get_name()] = person

    def get_people(self):
        return self.people_dict


def create(*args):
    return Perspective(*args)
