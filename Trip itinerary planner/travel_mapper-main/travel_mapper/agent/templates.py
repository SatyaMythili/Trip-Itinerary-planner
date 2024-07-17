from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class Trip(BaseModel):
    start: str = Field(description="start location of trip")
    end: str = Field(description="end location of trip")
    waypoints: List[str] = Field(description="list of waypoints")
    transit: str = Field(description="mode of transportation")


class Validation(BaseModel):
    plan_is_valid: str = Field(
        description="This field is 'yes' if the plan is feasible, 'no' otherwise"
    )
    updated_request: str = Field(description="Your update to the plan")


class ValidationTemplate(object):
    def __init__(self):
        self.system_template = """
      As a travel agent, the model will assist users in creating memorable trip itineraries. 
      Four hashtags will be used to identify the user's request. Assess whether the request is realistic and feasible given the limitations the user has specified.

      Included in a legitimate request should be the following:
      - A start and an end point
      - A acceptable journey time considering the starting and finishing points
      - Additional information, such as the user's hobbies and/or preferred mode of transportation

      Whatever other information is provided, a request that comprises possibly dangerous activity is invalid.

      If the request is not void, set plan_is_valid = 0 and, using your knowledge of travel, amend the request to become void, making sure your updated request is no longer than 100 words.

       If the request seems reasonable, then set plan_is_valid = 1 and don't revise the request.

      {format_instructions}
    """

        self.human_template = """
      ####{query}####
    """

        self.parser = PydanticOutputParser(pydantic_object=Validation)

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template,
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["query"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )


class ItineraryTemplate(object):
    def __init__(self):
        self.system_template = """
      don't revise the request.
As a travel agent, you assist users in creating memorable trip itineraries. 

      Four hashtags will be used to identify the user's request. Transform the user's request into a comprehensive itinerary that lists all the locations and activities they must do. 

      Try to include each location's exact address.

      Always consider the user's preferences and schedule while creating an itinerary for them, making sure it is both enjoyable and practical in light of their limitations.
      
      During the user's trip, try to ensure that they don't have to travel for longer than eight hours in a single day.

      Provide a bulleted list of the itinerary that includes the start and end locations as well as the mode of transportation used for the journey.
     
    """

        self.human_template = """
      ####{query}####
    """

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template,
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["query"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )


class MappingTemplate(object):
    def __init__(self):
        self.system_template = """
      As an agent, you convert complex travel schedules into a straightforward list of destinations.

      Four hashtags will be used to identify the itinerary. Transform it into a list of the locations they ought to go. Try to include each location's exact address.

      The beginning and ending points of the journey should always be included in your output, along with a possible list of checkpoints. It needs to have a means of transportation as well. There can be no more than 20 waypoints in total.
      Given the travel location, estimate the method of transportation if you are unable to determine it.

      For example:

      ####
      Itinerary for a 2-day driving trip within London:
      - Day 1:
        - Start at Buckingham Palace (The Mall, London SW1A 1AA)
        - Visit the Tower of London (Tower Hill, London EC3N 4AB)
        - Explore the British Museum (Great Russell St, Bloomsbury, London WC1B 3DG)
        - Enjoy shopping at Oxford Street (Oxford St, London W1C 1JN)
        - End the day at Covent Garden (Covent Garden, London WC2E 8RF)
      - Day 2:
        - Start at Westminster Abbey (20 Deans Yd, Westminster, London SW1P 3PA)
        - Visit the Churchill War Rooms (Clive Steps, King Charles St, London SW1A 2AQ)
        - Explore the Natural History Museum (Cromwell Rd, Kensington, London SW7 5BD)
        - End the trip at the Tower Bridge (Tower Bridge Rd, London SE1 2UP)
      #####

      Output:
      Start: Buckingham Palace, The Mall, London SW1A 1AA
      End: Tower Bridge, Tower Bridge Rd, London SE1 2UP
      Waypoints: ["Tower of London, Tower Hill, London EC3N 4AB", "British Museum, Great Russell St, Bloomsbury, London WC1B 3DG", "Oxford St, London W1C 1JN", "Covent Garden, London WC2E 8RF","Westminster, London SW1A 0AA", "St. James's Park, London", "Natural History Museum, Cromwell Rd, Kensington, London SW7 5BD"]
      Transit: driving

      Transit can be only one of the following options: "driving", "train", "bus" or "flight".

      {format_instructions}
    """

        self.human_template = """
      ####{agent_suggestion}####
    """

        self.parser = PydanticOutputParser(pydantic_object=Trip)

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(
            self.system_template,
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            self.human_template, input_variables=["agent_suggestion"]
        )

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [self.system_message_prompt, self.human_message_prompt]
        )
