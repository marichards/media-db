A GUIDE TO TABLES

BIOMASS
-biomassID: primary key, identifies a biomass composition
-Genus: identifies genus for a biomass composition
-Species: identifies species for a biomass composition
-sourceID: foreign key, links to SOURCES, indicates the literature source where a biomass composition was found

BIOMASS_COMPOUNDS
-biocompID: primary key, identifies a biomass/compound relationship
-biomassID: foreign key, links to BIOMASS, identifies the biomass composition
-compID: foreign key, links to COMPOUNDS, identifies the compound
-Coefficient: quantifies the stoichiometric coefficient of the specified compound as a contribution to the specified biomass composition

COMPOUND_EXCEPTIONS
COMPOUND_REPLACEMENTS
-These tables contain extra information pertinent to the Price group that is non-essential for database users

COMPOUNDS
-compID: primary key, identifies a compound
-KEGG_ID: identifies the KEGG database identifier, if it exists, for the compound
-BiGG_ID: identifies the BiGG database identifier, if it exists, for the compound
-user_identifier: only for compounds with neither a KEGG nor a BiGG identifier, entries in this column give a human-readable identifier for a compound

CONTRIBUTORS
-contributorID: primary key, identifies a contributor to the database
-Last_Name: identifies a contributor to the database by last name

GROWTH_DATA
-growthID: primary key, identifies a growth condition
-strainID: foreign key, links to ORGANISMS, identifies the organism grown in a specific growth condition
-medID: foreign key, links to MEDIA_NAMES, identifies the media used in a specific growth condition
-sourceID: foreign key, links to SOURCES, identifies the literature source where a specific growth condition was found
-Growth_Rate: for growth conditions with measured growth rates, quantifies the growth rate for a specific growth condition
-Growth_Units: for growth conditions with measured growth rates, specifies the units for the measured growth rate of a specific growth condition
-pH: quantifies the pH of a growth condition, when specified in the literature source
-Temperature_C: quantifies the temperature of a growth condition, when specified in the literature source
-measureID: foreign key, links to MEASUREMENTS, identifies the technique used to determine the growth rate
-Additional_Notes: contains any additional information about the specified growth condition not otherwise specified 

MEASUREMENTS
-measureID: primary key, identifies a measurement technique
-Measurement_Technique: specifies a measurement technique used for finding growth rate, either the method used in the literature source or "slope estimation" to specify that growth rates were manually estimated by reading off growth curves in the literature

MEDIA_COMPOUNDS
-medcompID: primary key, identifies a media/compound relationship
-medID: foreign key, links to MEDIA_NAMES, identifies the media composition
-compID: foreign key, links to COMPOUNDS, identifies the compound
-Amount_mM: quantifies the amount of a compound present in a medium composition in units of millimolar (mM)

MEDIA_NAMES
-medID: primary key, identifies a medium composition
-Media_name: provides a human-readable identifier for a specific medium composition
-Is_defined: either Y or N, indicates if a medium composition is chemically defined
-Is_minimal: either Y or N, indicates if a medium composition is specified as "Minimal" in the literature source

NAMES_OF_COMPOUNDS
-nameID: primary key, identifies a compound name
-compID: foreign key, links to COMPOUNDS, identifies the compound
-Name: provides a common, human-readable name for a compound

ORGANISMS
-strainID: primary key, identifies a specific organism strain
-Genus: specifies the organism genus
-Species: specifies the organism species
-Strain: specifies the organism strain, if applicable
-contributorID: foreign key, links to CONTRIBUTORS, identifies which contributor entered information for this organism into the database
-typeID: foreign key, links to TYPES_OF_ORGANISMS, identifies which kingdom the organism belongs to

ORGANISMS_SOURCES
-strainsourceID: primary key, identifies a unique organism/source relationship
-strainID: foreign key, links to ORGANISMS, identifies the organism
-sourceID: foreign key, links to SOURCES, identifies the literature source where information on an organism was taken from

PRODUCTS
-prodID: primary key, identifies a dissociation product
-rxntID: foreign key, links to REACTANTS, identifies the dissociation reactant, a compound that does not have an identifier in KEGG or BiGG
-coeff: specifies the stoichiometric coefficient for a product when dissociating from the specified reactant
-compID: foreign key, links to COMPOUNDS, specifies the compound identifier for the product

REACTANTS
-rxntID: primary key, identifies a "reactant" that has no KEGG or BiGG ID
-compID: foreign key, links to COMPOUNDS, identifies the compound
-Similar_Compounds: foreign key, links to COMPOUNDS, if applicable gives a compID that identifies compounds with KEGG IDs that are similar to the "reactant"

SECRETION_UPTAKE
-secretionuptakeID: primary key, identifies a secretion or uptake rate
-growthID: foreign key, links to GROWTH_RATES, identifies the growth condition that the secretion/uptake rate is associated with
-compID: foreign key, links to COMPOUNDS, identifies the compound being secreted/uptaken
-Rate: quantifies the rate of secretion/uptake
-Units: specifies the units of the secretion/uptake rate
-rateID: foreign key, links to SECRETION_UPTAKE_KEY, specifies whether the given rate is an uptake, a secretion, or a yield coefficient

SECRETION_UPTAKE_KEY
-rateID: primary key, identifies a secretion/uptake rate type
-Rate_Type: specifies the rate type (uptake/secretion/yield coefficient)

SEED_COMPOUNDS
-seedkeggID: primary key, specifies a KEGG-Seed compound relationship
-KEGG_ID: foreign key, links to COMPOUNDS, identifies the KEGG_ID for a compound
-Seed_ID: specifies the Seed_ID for a compound that corresponds to the given KEGG_ID

SOURCES
-sourceID: primary key, specifies a literature source
-First_Author: specifies the last name of the first author listed for the literature source
-Journal: for scientific articles, specifies the full name of the journal where the article was found
-Year: specifies the year when the source was published
-Title: gives the title of the literature source
-Link: for sources found online, specifies a url that links to the source

TYPES_OF_ORGANISMS
-typeID: primary key, identifies an organism type (kingdom)
-Organism_type: specifies the name of the organism type (archaea/bacteria/eukaryote)