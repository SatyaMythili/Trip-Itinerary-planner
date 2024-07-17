from travel_mapper.agent.Agent import Agent
from travel_mapper.routing.RouteFinder import RouteFinder
from travel_mapper.user_interface.utils import (generate_leafmap, validation_message, generate_generic_leafmap)
from travel_mapper.user_interface import utils
from dotenv import load_dotenv
from pathlib import Path
from travel_mapper.user_interface.constants import VALID_MESSAGE
import os
# all import statements


"""load_secrets is used to retrieve API keys such as those for OpenAI and Google Maps"""
def load_secrets():
    load_dotenv()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    open_ai_key = os.getenv("OPENAI_API_KEY")
    google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
    google_palm_key = os.getenv("GOOGLE_PALM_API_KEY")

    return {
        "OPENAI_API_KEY": open_ai_key,
        "GOOGLE_MAPS_API_KEY": google_maps_key,
        "GOOGLE_PALM_API_KEY": google_palm_key,
    }
""" Utilizing environment variables, this Function loads API keys.
It loads variables from a.env file using the dotenv package, 
which is a standard method for securely and modularly handling configuration settings and secrets."""

def assert_secrets(secrets_dict):
    for key in ['OPENAI_API_KEY', 'GOOGLE_MAPS_API_KEY', 'GOOGLE_PALM_API_KEY']:
        assert secrets_dict[key] is not None, f'{key} is missing.'

""" This function verifies that the secrets_dict dictionary contains all required API keys. To make sure that every key is not None, we made use of the Assert statement.
This is a safety measure to make sure the program has all the necessary API keys before it begins carrying out any activities that require them."""



class TravelMapperBase(object):
    def __init__(self, openai_api_key, google_maps_key, google_palm_api_key, verbose=False):
        self.travel_agent = Agent(openai_api_key, google_palm_api_key, debug=verbose)
        self.route_finder = RouteFinder(google_maps_key)
        """ Constructor that sets the verbosity flag and provided API keys to initialize the Agent and RouteFinder."""

    def parse(self, query, make_map=True):
        itinerary, list_of_places, validation = self.travel_agent.suggest_travel(query)
        if make_map:
            directions, sampled_route, mapping_dict = self.route_finder.generate_route(list_of_places, itinerary)
            return itinerary, directions, sampled_route, mapping_dict
        return itinerary, list_of_places, validation
        """ This method receives a trip query, processes it, and returns results pertaining to travel. """



class TravelMapperForUI(TravelMapperBase): # UI Operations
    def _model_type_switch(self, new_model_name):
        current_model_name = self.travel_agent.chat_model.model_name
        if ("gpt" in current_model_name and "gpt" not in new_model_name) or (
            "bison" in current_model_name and "bison" not in new_model_name
        ):

            self.travel_agent.update_model_family(new_model_name)
        elif current_model_name != new_model_name:
            self.travel_agent.chat_model.model_name = new_model_name



    def validate_and_respond(self, query):
        itinerary, validation = self.parse(query, make_map=False)
        return itinerary, utils.validation_message(validation)
        """ Validate query and provide appropriate response."""


    def generate_without_leafmap(self, query, model_name):
        self._model_type_switch(model_name)

        itinerary, list_of_places, validation = self.travel_agent.suggest_travel(query)
            # message validation
        validation_string = validation_message(validation)

        if validation_string != VALID_MESSAGE:
            itinerary = "Itinerary can not be generated, Please check the prompt that you have entered!"

        return itinerary, validation_string

    def generate_with_leafmap(self, query, model_name):
        self._model_type_switch(model_name)

        itinerary, list_of_places, validation = self.travel_agent.suggest_travel(query)

        # message validation
        validation_string = validation_message(validation)

        if validation_string != VALID_MESSAGE:
            itinerary = "Itinerary can not be generated, Please check the prompt that you have entered!!"
            # for a generic map
            map_html = generate_generic_leafmap()

        else:
            (
                directions_list,
                sampled_route,
                mapping_dict,
            ) = self.route_finder.generate_route(
                list_of_places=list_of_places, itinerary=itinerary, include_map=False
            )

            map_html = generate_leafmap(directions_list, sampled_route)

        return map_html, itinerary, validation_string
