"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests, random, json

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartIntent":
        return startGame(intent, session)
    elif intent_name == "DistanceGuessIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Distance Guessing game. " \
                    "I am a fun game that will test your geography skills. " \
                    "You can begin playing by saying, start game."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say start game to begin playing the distance guessing game."
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing the distance guessing game! Have a nice day."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def getRandomCity():
    cities = ["New York***New York",
                "Los Angeles***California",
                "Chicago***Illinois",
                "Houston***Texas",
                "Philadelphia***Pennsylvania",
                "Phoenix***Arizona",
                "San Antonio***Texas",
                "San Diego*** California",
                "Dallas***Texas",
                "San Jose***California",
                "Austin***Texas",
                "Jacksonville***Florida",
                "San Francisco***California",
                "Indianapolis***Indiana",
                "Columbus***Ohio",
                "Fort Worth***Texas",
                "Charlotte***North Carolina",
                "Detroit***Michigan",
                "El Paso***Texas",
                "Seattle***Washington",
                "Denver***Colorado",
                "Washington***DC",
                "Memphis***Tennessee",
                "Boston***Massachusetts",
                "Nashville***Tennessee",
                "Baltimore***Maryland",
                "Oklahoma City***Oklahoma",
                "Portland***Oregon",
                "Las Vegas***Nevada",
                "Louisville***Kentucky",
                "Milwaukee***Wisconsin",
                "Albuquerque***New Mexico",
                "Tucson***Arizona",
                "Fresno***California",
                "Sacramento***California",
                "Long Beach***California",
                "Kansas City***Missouri",
                "Mesa***Arizona",
                "Atlanta***Georgia",
                "Virginia Beach***Virginia",
                "Omaha***Nebraska",
                "Colorado Springs***Colorado",
                "Raleigh***North Carolina",
                "Miami***Florida",
                "Oakland***California",
                "Minneapolis***Minnesota",
                "Tulsa***Oklahoma",
                "Cleveland***Ohio",
                "Wichita***Kansas",
                "New Orleans***Louisiana",
                "Arlington***Texas"]

    city = random.choice(cities)
    
    citySplit = city.split('***')

    return citySplit

def getActualDistance(city):
    deviceLocation = requests.get("http://freegeoip.net/json/")
    zipCode = deviceLocation.json()['zip_code']
    zipCode = str(int(zipCode))

    distanceRequest = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+zipCode+"&destinations=" + city[0]+"+"+city[1] + "&units=imperial")
    distance = distanceRequest.json()['rows'][0]['elements'][0]['distance']['text']
    return distance

def startGame(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = "Start Distance Guesser Game"
    session_attributes = {}
    should_end_session = False

    city = getRandomCity()
    distance = getActualDistance(city)
    distance = distance.replace(",","")
    session_attributes = create_distance_attributes(distance,city)
    speech_output = "How many miles away do you think " + city[0] + ", " + city[1] \
                       + " is from your current location?" 
    reprompt_text = "How many miles away do you think " + city[0] + ", " + city[1] \
                       + " is from your current location?"
    

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_distance_attributes(distance,city):
    return {"distance": distance, "city": city[0] + ", "+city[1]}


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "distance" in session.get('attributes', {}):
        distance = session['attributes']['distance']
        city = session['attributes']['city']
        if(distance.endswith(' mi')):
           distance_num = int(distance[:-3])
        guess = int(intent['slots']['Number']['value'])

        difference = abs(distance_num - guess)
        
        if(difference <= 30 and difference != 0):
           speech_output = "You were very close! You were only off by " + str(difference) + " miles. The distance between your current location and " + city + " is " + distance + "les."
           should_end_session = True
        elif(difference <= 0):
           speech_output = "You are absolutely correct! The distance between your current location and " + city + " is exactly" + distance + "les!"
           should_end_session = True
        else:
            speech_output = "Sorry! You are off by " + str(difference) + " miles. The distance between your current location and " + city + " is " + distance + "les."
            should_end_session = True
    else:
        speech_output = "I'm not sure what your guess was! Please try again."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        "Distance Guess Result", speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
