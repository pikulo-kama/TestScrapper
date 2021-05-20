import re
from copy import deepcopy
from typing import Dict, List

import pycountry

from abstract.pdf import DataEntryMapper
from models import PersonDetails, DataEntry


class DataEntryMapperImpl(DataEntryMapper):
    DATA_ENTRY_REGEX_PATTERN = re.compile("\n?(?P<sessionName>P\\d{3})\\s+" +
                                          "(?P<topicTitle>[^a-z]*?)(?=[A-Z][a-zå])" +
                                          "(?P<names>.+?[a-z0-9]\n)" +
                                          "(?P<locations>.+?[a-zA-Z]\n)?" +
                                          "(?P<abstract>.*)", flags=re.RegexFlag.S)

    def map(self, record: str) -> List[DataEntry]:
        """
        Extract names and locations and map data entry for each people mentioned in block.
        :param record:
        :return:
        """
        dataEntries = []

        match = DataEntryMapperImpl.DATA_ENTRY_REGEX_PATTERN.match(record)

        generalDataEntry = self._buildGeneralDataEntry(match.groupdict())
        detailsCollection = self._formatPersonDetails(match['names'], match['locations'])

        for details in detailsCollection:
            dataEntry = deepcopy(generalDataEntry)

            dataEntry.name = details.name
            dataEntry.affiliationName = details.affiliationName
            dataEntry.personsLocation = details.location

            dataEntries.append(dataEntry)

        return dataEntries

    @staticmethod
    def _buildGeneralDataEntry(match: Dict[str, str]) -> DataEntry:

        def formatSessionName(sessionName):
            return str(sessionName).strip()

        def formatTopicTitle(title: str):
            topicTitle = re.sub(r"\s+", " ", title)
            return re.sub(r"­\s", "", topicTitle).strip()

        dataEntry = DataEntry()

        dataEntry.topicTitle = formatTopicTitle(match['topicTitle'])
        dataEntry.sessionName = formatSessionName(match['sessionName'])
        dataEntry.presentationAbstract = match['abstract']

        return dataEntry

    def _formatPersonDetails(self, names: str, locations: str) -> List[PersonDetails]:

        personDetails = []

        def formatName(_name: str):
            return re.sub(r"-\n\d", "", _name.strip())

        if locations is None:

            for name in names.split(","):
                details = PersonDetails()
                details.name = formatName(name)

                personDetails.append(details)

            return personDetails

        identifiedLocations = {}
        locationMatches = re.finditer(r" ?(?P<id>\d)(?P<content>\D+)", locations)

        if locationMatches:
            for locationMatch in locationMatches:
                locationMatch = locationMatch.groupdict()
                locationMatch['content'] = re.sub("and|-|\n", '', locationMatch['content']).strip(", \n\r\t-")

                identifiedLocations[locationMatch['id']] = locationMatch['content'].strip()

            for name in names.split(","):
                name = name.strip()

                details = PersonDetails()

                if identifiedLocations:
                    locationId = name[-1]
                    name = name[:-1]

                    try:
                        details.affiliationName = identifiedLocations[locationId]
                    except KeyError:
                        details.affiliationName = ""
                else:
                    details.affiliationName = locations.strip()

                details.name = formatName(name)
                details.location = self._extractLocation([details.affiliationName, locations])

                personDetails.append(details)

        else:

            for name in names.split(","):
                details = PersonDetails()
                details.name = formatName(name)
                details.location = self._extractLocation(["", locations])

                personDetails.append(details)

        return personDetails

    def _extractLocation(self, lookupSources: List[str]) -> str:

        for location in lookupSources:

            locationBlock = location[-30:]

            if locationBlock:

                lastTwoWords = locationBlock.split(" ")[-2:]
                lastWord = lastTwoWords[-1]

                for possibleLocation in [' '.join(lastTwoWords), lastWord]:

                    foundCountriesByAlpha2 = None
                    foundCountriesByAlpha3 = None
                    foundCountriesByName = None

                    try:

                        foundCountriesByAlpha2 = pycountry.countries.get(alpha_2=possibleLocation)
                        foundCountriesByAlpha3 = pycountry.countries.get(alpha_3=possibleLocation)
                        foundCountriesByName = pycountry.countries.get(name=possibleLocation)

                    except LookupError as e:
                        print(e)

                    if foundCountriesByAlpha2:
                        return foundCountriesByAlpha2.name

                    if foundCountriesByAlpha3:
                        return foundCountriesByAlpha3.name

                    if foundCountriesByName:
                        return foundCountriesByName.name

        return ""
