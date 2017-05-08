powerdash_base_url = "http://cooper-powerdash.herokuapp.com"
powerdash_name_to_dgm = {
    "7th floor mechanical, 8th and 9th lighting and plugs": "x-pml:/diagrams/ud/41cooper/41 7-dh.dgm",
    "4th floor mechanical 2nd,3rd,5th lighting and plugs": "x-pml:/diagrams/ud/41cooper/41 4-dh.dgm",
    "cellar power and lighting": "x-pml:/diagrams/ud/41cooper/41 cdh.dgm",
    "sub-cellar power and lighting": "x-pml:/diagrams/ud/41cooper/41 5-dh.dgm",
    "roof mechanical": "x-pml:/diagrams/ud/41cooper/41 rdhm.dgm",
    "7th floor lighting and plugs": "x-pml:/diagrams/ud/41cooper/417fltl.dgm",
    "6th floor lighting and plugs": "x-pml:/diagrams/ud/41cooper/416fltl.dgm",
    "4th floor lighting and plugs": "x-pml:/diagrams/ud/41cooper/414tl.dgm",
    "3rd floor lighting and plugs": "x-pml:/diagrams/ud/41cooper/413tl.dgm",
    "retail": "x-pml:/diagrams/ud/41cooper/41 rt.dgm",
    "elevator": "x-pml:/diagrams/ud/41cooper/41elevator.dgm",
    "overall utilities": "x-pml:/diagrams/ud/41cooper.dgm"
}
powerdash_name_to_series = {
    "7th floor mechanical, 8th and 9th lighting and plugs": 'SATEC112KW',
    "4th floor mechanical 2nd,3rd,5th lighting and plugs": "SATEC111KW",
    "cellar power and lighting": "SATEC110KW",
    "sub-cellar power and lighting": "SATEC19KW",
    "roof mechanical": "SATEC18KW",
    "7th floor lighting and plugs": "SATEC15KW",
    "6th floor lighting and plugs": "SATEC14KW",
    "4th floor lighting and plugs": "SATEC13KW",
    "3rd floor lighting and plugs": "SATEC12KW",
    "retail": "SATEC17KW",
    "elevator": "SATEC11KW"
}
distribution_board_metadata = {
    "7th floor mechanical, 8th and 9th lighting and plugs": ["7th Floor Lights",
                                                             "7th Floor High Voltage Educational Equipment (Instron, Robotic Arm, etc...)",
                                                             "6th Floor Plugs", "9th Floor Plugs"],
    "4th floor mechanical 2nd,3rd,5th lighting and plugs": ["4th Floor Lights", "5th Floor Plugs", "3rd Floor Plugs"],
    "cellar power and lighting": ["LL1 Lights", "Rose Auditorium Equipment and Lights",
                                  "Ground Level Lights and Plugs"],
    "sub-cellar power and lighting": ["LL2 Lights", "High Voltage Machining Equipment (Welder, Lathe, etc...)", "AHU 1",
                                      "AHU 2", "AHU 3"],
    "roof mechanical": ["Cooling Tower", "Transformers", "Circulating Pump 1", "Circulating Pump 2",
                        "Circulating Pump 3", "Heaters", "Exhaust Fans", "AHU 4", "AHU 5", "AHU 6", "Gas Boosters"],
    "7th floor lighting and plugs": ["7th Floor Plugs"],
    "6th floor lighting and plugs": ["6th Floor Plugs"],
    "4th floor lighting and plugs": ["4th Floor Plugs"],
    "3rd floor lighting and plugs": ["3rd Floor Plugs"],
    "retail": ["Preschool of the Arts"],
    "elevator": ["Express Elevator", "Local Elevator", "Cargo Elevator"],
}

utility_metadata = {
    'Utility 1': ["6th floor lighting and plugs", "7th floor lighting and plugs", "elevator",
                  "sub-cellar power and lighting", "retail", "Cooper Union Servers"],
    'Utility 2': ["3rd floor lighting and plugs", "4th floor mechanical 2nd,3rd,5th lighting and plugs",
                  "4th floor lighting and plugs", "7th floor mechanical, 8th and 9th lighting and plugs",
                  "cellar power and lighting", "roof mechanical", "Cooper Union Server Room AC"]
}

distribution_boards = ["7th floor mechanical, 8th and 9th lighting and plugs",
                       "4th floor mechanical 2nd,3rd,5th lighting and plugs",
                       "cellar power and lighting",
                       "sub-cellar power and lighting",
                       "roof mechanical",
                       "7th floor lighting and plugs",
                       "6th floor lighting and plugs",
                       "4th floor lighting and plugs",
                       "3rd floor lighting and plugs",
                       "retail",
                       "elevator"]
