from services import MatchingService
import json


if __name__ == '__main__':
    with open('searches.txt', 'r', encoding='utf-8') as file:
        searches = [line.strip() for line in file]
    
    with open('properties.json', 'r', encoding='utf-8') as file:
        properties = json.load(file)

    matched_searches = MatchingService(
        searches=searches,
        properties=properties,
    ).match()

    assert matched_searches == [
        'ciudad de méxico/cuauhtémoc',
        'ciudad de méxico/cuauhtémoc/property_type__office,apartment/size__100_200/price__3000000_4000000/bedrooms_2/bathrooms_1',
        'Chihuahua/Chihuahua/property_type__house,office/size__80',
    ]