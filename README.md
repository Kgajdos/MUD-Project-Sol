# MUD Project Sol

## Overview
**Project Sol** is a sci-fi based Multi-User Dungeon (MUD) set in the future. This immersive text-based game allows players to explore space, engage in combat, mine asteroids, and more.

Project Sol is currently in development, and we welcome contributions from the community.

## Features
- **Exploration**: Traverse a vast universe filled with unique locations and hidden secrets.
- **Combat**: Engage in tactical space battles and ground combat.
- **Mining**: Discover and mine asteroids for valuable resources.
- **Crafting**: Create and enhance items using materials gathered from across the galaxy.
- **Roles and Tutorials**: Play as a Pilot, Miner, Fighter, Freighter, or Researcher, with tutorials to guide new players.

## Installation
To set up Project Sol locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/kgajdos/project-sol.git
    cd project-sol
    ```

2. **Set up a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Initialize the Evennia game directory**:
    ```sh
    evennia init mygame
    cd mygame
    ```

5. **Run the game server**:
    ```sh
    evennia migrate
    evennia start
    evennia runserver
    ```

## Usage
Once the server is running, you can connect to your MUD using a telnet client or a specialized MUD client. The default address is `localhost` on port `4000`. This will only create a local version of the game on your environment.

### Connecting to Your Local Server
- **Telnet**: Open a terminal and type `telnet localhost 4000`.
- **MUD Client**: Use a MUD client like Mudlet, TinTin++, or others, and connect to `localhost` on port `4000`.

This setup allows you to run and test the game locally on your machine. You can explore, develop, and debug without affecting a live server.

## Development
To contribute to Project Sol, please follow these guidelines:

1. **Fork the repository** and create a new branch for your feature or bugfix.
2. **Write tests** for your changes and ensure all existing tests pass.
3. **Open a pull request**, describing your changes in detail.

### Known Bugs
- **Renaming a Ship**: Fixed.
- **Character Stats**: Significant difficulties with character stats, possibly related to improper usage of enums. Status: In-Progress.
- **CmdPutAway Command**: Outdated and non-functional. Status: To-Do.
- **CombatHandler Script**: Endless loop with the ending message. Status: To-Do.
- **Multiple Prototypes**: Issues with spawning. Status: To-Do.
- **Ship Look Commands**: Multiple look commands when in the same room as a ship. Fixed.
- **Ship Command Locks**: Anyone can board and fly anyone's ship. Status: In-Progress.
- **Command Console Error**: `NoneType` object issue. Status: Temporary Fix.

## Planned Features
- **Corporate Roles**: Implement CEO, COO, CFO roles and building projects.
- **Exploration System**: Procedurally generate points of interest and celestial phenomena.
- **Wearable Items Enhancement**: Enhance wearable items with quality attributes.
- **Item Inventory Management**: Improve item inventory management and interaction.
- **Drinks with Effects**: Create drinks with their given effects.
- **Player Commands for Eating and Drinking**: Allow the player to eat and drink with effects modifying their attributes.

## Contact
For questions or support, please contact us at [your email address].

## License
This project is licensed under the Creative Commons CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.

### Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

#### Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

#### 1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

#### 2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

#### 3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged
