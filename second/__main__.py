from services import MatchingService


if __name__ == '__main__':
    searches = [] # TODO: read from text file
    properties = [] # TODO: read from json file

    matched_searches = MatchingService(
        searches=searches,
        properties=properties,
    ).match()

    assert matched_searches == [
        'ciudad de méxico/cuauhtémoc',
        'ciudad de méxico/cuauhtémoc/property_type__office,apartment/size__100_200/price__3000000_4000000/bedrooms_2/bathrooms_1',
        'Chihuahua/Chihuahua/property_type__house,office/size__80',
    ]
