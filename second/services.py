class MatchingService:
    def __init__(self, searches, properties):
        self.searches = searches
        self.properties = properties

    def match(self):
        matched_searches = []

        for search in self.searches:
            if self.match_search(search):
                matched_searches.append(search)

        return matched_searches

    def match_search(self, search):
        search_params = self.parse_search(search)

        matched_properties = []  # Lista para almacenar propiedades coincidentes

        for property_info in self.properties:
            if self.property_matches_search(property_info, search_params):
                matched_properties.append(property_info)

        if matched_properties:
            # Si hay propiedades coincidentes, formatear la búsqueda coincidente
            matched_search = f"{search_params['state']}/{search_params['city']}/"
            matched_search += "property_type__" + ",".join(search_params['property_type'])
            if search_params['price_min'] is not None or search_params['price_max'] is not None:
                matched_search += f"/price__{search_params['price_min']}_{search_params['price_max']}"
            if search_params['bedrooms'] is not None:
                matched_search += f"/bedrooms_{search_params['bedrooms']}"
            if search_params['bathrooms'] is not None:
                matched_search += f"/bathrooms_{search_params['bathrooms']}"
            if search_params['size_min'] is not None or search_params['size_max'] is not None:
                matched_search += f"/size__{search_params['size_min']}_{search_params['size_max']}"

            return matched_search

        return None

    @staticmethod
    def parse_search(search):
        # Parsear la cadena de búsqueda y extraer parámetros
        search_params = {
            "state": "",
            "city": "",
            "property_type": [],
            "price_min": None,
            "price_max": None,
            "bedrooms": None,
            "bathrooms": None,
            "size_min": None,
            "size_max": None,
        }

        # Dividir la cadena de búsqueda en partes separadas por '/'
        parts = search.split('/')

        # Extraer estado y ciudad (si están presentes)
        search_params["state"] = parts[0]
        search_params["city"] = parts[1]

        # Iterar sobre las partes restantes para extraer otros parámetros
        for part in parts[2:]:
            if '__' in part:
                key, value = part.split('__')
                if key == "property_type" and value in ["HOUSE", "APARTMENT", "WAREHOUSE", "LAND", "OFFICE"]:
                    search_params[key].append(value)
                elif key == "price":
                    min_max = value.split('_')
                    if len(min_max) == 1:
                        search_params["price_max"] = int(min_max[0])
                    elif len(min_max) == 2:
                        search_params["price_min"] = int(min_max[0])
                        search_params["price_max"] = int(min_max[1])
                elif key in ["bedrooms", "bathrooms", "size"]:
                    min_max = value.split('_')
                    if len(min_max) == 1:
                        search_params[f"{key}_min"] = int(min_max[0])
                    elif len(min_max) == 2:
                        search_params[f"{key}_min"] = int(min_max[0])
                        search_params[f"{key}_max"] = int(min_max[1])

        return search_params

    @staticmethod
    def property_matches_search(property_info, search_params):
        # Convertir las ubicaciones a minúsculas para comparaciones insensibles a mayúsculas y minúsculas
        property_state = property_info["state"].lower()
        property_city = property_info["city"].lower()

        search_state = search_params["state"].lower()
        search_city = search_params["city"].lower()

        # Verificar si la ubicación coincide
        if (
            property_state != search_state
            or property_city != search_city
        ):
            return False

        # Verificar el tipo de propiedad (sin importar mayúsculas/minúsculas)
        if (
            not search_params["property_type"]
            or property_info["property_type"].upper() in [
                prop_type.upper() for prop_type in search_params["property_type"]
            ]
        ):
            # Verificar el precio (puede ser mínimo o máximo)
            price_match = (
                (search_params["price_min"] is None or property_info["price"] >= search_params["price_min"])
                and (search_params["price_max"] is None or property_info["price"] <= search_params["price_max"])
            )

            # Verificar el número de recámaras y baños
            bedrooms_match = (
                search_params["bedrooms"] is None or property_info["bedrooms"] == search_params["bedrooms"]
            )
            bathrooms_match = (
                search_params["bathrooms"] is None or property_info["bathrooms"] == search_params["bathrooms"]
            )

            # Verificar el tamaño (puede ser mínimo o máximo)
            size_match = (
                (search_params["size_min"] is None or property_info["size"] >= search_params["size_min"])
                and (search_params["size_max"] is None or property_info["size"] <= search_params["size_max"])
            )

            # Devolver True si todos los criterios coinciden
            return price_match and bedrooms_match and bathrooms_match and size_match

        return False


