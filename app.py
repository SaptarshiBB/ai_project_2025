from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import logging

app = Flask(__name__)
CORS(app)  


logging.basicConfig(level=logging.DEBUG)


genai.configure(api_key="")  #put the api key here personal key not for share


model = genai.GenerativeModel('gemini-1.5-pro-latest')  # i am using gemini 1.5 pro model which is avaliable you can use what you like 


ALLOWED_TOPICS = {
   
    "clean","cleanup", "clean-up", "community cleanup", "neighborhood cleanup", "beach cleanup", 
    "river cleanup", "park cleanup", "street cleaning", "highway cleanup", "lake cleanup",
    "forest cleanup", "underwater cleanup", "mountain cleanup", "desert cleanup", 
    "urban cleanup", "rural cleanup", "school cleanup", "playground cleanup",
    "shoreline cleanup", "wetland cleanup", "trail cleanup", "vacant lot cleanup",
    "litter picking", "plogging", "trash collection", "debris removal", "waste pickup",
    "illegal dumping cleanup", "hazardous waste removal", "post-storm cleanup",
    "post-event cleanup", "neighborhood beautification", "graffiti removal",
    "public space maintenance", "adopt-a-road", "adopt-a-park", "adopt-a-spot",
    "community stewardship", "litter patrol", "trash tag", "clean sweep",
    "spruce up", "tidy up", "spring cleaning", "deep clean", "sanitation drive",
    "environmental sanitation", "neighborhood revitalization", "blight removal",
    "brownfield restoration", "ecosystem restoration", "habitat cleanup",

    "trash", "litter", "garbage", "refuse", "rubbish", "debris", "waste", "junk",
    "plastic waste", "food waste", "organic waste", "yard waste", "construction waste",
    "electronic waste", "hazardous waste", "household waste", "industrial waste",
    "marine debris", "microplastics", "nurdles", "cigarette butts", "chewing gum",
    "fast food packaging", "single-use plastics", "plastic bags", "plastic bottles",
    "plastic straws", "plastic utensils", "styrofoam", "fishing gear", "ghost nets",
    "abandoned boats", "tires", "scrap metal", "glass bottles", "aluminum cans",
    "paper waste", "cardboard", "textile waste", "diapers", "medical waste",
    "hazardous household waste", "paint disposal", "battery recycling",
    "oil disposal", "chemical waste", "asbestos removal","roadside waste","roadside dump",

   
    "recycling", "upcycling", "downcycling", "composting", "vermicomposting",
    "waste management", "waste reduction", "waste audit", "zero waste",
    "circular economy", "source reduction", "reuse", "repair", "refill",
    "donation", "thrift", "swap", "sharing economy", "material recovery",
    "single-stream recycling", "dual-stream recycling", "e-waste recycling",
    "textile recycling", "battery recycling", "oil recycling", "metal recycling",
    "glass recycling", "paper recycling", "plastic recycling", "organic recycling",
    "compostable", "biodegradable", "landfill diversion", "waste-to-energy",
    "incineration", "anaerobic digestion", "pyrolysis", "gasification",
    "extended producer responsibility", "product stewardship", "take-back programs",
    "deposit return schemes", "pay-as-you-throw", "bulky waste", "hazardous waste",
    "waste characterization", "waste composition", "diversion rate", "MRF",
    "transfer station", "sanitary landfill", "leachate", "methane capture",

   
    "pollution", "littering", "illegal dumping", "fly-tipping", "marine pollution",
    "plastic pollution", "water pollution", "air pollution", "soil contamination",
    "noise pollution", "light pollution", "thermal pollution", "nutrient pollution",
    "sediment pollution", "chemical pollution", "oil spills", "sewage overflow",
    "stormwater runoff", "urban runoff", "agricultural runoff", "acid rain",
    "eutrophication", "algal blooms", "dead zones", "bioaccumulation",
    "microplastics in food chain", "great pacific garbage patch", "gyres",
    "climate change", "global warming", "carbon emissions", "methane emissions",
    "deforestation", "desertification", "soil erosion", "habitat destruction",
    "biodiversity loss", "invasive species", "species extinction", "ecosystem collapse",
    "environmental degradation", "resource depletion", "overshoot day",

    "sustainability", "sustainable development", "green living", "eco-friendly",
    "environmentally friendly", "carbon footprint", "ecological footprint",
    "water footprint", "energy conservation", "water conservation", "resource efficiency",
    "green building", "LEED certification", "passive house", "net zero",
    "renewable energy", "solar", "wind", "geothermal", "hydropower", "biomass",
    "energy efficiency", "green technology", "clean technology", "green chemistry",
    "sustainable agriculture", "organic farming", "permaculture", "regenerative agriculture",
    "urban farming", "community gardens", "food security", "local food", "farm to table",
    "slow food", "meatless Monday", "plant-based", "vegan", "vegetarian",
    "sustainable fashion", "ethical consumerism", "minimalism", "simple living",
    "voluntary simplicity", "degrowth", "steady state economy",

    
    "community engagement", "civic participation", "volunteerism", "service learning",
    "corporate volunteering", "employee engagement", "team building", "youth programs",
    "school programs", "scouts", "girl scouts", "boy scouts", "4-H", "rotary",
    "lions club", "kiwanis", "environmental education", "public awareness",
    "behavior change", "nudge theory", "community-based social marketing",
    "environmental policy", "litter laws", "plastic bans", "bag bans", "straw bans",
    "extended producer responsibility", "product stewardship", "right to repair",
    "green procurement", "sustainable purchasing", "environmental justice",
    "climate justice", "just transition", "green jobs", "environmental health",
    "public health", "environmental racism", "food justice", "water justice",
    "urban planning", "smart growth", "new urbanism", "complete streets",
    "transit-oriented development", "walkability", "bikeability", "green infrastructure",
    "low impact development", "sponge cities",

   
    "litter pickers", "grabbers", "gloves", "safety vests", "reflective gear",
    "trash bags", "recycling bins", "compost bins", "wheelbarrows", "rakes",
    "brooms", "shovels", "hoes", "trowels", "pruners", "hedge trimmers",
    "wheelie bins", "dumpsters", "roll-off containers", "trash cans",
    "recycling carts", "compost tumblers", "water bottles", "reusable bags",
    "reusable utensils", "reusable straws", "water stations", "hydration stations",
    "first aid kits", "sunscreen", "bug spray", "safety glasses", "hard hats",
    "work boots", "high-visibility clothing", "weather radios", "trash skimmers",
    "waterway cleanup tools", "beach rakes", "sand sifters","dustbins","hand gloves",

    "Earth Day", "World Cleanup Day", "Coastal Cleanup Day", "Great American Cleanup",
    "Clean Up the World", "Plastic Free July", "World Environment Day",
    "Arbor Day", "World Oceans Day", "World Water Day", "America Recycles Day",
    "Buy Nothing Day", "Car Free Day", "Meatless Monday", "Bike to Work Day",
    "Park(ing) Day", "Jane's Walk", "Love Your Block", "Keep America Beautiful",
    "Surfrider Foundation", "Ocean Conservancy", "Sierra Club", "Nature Conservancy",
    "World Wildlife Fund", "Greenpeace", "350.org", "Extinction Rebellion",
    "Fridays for Future", "Youth Climate Strike", "Sunrise Movement",
    "Citizens' Climate Lobby", "Transition Towns", "Slow Food Movement",
    "Zero Waste Home", "Plastic Pollution Coalition","swach bharat","yamuna cleaning drive","yamuna cleanup","ganga clean","Swachh Bharat Abhiyan",
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        app.logger.debug("Received chat request")
        
        data = request.get_json()
        if not data or 'message' not in data:
            app.logger.error("Missing message in request")
            return jsonify({'error': 'Missing message'}), 400

        user_input = data['message'].strip().lower()
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Topic check
        if not any(topic in user_input for topic in ALLOWED_TOPICS):
            return jsonify({
                'response': "I'm here to discuss community clean-up and sustainability. "
                           "Try asking about recycling, volunteering, or reducing waste!"
            })

        
        response = model.generate_content(
            user_input,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9
            )
        )
        
        if not response.text:
            raise ValueError('Empty response from AI model')

        return jsonify({'response': response.text})

    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
