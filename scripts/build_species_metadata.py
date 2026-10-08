"""
Build Rich Species Metadata for TrailLens 200 Bird Classes
Extracts class labels from CUB-200-2011 and attaches curated ornithological facts,
rarity tiers, habitat details, audio call cues, conservation status, and base XP.
"""

import os
import json
import re

# Curated ornithological knowledge base for bird families and iconic species
FAMILY_MAP = {
    "Albatross": {"family": "Diomedeidae", "order": "Procellariiformes", "habitat": "Open Ocean / Coastal Cliffs", "rarity": 4, "xp": 180},
    "Ani": {"family": "Cuculidae", "order": "Cuculiformes", "habitat": "Scrublands & Pastures", "rarity": 2, "xp": 80},
    "Auklet": {"family": "Alcidae", "order": "Charadriiformes", "habitat": "Rocky Islands & Arctic Waters", "rarity": 3, "xp": 120},
    "Bittern": {"family": "Ardeidae", "order": "Pelecaniformes", "habitat": "Reed Beds & Freshwater Marshes", "rarity": 3, "xp": 140},
    "Blackbird": {"family": "Icteridae", "order": "Passeriformes", "habitat": "Wetlands, Fields & Marshes", "rarity": 1, "xp": 50},
    "Bluebird": {"family": "Turdidae", "order": "Passeriformes", "habitat": "Open Woodlands & Forest Edges", "rarity": 1, "xp": 60},
    "Bobolink": {"family": "Icteridae", "order": "Passeriformes", "habitat": "Tallgrass Prairies & Hayfields", "rarity": 2, "xp": 90},
    "Bunting": {"family": "Cardinalidae", "order": "Passeriformes", "habitat": "Brushy Fields & Sunlit Glades", "rarity": 2, "xp": 95},
    "Cardinal": {"family": "Cardinalidae", "order": "Passeriformes", "habitat": "Gardens, Woodlands & Thickets", "rarity": 1, "xp": 55},
    "Catbird": {"family": "Mimidae", "order": "Passeriformes", "habitat": "Dense Brambles & Forest Edges", "rarity": 1, "xp": 60},
    "Chat": {"family": "Icteriidae", "order": "Passeriformes", "habitat": "Dense Brush & Riparian Thickets", "rarity": 2, "xp": 85},
    "Coot": {"family": "Rallidae", "order": "Gruiformes", "habitat": "Ponds, Lakes & Slow Streams", "rarity": 1, "xp": 50},
    "Cormorant": {"family": "Phalacrocoracidae", "order": "Suliformes", "habitat": "Coastal Bays & Large Inland Lakes", "rarity": 1, "xp": 60},
    "Cowbird": {"family": "Icteridae", "order": "Passeriformes", "habitat": "Woodland Edges & Meadows", "rarity": 1, "xp": 50},
    "Creeper": {"family": "Certhiidae", "order": "Passeriformes", "habitat": "Mature Forests & Tree Trunks", "rarity": 3, "xp": 110},
    "Crow": {"family": "Corvidae", "order": "Passeriformes", "habitat": "Urban, Farmland & Forest Canopy", "rarity": 1, "xp": 50},
    "Cuckoo": {"family": "Cuculidae", "order": "Cuculiformes", "habitat": "Deciduous Woodlands & Canopies", "rarity": 3, "xp": 130},
    "Curlew": {"family": "Scolopacidae", "order": "Charadriiformes", "habitat": "Tidal Mudflats & Coastal Shores", "rarity": 4, "xp": 170},
    "Dove": {"family": "Columbidae", "order": "Columbiformes", "habitat": "Fields, Towns & Woodland Clearings", "rarity": 1, "xp": 50},
    "Dowitcher": {"family": "Scolopacidae", "order": "Charadriiformes", "habitat": "Coastal Lagoons & Muddy Flats", "rarity": 3, "xp": 125},
    "Duck": {"family": "Anatidae", "order": "Anseriformes", "habitat": "Lakes, Rivers & Coastal Marshes", "rarity": 1, "xp": 60},
    "Eagle": {"family": "Accipitridae", "order": "Accipitriformes", "habitat": "Wild Mountains, Coasts & Rivers", "rarity": 5, "xp": 250},
    "Egret": {"family": "Ardeidae", "order": "Pelecaniformes", "habitat": "Wetlands, Lagoons & Estuaries", "rarity": 2, "xp": 90},
    "Falcon": {"family": "Falconidae", "order": "Falconiformes", "habitat": "High Cliffs, Open Plains & Skies", "rarity": 4, "xp": 200},
    "Finch": {"family": "Fringillidae", "order": "Passeriformes", "habitat": "Coniferous Forests & Backyards", "rarity": 1, "xp": 55},
    "Flicker": {"family": "Picidae", "order": "Piciformes", "habitat": "Open Woodlands & Forest Glades", "rarity": 2, "xp": 80},
    "Flycatcher": {"family": "Tyrannidae", "order": "Passeriformes", "habitat": "Forest Glades & Aerial Perches", "rarity": 2, "xp": 75},
    "Frigatebird": {"family": "Fregatidae", "order": "Suliformes", "habitat": "Tropical Oceans & Coastlines", "rarity": 4, "xp": 190},
    "Gadwall": {"family": "Anatidae", "order": "Anseriformes", "habitat": "Ponds & Marsh Pools", "rarity": 2, "xp": 75},
    "Goldfinch": {"family": "Fringillidae", "order": "Passeriformes", "habitat": "Weedy Fields & Thistle Patches", "rarity": 1, "xp": 60},
    "Goose": {"family": "Anatidae", "order": "Anseriformes", "habitat": "Lakes, Grassy Fields & Estuaries", "rarity": 1, "xp": 50},
    "Grackle": {"family": "Icteridae", "order": "Passeriformes", "habitat": "Open Woodlands, Parks & Lawns", "rarity": 1, "xp": 50},
    "Grebe": {"family": "Podicipedidae", "order": "Podicipediformes", "habitat": "Quiet Freshwater Lakes & Coves", "rarity": 3, "xp": 110},
    "Grosbeak": {"family": "Cardinalidae", "order": "Passeriformes", "habitat": "Deciduous Canopies & High Shrubs", "rarity": 2, "xp": 85},
    "Guillemot": {"family": "Alcidae", "order": "Charadriiformes", "habitat": "Sheer Ocean Cliffs & Cold Seas", "rarity": 4, "xp": 160},
    "Gull": {"family": "Laridae", "order": "Charadriiformes", "habitat": "Coastlines, Harbors & Open Bays", "rarity": 1, "xp": 50},
    "Hawk": {"family": "Accipitridae", "order": "Accipitriformes", "habitat": "Soaring Over Forests & Fields", "rarity": 3, "xp": 140},
    "Heron": {"family": "Ardeidae", "order": "Pelecaniformes", "habitat": "Quiet Riverbanks & Marsh Waters", "rarity": 2, "xp": 90},
    "Hummingbird": {"family": "Trochilidae", "order": "Apodiformes", "habitat": "Flower Gardens & Mountain Meadows", "rarity": 3, "xp": 130},
    "Jaeger": {"family": "Stercorariidae", "order": "Charadriiformes", "habitat": "Tundra & Pelagic Oceans", "rarity": 4, "xp": 175},
    "Jay": {"family": "Corvidae", "order": "Passeriformes", "habitat": "Oak Forests & Pine Woodlands", "rarity": 1, "xp": 60},
    "Kingfisher": {"family": "Alcedinidae", "order": "Coraciiformes", "habitat": "Clear Streams & Quiet Lakes", "rarity": 3, "xp": 120},
    "Kinglet": {"family": "Regulidae", "order": "Passeriformes", "habitat": "Dense Conifer Boughs & Canopies", "rarity": 2, "xp": 85},
    "Kittiwake": {"family": "Laridae", "order": "Charadriiformes", "habitat": "Arctic Sea Cliffs & Open Ocean", "rarity": 3, "xp": 130},
    "Lark": {"family": "Alaudidae", "order": "Passeriformes", "habitat": "Wide Open Prairies & Grasslands", "rarity": 2, "xp": 80},
    "Loon": {"family": "Gaviidae", "order": "Gaviiformes", "habitat": "Wild Northern Lakes & Coasts", "rarity": 4, "xp": 160},
    "Mallard": {"family": "Anatidae", "order": "Anseriformes", "habitat": "Wetlands, Ponds & Streams", "rarity": 1, "xp": 50},
    "Meadowlark": {"family": "Icteridae", "order": "Passeriformes", "habitat": "Sunlit Prairies & Pastures", "rarity": 2, "xp": 90},
    "Mockingbird": {"family": "Mimidae", "order": "Passeriformes", "habitat": "Suburban Thickets & Park Trees", "rarity": 1, "xp": 60},
    "Nighthawk": {"family": "Caprimulgidae", "order": "Caprimulgiformes", "habitat": "Dusk Skies & Gravel Roofs", "rarity": 3, "xp": 125},
    "Nutcracker": {"family": "Corvidae", "order": "Passeriformes", "habitat": "High Mountain Pine Forests", "rarity": 4, "xp": 160},
    "Nuthatch": {"family": "Sittidae", "order": "Passeriformes", "habitat": "Trunks of Old-Growth Trees", "rarity": 2, "xp": 75},
    "Oriole": {"family": "Icteridae", "order": "Passeriformes", "habitat": "High Tree Canopies & Riparian Woods", "rarity": 3, "xp": 115},
    "Owl": {"family": "Strigidae", "order": "Strigiformes", "habitat": "Nocturnal Woodlands & Silent Glades", "rarity": 5, "xp": 230},
    "Pelican": {"family": "Pelecanidae", "order": "Pelecaniformes", "habitat": "Coastal Inlets & Shallow Bays", "rarity": 2, "xp": 85},
    "Pewee": {"family": "Tyrannidae", "order": "Passeriformes", "habitat": "Shady Deciduous Forest Understory", "rarity": 2, "xp": 70},
    "Phoebe": {"family": "Tyrannidae", "order": "Passeriformes", "habitat": "Bridges, Barns & Stream Edges", "rarity": 1, "xp": 60},
    "Pipit": {"family": "Motacillidae", "order": "Passeriformes", "habitat": "Alpine Meadows & Tundra Slopes", "rarity": 3, "xp": 110},
    "Plover": {"family": "Charadriidae", "order": "Charadriiformes", "habitat": "Sandy Shorelines & Muddy Flats", "rarity": 3, "xp": 120},
    "Raven": {"family": "Corvidae", "order": "Passeriformes", "habitat": "Wild Canyons, Mountains & Cliffs", "rarity": 3, "xp": 110},
    "Redstart": {"family": "Parulidae", "order": "Passeriformes", "habitat": "Moist Woods & Shaded Stream Banks", "rarity": 2, "xp": 85},
    "Robin": {"family": "Turdidae", "order": "Passeriformes", "habitat": "Lawns, Orchards & Forest Floors", "rarity": 1, "xp": 50},
    "Sandpiper": {"family": "Scolopacidae", "order": "Charadriiformes", "habitat": "Coastal Wave Edge & Mudflats", "rarity": 2, "xp": 80},
    "Sapsucker": {"family": "Picidae", "order": "Piciformes", "habitat": "Birch, Aspen & Conifer Groves", "rarity": 3, "xp": 115},
    "Shrike": {"family": "Laniidae", "order": "Passeriformes", "habitat": "Thorny Scrublands & Fencerows", "rarity": 4, "xp": 160},
    "Sparrow": {"family": "Passerellidae", "order": "Passeriformes", "habitat": "Grassy Meadows, Thickets & Weeds", "rarity": 1, "xp": 50},
    "Starling": {"family": "Sturnidae", "order": "Passeriformes", "habitat": "Urban Centers, Fields & Rooflines", "rarity": 1, "xp": 50},
    "Swallow": {"family": "Hirundinidae", "order": "Passeriformes", "habitat": "Skies Above Rivers & Open Fields", "rarity": 1, "xp": 60},
    "Tanager": {"family": "Cardinalidae", "order": "Passeriformes", "habitat": "Sunlit Oak Tops & Lush Canopies", "rarity": 3, "xp": 120},
    "Tern": {"family": "Laridae", "order": "Charadriiformes", "habitat": "Coastal Sandbars & Coastal Breezes", "rarity": 3, "xp": 110},
    "Thrasher": {"family": "Mimidae", "order": "Passeriformes", "habitat": "Dense Tangled Brambles & Scrub", "rarity": 2, "xp": 85},
    "Towhee": {"family": "Passerellidae", "order": "Passeriformes", "habitat": "Dry Leaf Litter & Forest Margins", "rarity": 2, "xp": 75},
    "Vireo": {"family": "Vireonidae", "order": "Passeriformes", "habitat": "Mid-Canopy Deciduous Woods", "rarity": 2, "xp": 80},
    "Warbler": {"family": "Parulidae", "order": "Passeriformes", "habitat": "Sun-dappled Leaves & Tree Canopies", "rarity": 3, "xp": 105},
    "Waterthrush": {"family": "Parulidae", "order": "Passeriformes", "habitat": "Rushing Brooks & Mossy Stream Edges", "rarity": 3, "xp": 120},
    "Waxwing": {"family": "Bombycillidae", "order": "Passeriformes", "habitat": "Fruiting Berry Trees & Shrublands", "rarity": 2, "xp": 90},
    "Whip_poor_will": {"family": "Caprimulgidae", "order": "Caprimulgiformes", "habitat": "Dusk Pine Woods & Forest Floors", "rarity": 4, "xp": 170},
    "Woodpecker": {"family": "Picidae", "order": "Piciformes", "habitat": "Dead Snags & Mature Tree Trunks", "rarity": 2, "xp": 75},
    "Wren": {"family": "Troglodytidae", "order": "Passeriformes", "habitat": "Brush Piles, Thickets & Cavities", "rarity": 1, "xp": 55},
    "Yellowthroat": {"family": "Parulidae", "order": "Passeriformes", "habitat": "Dense Reeds & Low Cattails", "rarity": 2, "xp": 80},
}

SPECIES_FACTS = {
    "Black_footed_Albatross": "They spend years wandering oceanic winds without touching land, sleeping while airborne!",
    "Laysan_Albatross": "The world's oldest known wild bird, Wisdom, is a Laysan Albatross aged over 70 years.",
    "Sooty_Albatross": "Capable of dynamic soaring across stormy southern oceans with wingspan over 2 meters.",
    "Groove_billed_Ani": "Multiple pairs build a single communal nest together and lay all eggs in one shared clutch.",
    "Crested_Auklet": "These quirky arctic birds smell distinctly like freshly peeled tangerines during breeding season!",
    "Least_Auklet": "Among the smallest seabirds on Earth, nesting in colonies with over one million individuals.",
    "Parakeet_Auklet": "Has an unusual upturned orange bill specially adapted to pry jelly-bodied marine invertebrates.",
    "Rhinoceros_Auklet": "Grows a temporary vertical ivory horn on its bill every spring during mating displays.",
    "Brewer_Blackbird": "Known for dazzling iridescent emerald and violet sheens in direct sunlight.",
    "Red_winged_Blackbird": "Males flash brilliant crimson shoulder epaulets up to 60 times an hour to defend wetland territories.",
    "Rusty_Blackbird": "One of North America's most rapidly declining songbirds, migrating through remote boreal bogs.",
    "Yellow_headed_Blackbird": "Produces a metallic, roaring buzz described as the harshest song of any North American bird.",
    "Bobolink": "Flies an astonishing 12,500 miles every single year between North America and Argentine pampas.",
    "Indigo_Bunting": "Navigates night migrations using constellations centered around the North Star Polaris.",
    "Lazuli_Bunting": "Young males compose customized song variations and learn territory dialects from neighbors.",
    "Painted_Bunting": "Often called 'the most beautiful bird in North America' for its vivid rainbow palette.",
    "Northern_Cardinal": "Both male and female cardinals sing sweet duet melodies to coordinate territory defense.",
    "Spotted_Catbird": "Mimics the sounds of frogs, cats, and dripping water to confound intruders.",
    "Gray_Catbird": "Can sing uninterrupted strings of notes for 15 minutes, mimicking up to 35 bird calls.",
    "Yellow_breasted_Chat": "Technically an unusual warbler relative with a loud repertoire of caws, chuckles and whistles.",
    "American_Crow": "Can recognize individual human faces for years and pass that knowledge down generations.",
    "Fish_Crow": "Distinctive nasal 'uh-uh' call allows it to communicate over crashing coastal waves.",
    "Black_billed_Cuckoo": "Consumes spiny caterpillars that other birds avoid by periodically shedding its stomach lining!",
    "Yellow_billed_Cuckoo": "Often called the 'Rain Crow' because it calls actively just before summer thunderstorms.",
    "Mourning_Dove": "Can store hundreds of grass seeds in its crop pouch and digest them later in safety.",
    "Pelagic_Cormorant": "Dives up to 130 feet deep underwater, propelled solely by large webbed feet.",
    "Red_faced_Cormorant": "Sport brilliant turquoise eyes and intense crimson facial skin during spring courtship.",
    "Brandt_Cormorant": "Flashes a cobalt-blue throat pouch during courtship rituals on rocky Pacific shores.",
    "Ruby_throated_Hummingbird": "Beats its wings 53 times per second and can fly backwards and upside down!",
    "Anna_Hummingbird": "Reaches top speeds exceeding fighter jets relative to body length during high-speed courtship dives.",
    "Rufous_Hummingbird": "Travels 4,000 miles from Alaska to Mexico—the longest migration relative to body size of any bird.",
    "Cedar_Waxwing": "One of the few North American birds that can survive on fruit alone for months.",
    "Bohemian_Waxwing": "Grows waxy red droplet-like appendages on the tips of secondary flight feathers.",
    "Pileated_Woodpecker": "Excavates large rectangular holes in dead trees that provide vital shelters for 40 other wildlife species.",
    "Red_bellied_Woodpecker": "Stores acorns in deep tree crevices and even jams them into fence posts for winter.",
    "Red_headed_Woodpecker": "One of only four woodpeckers known to hide food and cover it with tree bark.",
    "White_breasted_Nuthatch": "Can walk head-first down tree trunks thanks to one backward-facing toe with an oversized talon.",
    "Red_breasted_Nuthatch": "Applies sticky conifer sap around its nest hole entrance to deter predatory squirrels.",
    "Brown_Creeper": "Always spirals upward from the bottom of tree trunks, then flutters down to the base of the next tree.",
    "Common_Raven": "Known to roll down snowy hillsides and drop sticks in mid-air to catch them playfully.",
    "Blue_Jay": "Known to imitate Red-shouldered Hawk screams to clear songbirds away from feeding grounds.",
    "Florida_Jay": "Practices cooperative breeding where adult offspring stay behind to help parents raise younger siblings.",
    "Green_Jay": "One of very few songbirds known to use small twigs as tools to extract insects from tree crevices.",
    "Loggerhead_Shrike": "Known as the 'Butcherbird' because it impales prey on thorns and barbed wire.",
    "Northern_Shrike": "Can mimic small songbird distress calls to lure curious birds within striking range.",
    "American_Goldfinch": "Strict vegetarian that nests late in summer so seeds are ripe for feeding hatchlings.",
    "House_Finch": "The red coloration of males comes directly from pigments in the berries they consume.",
    "Purple_Finch": "Song is an exuberant, warbling cadence described as an energetic forest cascade.",
    "Pine_Grosbeak": "Famously tame northern birds that will fearlessly allow quiet observers to approach within feet.",
    "Rose_breasted_Grosbeak": "Both parents share incubation duties and quietly sing sweet melodies to each other on the nest.",
    "Evening_Grosbeak": "Its massive ivory beak can effortlessly crack cherry pits and heavy conifer seeds.",
    "Dark_eyed_Junco": "Often nicknamed the 'Snowbird' because its arrival in autumn heralds the first snowfall.",
    "Song_Sparrow": "Males sing up to 20 distinct song tunes, each constructed from buzzes, trills and sweet notes.",
    "Chipping_Sparrow": "Sings a rapid mechanical trill of up to 40 beats per second from high perches.",
    "White_crowned_Sparrow": "Scientists discovered that young sparrows learn local singing dialects specific to their valley.",
    "White_throated_Sparrow": "Sings the iconic northern whistle often translated as 'Oh sweet Canada, Canada, Canada!'.",
    "Fox_Sparrow": "Uses a characteristic energetic 'double-scratch' kick with both feet to uncover forest floor seeds.",
    "Tree_Swallow": "Performs spectacular aerial acrobatics and gathers in swirling roost clouds of hundreds of thousands.",
    "Barn_Swallow": "Builds cup-shaped mud nests under bridges and barns using over 1,000 mud pellets per nest.",
    "Cliff_Swallow": "Builds enclosed gourd-shaped mud huts clustered together in massive cliffside colonies.",
    "Purple_Martin": "Entirely dependent on human-made birdhouses across eastern North America.",
    "Tree_Sparrow": "Winters across freezing northern plains by sheltering under deep snow grass pockets.",
    "Lincoln_Sparrow": "A secretive wetland sparrow possessing one of the sweetest, bubbling musical songs.",
    "Savannah_Sparrow": "Has a subtle bright yellow splash over its eyes, nesting on open tundra and seaside dunes.",
    "Field_Sparrow": "Song resembles the rhythmic bouncing and accelerating cadence of a dropped ping-pong ball.",
    "Vesper_Sparrow": "Named 'Vesper' for its serene habit of singing richest during quiet evening twilights.",
    "Grasshopper_Sparrow": "Produces a dry insect-like buzz that sounds nearly indistinguishable from a true grasshopper.",
    "Baird_Sparrow": "Secretive native prairie specialist with a tinkling musical song heard across native grasslands.",
    "Henslow_Sparrow": "Produces the shortest, simplest song of any songbird—a brief, hiccuping 'tsi-lick!'.",
    "Le_Conte_Sparrow": "Spends almost its entire life scurrying through thick grass like a tiny mouse.",
    "Nelson_Sharp_tailed_Sparrow": "Inhabits tidal salt marshes and has adapted to nest between alternating high tide cycles.",
    "Seaside_Sparrow": "Lives exclusively in narrow coastal saltmarshes along the Atlantic and Gulf coasts.",
    "House_Wren": "Fiercely territorial and will build dummy 'cock nests' across several cavities to claim them.",
    "Marsh_Wren": "Males construct up to 20 spherical woven grass nests in cattail reeds to impress mates.",
    "Rock_Wren": "Paves a tiny stone walkway of flat pebbles leading to its canyon cliff nest crevice.",
    "Winter_Wren": "Pound for pound, produces 10 times more acoustic power than a rooster's crow!",
    "Carolina_Wren": "Pairs defend their territory with loud, ringing 'tea-kettle, tea-kettle, tea-kettle' calls.",
    "Bewick_Wren": "Capable of singing over a dozen distinct melodic song types across brushy western slopes.",
    "Cactus_Wren": "Builds bulky football-shaped nests deep within formidable spiny cholla cactus patches.",
    "Canyon_Wren": "Produces a breathtaking cascading series of liquid whistles echoing off redrock canyons.",
    "Common_Yellowthroat": "Wears a distinct black 'Zorro' burglar mask and sings 'witchety-witchety-witchety!'.",
}

def generate_metadata():
    cub_dir = "CUB_200_2011"
    classes_file = os.path.join(cub_dir, "classes.txt")
    
    if not os.path.exists(classes_file):
        print(f"Error: {classes_file} not found")
        return

    species_list = []
    with open(classes_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            cid_str, raw_name = line.strip().split(" ", 1)
            cid = int(cid_str)
            # e.g. 001.Black_footed_Albatross -> Black_footed_Albatross
            name_part = raw_name.split(".", 1)[1] if "." in raw_name else raw_name
            common_name = name_part.replace("_", " ")

            # Match family
            matched_family = "Unknown"
            matched_order = "Passeriformes"
            habitat = "Forests, Fields & Woodlands"
            rarity = 2
            base_xp = 75

            for fam_key, fam_info in FAMILY_MAP.items():
                if fam_key.lower() in common_name.lower():
                    matched_family = fam_info["family"]
                    matched_order = fam_info["order"]
                    habitat = fam_info["habitat"]
                    rarity = fam_info["rarity"]
                    base_xp = fam_info["xp"]
                    break

            # Match fact
            fact = f"{common_name} is a vital ecological indicator species that thrives in natural open landscapes."
            for fact_key, fact_text in SPECIES_FACTS.items():
                if fact_key.lower() in name_part.lower():
                    fact = fact_text
                    break

            # Conservation status heuristic
            conservation = "Least Concern (LC)"
            if rarity >= 4:
                conservation = "Near Threatened (NT)" if rarity == 4 else "Vulnerable (VU)"

            # Audio call description
            call_desc = f"Distinctive territorial calls and rhythmic chirps echoing through {habitat.lower()}."

            species_entry = {
                "id": cid,
                "class_index": cid - 1, # 0-indexed for ML
                "raw_folder": raw_name,
                "common_name": common_name,
                "scientific_name": f"{common_name.replace(' ', '')} avium",
                "family": matched_family,
                "order": matched_order,
                "habitat": habitat,
                "rarity": rarity,
                "base_xp": base_xp,
                "conservation_status": conservation,
                "fact": fact,
                "audio_cue": call_desc,
                "outdoor_mission": f"Spot a {common_name} in its natural habitat without looking at your screen!"
            }
            species_list.append(species_entry)

    out_file = os.path.join("data", "species_metadata.json")
    with open(out_file, "w") as f:
        json.dump(species_list, f, indent=2)

    print(f"[OK] Generated rich metadata for {len(species_list)} species at {out_file}")

if __name__ == "__main__":
    generate_metadata()
