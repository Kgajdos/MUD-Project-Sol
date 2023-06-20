from evennia.utils import dedent
from typeclasses.characters import Character
import inflect
_INFLECT = inflect.engine()

#########################################################
#                   WELCOME PAGE                        #
#########################################################
def menunode_welcome(caller):
    """Starting Page"""
    text = dedent(
        """\
        You awaken in a small room, a warm glow dances around you.
        Before you is a mirror.
        """
    )
    help = "You will have the ability to make changes before the character is finalized."
    options = {"desc": "look mirror", "goto": "menunode_info_base"}
    return (text, help), options



#########################################################
#                INFORMATIONAL PAGES                    #
#########################################################

#A dictionary for storing character info
_CLASS_INFO_DICT = {
    "Fighter": dedent(
    """\
    Regardless of humanity's feelings on the matter, conflict is constant.
    Fighters can achieve fame and wealth, if they don't make the ultimate 
    sacrifice.
    
    Follow a strong moral code and become a hero, or else...
    """
    ),
    "Freighter": dedent(
    """\
    Near everyone relies on goods being shipped in, making it the most 
    lucrative business. Either work for corporations or become a modern
    merchant sailor!   

    Space is incomprehensively big... and lonely... 
    """
    ),
    "Miner": dedent(
    """\
    Mining is the heart of all industry. As such, Miners enjoy constant
    employment at competitive prices. The work is repetative though and 
    may not be for everyone.    

    Would you rather stare at rocks all day or the fabricator?
    """
    ),
    "Researcher": dedent(
    """\
    Science never sleeps but thankfully you can with the assistance of on
    board AI. While you can sell your findings, riches are not often found
    here.    

    But hey, the rats are cute!
    """
    )
}

def menunode_info_base(caller):
    """Base node for the informational choices"""
    #the node base for the job descision
    caller.new_char.db.chargen_step = "menunode_info_base"

    text = dedent(
        """\
        Hello, I'm Mirvelle, I'm here to assist you in getting started on Kupier Station.
        Why don't you check out the type of work that's needed around here.
        Perhaps there's something that interests you?
    
        """
    )
    help = "Ship types are locked to their respective jobs."
    options = []
    #Options built from info dict above
    for pclass in _CLASS_INFO_DICT.keys():
        options.append(
            {
                "desc": f"Learn about the |c{pclass}|n job",
                "goto": ("menunode_info_class", {"selected_class": pclass})
            }
        )
    return (text, help), options

def menunode_info_class(caller, raw_string, selected_class=None, **kwargs):
    """Informational job/class overview"""
    #checks if there's a selected class, goes back if not
    if not selected_class:
        caller.new_char.db.chargen_step = "menunode_welcome"
        return "Something went wrong. Please try again."
    
    text = _CLASS_INFO_DICT[selected_class]
    options = []

    options.append(
        {"desc": f"Become {_INFLECT.an(selected_class)}",
         "goto": (_set_class, {"selected_class": selected_class})}
    )
    options.append(
        {"desc": "Return to class list",
         "goto": "menunode_info_base"}
    )
    #builds options based on info dict
    for pclass in _CLASS_INFO_DICT.keys():
        if pclass != selected_class:
            options.append(
                {"desc": f"Learn about the |c{pclass}|n job",
                 "goto": ("menunode_info_class", {"selected_class": pclass})}
            )
        return text, options
    
def _set_class(caller, raw_string, selected_class = None, **kwargs):
    #A job should always be selected here **CLASS = JOB**
    if not selected_class:
        #go back to choose
        return "menunode_info_base"
    
    char = caller.new_char
    #possible new code here
    char.db.player_class = selected_class

    #move on to categories
    return "menunode_categories"

#########################################################
#                 OPTION CATEGORIES                     #
#########################################################

#a dict of player appearance in 3 categories (key)
_APPEARANCE_DICT = {
    "sex": [
        "male",
        "female",
        "other",
        "none",
    ],
    "body_type": [
        "lanky",
        "sturdy",
        "bulky",
        "slender",
        "thin",
        "frail",
        "agile",
        "clumsy",
        "fastideous",
        "large",
        "fat",
        "husky",
        "average"
    ],
    "adjective": [
        "reflective",
        "rude",
        "competitive",
        "neighborly",
        "peaceful",
        "loud",
        "classy",
        "youthful",
        "burly",
        "ambitious",
        "humorous",
        "creative",
        "confident",
        "adventurous",
        "honest",
        "enthusiastic",
        "trustworthy",
        "kind"
    ],
    "height": ["diminutive", "short", "average", "tall", "towering"],
    "disposition": [
        "calm",
        "nice",
        "smart",
        "strong",
        "demanding",
        "dominating",
        "alluring",
        "snarky",
        "angry",
        "mean",
        "friendly",
        "affectionate",
        "cheery",
        "uncomfortable",
        "irritable",
        "sociable",
        "quiet",
        "pious"
    ]
}

def menunode_categories(caller, **kwargs):
    """Base node for categorized options."""
    #new decision point, need to save a resume point here
    caller.new_char.db.chargen_step = "menunode_categories"

    text = dedent(
        """\
        Why don't you tell me a little about yourself?

        """
    )
    help = "Here is where you will describe yourself. Remember that other players will get to know you based on this description."
    options = []
    ##appends dict key
    for category in _APPEARANCE_DICT.keys():
        options.append(
            {"desc": f"Choose your |c{category}|n",
             "goto": ("menunode_category_options", {"category": category})}
        )
    #appends next step
    options.append(
        {"key": ("(Next)", "next", "n"),
         "desc": "Continue to next step.",
         "goto": "menunode_multi_choice"}
    )
    #appends previous step
    options.append(
        {"key": ("(Back)", "back", "b"),
         "desc": "Go back to previous step.",
         "goto": "menunode_info_base"}
    )
    return (text, help), options

def menunode_category_options(caller, raw_string, category=None, **kwargs):
    """Choosing an option within the cat"""
    if not category:
        return "Something went wrong. Please try again."
    
    #can use help to inform player of mechanic-related choices
    text = f"Choose your {category}:"
    help = f"This will define your {category}."

    options = []
    # build the list of options from the right category of your dictionary
    for option in _APPEARANCE_DICT[category]:
        options.append(
            {"desc": option, "goto": (_set_category_opt,
                                      {"category": category, "value": option})}
        )
    options.append(
        {
            "key": ("(Back)", "back", "b"),
            "desc": f"Don't change {category}",
            "goto": "menunode_categories"
        }
        )
    return (text, help), options

def _set_category_opt(caller, raw_string, category, value, **kwargs):
    """Set the option for a category"""
    caller.new_char.attributes.add(category, value)

    return "menunode_categories"

#########################################################
#                 MULTIPLE CHOICE                       #
#########################################################

_SKILL_OPTIONS = [
    "cooking",
    "diplomacy",
    "fabricating",
    "guns",
    "logic",
    "luck",
    "mechanic",
    "melee",
    "piloting",
    "tinkering",
    "trade"
]

def menunode_multi_choice(caller, raw_string, **kwargs):
    char = caller.new_char

    #Resume point because of new decision
    char.db.chargen_step = "menunode_multi_choice"
# in order to support picking up from where we left off, get the options from the character
# if they weren't passed in
# this is again just a simple attribute, but you could retrieve this list however
    selected = kwargs.get("selected") or char.attributes.get("skill_list", [])

    text = dedent(
        """\
        Tell me three things you're good at.
        """
    )
    help = ("Please choose exactly 3 skills.")
    options = []
    for option in _SKILL_OPTIONS:
        #check if option is selected
        if option in selected:
            #if it has, we want to highlight it
            opt_desc = f"|y{option} (selected)|n"
        else:
            opt_desc = option
        options.append(
            {"desc": opt_desc, "goto": (_set_multichoice, {"selected": selected, "option": option, "level": 1, "xp": 0})}
        )

    #will only display the next option if 3 choices are made
    if len(selected) == 3:
        options.append(
            {
                "key": ("(Next)", "next", "n"),
                "desc": "Continue to next step",
                "goto": "menunode_choose_name"
            }
        )
    options.append(
        {
                "key": ("(Back)", "back", "b"),
                "desc": "Go back to the previous step",
                "goto": "menunode_categories"
        }
    )
    return (text, help), options
    
def _set_multichoice(caller, raw_string, selected=[], **kwargs):
    """Saves the current choices to the character"""
    #get the option being chosen
    if option := kwargs.get("option"):
        #already in list, remove
        if option in selected:
            selected.remove(option)
        #otherwise we add it
        else:
            selected.append(option)

        caller.new_char.attributes.add('skills', {skill: dict(level=1, exp=0) for skill in selected})

    return ("menunode_multi_choice", {"selected": selected})

#########################################################
#                      THE END                          #
#########################################################

def menunode_end(caller, raw_string):
    """End-of-chargen cleanup."""
    char = caller.new_char
    #create_objects(char)
    caller.new_char.attributes.remove("chargen_step")
    text = dedent(
        """
        Welcome to Project Sol!

        Enjoy your stay!
        """
    )
    return text, None

def menunode_choose_name(caller, raw_string, **kwargs):
    """Name selection"""
    char = caller.new_char

    char.db.chargen_step = "menunode_choose_name"

    #check to make sure an error message wasn't passed to the node
    if error := kwargs.get("error"):
        prompt_text = f"{error}. Enter a different name."
    else:
        prompt_text = "Enter a name here to check if it's available."

    text = dedent(
        f"""\
        And finally, what's your name?

        {prompt_text}
        """
    )
    help = "You will have the chance to change your mind before confirming, even if the name you've entered is available."
    #text-free field
    options = {"key": "_default", "goto": _check_charname}
    return (text, help), options

def _check_charname(caller, raw_string, **kwargs):
    """Check and confirm name choice"""

    charname = raw_string.strip()

    charname = caller.account.normalize_username(charname)

    candidates = Character.objects.filter_family(db_key__iexact=charname)
    if len(candidates):
       return (
           "menunode_chosen_name",
            {"error": f"|w{charname}|n is unavailable.\n\nEnter a different name."})
    else:
        caller.new_char.key = charname
        return "menunode_confirm_name"
    
def menunode_confirm_name(caller, raw_string, **kwargs):
    """Confirm name choice"""
    char = caller.new_char

    text = f"|w{char.key}|n is available! Confirm?"
    options = [
        {"key": ("yes", "y"), "goto": "menunode_end"},
        {"key": ("No", "n"), "goto": "menunode_choose_name"}
    ]
    return text, options
