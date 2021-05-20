class DataEntry:

    def __init__(self, name: str = '', affiliationName: str = '',
                 personsLocation: str = '', sessionName: str = '',
                 topicTitle: str = '', abstract: str = ''):
        self.__name = name
        self.__affiliationName = affiliationName
        self.__personsLocation = personsLocation
        self.__sessionName = sessionName
        self.__topicTitle = topicTitle
        self.__presentationAbstract = abstract

    @property
    def name(self):
        return self.__name

    @property
    def affiliationName(self):
        return self.__affiliationName

    @property
    def personsLocation(self):
        return self.__personsLocation

    @property
    def sessionName(self):
        return self.__sessionName

    @property
    def topicTitle(self):
        return self.__topicTitle

    @property
    def presentationAbstract(self):
        return self.__presentationAbstract

    @name.setter
    def name(self, value):
        self.__name = value

    @affiliationName.setter
    def affiliationName(self, value):
        self.__affiliationName = value

    @personsLocation.setter
    def personsLocation(self, value):
        self.__personsLocation = value

    @sessionName.setter
    def sessionName(self, value):
        self.__sessionName = value

    @topicTitle.setter
    def topicTitle(self, value):
        self.__topicTitle = value

    @presentationAbstract.setter
    def presentationAbstract(self, value):
        self.__presentationAbstract = value

    def __repr__(self):
        return f"<{self.__name}, {self.__affiliationName}, {self.__personsLocation}, " \
               f"{self.__sessionName}, {self.__topicTitle}, {self.__presentationAbstract[:50]}...>"

    def toArray(self):
        return [self.__name, self.__affiliationName, self.__personsLocation, self.__sessionName, self.__topicTitle,
                self.__presentationAbstract]


class PersonDetails:

    def __init__(self, name: str = '', location: str = '', affiliationName: str = None):
        self.__name = name
        self.__location = location
        self.__affiliationName = affiliationName

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value

    @property
    def affiliationName(self):
        return self.__affiliationName

    @affiliationName.setter
    def affiliationName(self, value):
        self.__affiliationName = value

    def __repr__(self):
        return f"<{self.__name}, {self.__affiliationName}, {self.__location}>"
