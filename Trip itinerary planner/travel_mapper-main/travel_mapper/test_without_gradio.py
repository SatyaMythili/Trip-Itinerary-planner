from travel_mapper.TravelMapper import load_secrets, assert_secrets
from travel_mapper.TravelMapper import TravelMapperBase

""" This function is used to test the TravelMapper application's features without utilizing a GUI """
def test(query=None):
    secrets = load_secrets()
    assert_secrets(secrets)

    default_query = """
        I want to do a 15 days trip from Los Angeles CA to New York City.
        I want to visit national parks and cities with great food.
        I want to use a rental car and drive for no more than 7 hours on any given day.
    """
    query = query if query else default_query

    mapper = TravelMapperBase(
        openai_api_key=secrets["OPENAI_API_KEY"],
        google_maps_key=secrets["GOOGLE_MAPS_API_KEY"],
        google_palm_api_key=secrets["GOOGLE_PALM_API_KEY"],
    )

    mapper.parse(query, make_map=True)


""" loading API keys through the TravelMapper library's load_secrets() function. 
The assert_secrets() function is then used to confirm that these keys are valid.  
A default travel query is used in the absence of a specified query."""