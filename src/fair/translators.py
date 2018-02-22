from pyld import jsonld
#import rdflib


# B2SHARE: webapp
# Level 1: FAIR Data Point metadata layer (data repository)
def translate_fdp(webapp):
    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema/",
        "dcat" : "http://www.w3.org/ns/dcat#",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o/",
        "r3d" : "http://www.re3data.org/schema/3-0/",
        "foaf" : "http://xmlns.com/foaf/",
        # B2SHARE otology (internal terms)
        "b2" : "https://b2share.eudat.eu/ontology/b2share/" }
    doc = {
        "@type": "r3d:Repository",
        "@id": webapp.identifier,
        "http://purl.org/dc/terms/identifier": webapp.identifier,
        "http://purl.org/dc/terms/description": webapp.description,
        "http://purl.org/dc/terms/title": webapp.name,
        "http://purl.org/dc/terms/hasVersion": webapp.version,
        "http://purl.org/dc/terms/publisher": webapp.publisher,

        #"http://purl.org/dc/terms/issued": webapp.created,
        #"http://purl.org/dc/terms/modified": webapp.updated,

        "https://b2share.eudat.eu/ontology/b2share/site_function" : webapp.site_function,
        "https://b2share.eudat.eu/ontology/b2share/training_site_link" : webapp.training_site_link,
        "https://b2share.eudat.eu/ontology/b2share/b2access_registration_link" : webapp.b2access_registration_link,
        "https://b2share.eudat.eu/ontology/b2share/b2note_url" : webapp.b2note_url,
        "https://b2share.eudat.eu/ontology/b2share/terms_of_use_link" : webapp.terms_of_use_link,

        "http://www.re3data.org/schema/3-0/repositoryIdentifier" : webapp.fdp_repository_id,
        "http://www.re3data.org/schema/3-0/institution" : webapp.institution,
        "http://www.re3data.org/schema/3-0/institutionCountry" : webapp.institution_country,
        "http://www.re3data.org/schema/3-0/lastUpdate" : webapp.updated,
        "http://www.re3data.org/schema/3-0/startDate" : webapp.created,
        "http://www.w3.org/2000/01/rdf-schema/label" : webapp.name,

        "http://rdf.biosemantics.org/ontologies/fdp-o/metadataIdentifier" : webapp.fdp_metadata_id,
        "http://rdf.biosemantics.org/ontologies/fdp-o/metadataModified" : webapp.updated,
        "http://rdf.biosemantics.org/ontologies/fdp-o/metadataIssued" : webapp.created

    }
    '''
    TO DISCUSS: a "lazy load" method to load the catalogs (communities)?
        e.g. r3d:dataCatalog <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/biobank> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/comparativeGenomics> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/patient-registry> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/textmining> , <http://dev-vm.fair-dtls.surf-hosted.nl:8082/fdp/transcriptomics> ;
    '''

    return jsonld.compact(doc, context)


def translate_fdp_rdfxml(webapp):
    jsonldmsg = translate_fdp(webapp)
    normalized = jsonld.normalize(jsonldmsg)
    #TODO: check error on transforming from N3 to RDF/XML (or Turtle?)
    # http://www.nolan-nichols.com/knowledge-graph-via-sparql.html
    #g = rdflib.Graph()
    #g.parse(data=normalized, format='n3')
    #result = g.serialize(format='turtle')

    result = normalized
    #print(result)

    return result

# B2SHARE: Community
# Level 2: Catalog metadata layer
def translate_catalog(community):

    # TODO: change from community.roles[1].name to community.roles["admin"].name and check if it is really a controlled vocabulary in B2SHAER (Thijs)

    AdminRole = {
        "@id": community.roles[1].name,
        "@type": "pro:PublishingRole",
        "http://purl.org/dc/terms/description" : community.roles[1].description,
        "http://purl.org/dc/terms/identifier": community.roles[1].identifier,
        "http://purl.org/dc/terms/title": community.roles[1].name
    }

    MemberRole = {
        "@id": community.roles[0].name,
        "@type": "pro:PublishingRole",
        "http://purl.org/dc/terms/description" : community.roles[0].description,
        "http://purl.org/dc/terms/identifier": community.roles[0].identifier,
        "http://purl.org/dc/terms/title": community.roles[0].name
    }

    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "dcat" : "http://www.w3.org/ns/dcat#",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o#",
        "foaf" : "http://xmlns.com/foaf/",
        # B2SHARE otology (internal terms)
        "b2" : "https://b2share.eudat.eu/ontology/b2share/",
        # Other ontologies (reused)
        "pro" : "http://purl.org/spar/pro/" # Publishing Roles
    }

    doc = {
        "@id": community.links.selflink,
        "@type": "dcat:Catalog",
        "http://purl.org/dc/terms/identifier": community.identifier,
        "http://purl.org/dc/terms/title": community.name,
        "http://purl.org/dc/terms/description": community.description,
        "http://purl.org/dc/terms/issued": community.created,
        "http://purl.org/dc/terms/modified": community.updated,
        "http://xmlns.com/foaf/logo" : community.logo,
        "https://b2share.eudat.eu/ontology/b2share/publication_workflow" : community.publication_workflow,
        "https://b2share.eudat.eu/ontology/b2share/restricted_submission" : community.restricted_submission,
        "https://b2share.eudat.eu/ontology/b2share/AdminRole" : AdminRole,
        "https://b2share.eudat.eu/ontology/b2share/MemberRole" : MemberRole
    }
    compacted = jsonld.compact(doc, context)
    return compacted


# Test mappings Level 2: Catalog x Community, according to translate_catalog method
def assert_fields_community_catalog(community, catalog):
    assert community.identifier == catalog["dct:identifier"]
    assert community.name == catalog["dct:title"]
    assert community.description == catalog["dct:description"]
    assert community.created == catalog["dct:issued"]
    assert community.updated == catalog["dct:modified"]
    assert community.logo == catalog["foaf:logo"]
    assert community.publication_workflow == catalog["b2:publication_workflow"]
    assert community.restricted_submission == catalog["b2:restricted_submission"]


# B2SHARE: Record
# Level 3: Dataset metadata layer
def translate_dataset(record):

    dc_descriptions = []
    for description in record.metadata.descriptions:
        #print(description.description)
        dc_description = {
            "http://purl.org/dc/terms/description": description.description
        }
        dc_descriptions.append(dc_description)
        #merged_dict = {key: value for (key, value) in (dc_descriptions.items() + dc_description.items())}

    #jsonDescription = json.dumps(dc_descriptions)
    #print(dc_descriptions)

    #Should these mappings consider other metadata fields, such as "disciplines" and resource types?
    dcat_themes = []
    if record.metadata.keywords is not None:
        for keyword in record.metadata.keywords:
            dcat_theme = {
                "http://www.w3.org/ns/dcat/theme": keyword
            }
            dcat_themes.append(dcat_theme)

    dcat_distributions = []
    for recordfile in record.files:
        dcat_distribution = {
            "http://www.w3.org/ns/dcat/distribution": recordfile.version_id #TODO: the most correct here is to use the file @id (which is based on the version_id) -> this would require to access the /files/ resource to retrieve the desired @id (to discuss)
        }
        dcat_distributions.append(dcat_distribution)

    dc_license = "no license metadata used"
    if record.metadata.license is not None:
        dc_license = record.metadata.license.license

    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "dcat" : "http://www.w3.org/ns/dcat/",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o#",
        "foaf" : "http://xmlns.com/foaf/",
        "b2" : "https://b2share.eudat.eu/ontology/b2share/"
    }

    doc = {
        "@id": record.links.selflink,
        "@type": "dcat:Dataset",
        "http://purl.org/dc/terms/identifier": "dataRecord", #record.identifier,
        "http://purl.org/dc/terms/title": record.name,
        "http://purl.org/dc/terms/issued": record.created,
        "http://purl.org/dc/terms/modified": record.updated,

        "https://b2share.eudat.eu/ontology/b2share/hasCommunity": record.metadata.community,
        "http://purl.org/dc/terms/language": record.metadata.language,
        "http://purl.org/dc/terms/hasVersion": record.metadata.version,
        "http://purl.org/dc/terms/publisher": record.metadata.publisher,

        "http://purl.org/dc/terms/license": dc_license, #"testing...", # license,

        #TODO: check if it is the best way to serialize an array in JSON-LD (through a property defined in the internal ontology)
        "https://b2share.eudat.eu/ontology/b2share/hasDescriptions": dc_descriptions,
        "https://b2share.eudat.eu/ontology/b2share/hasThemes": dcat_themes,
        "https://b2share.eudat.eu/ontology/b2share/hasDistributions": dcat_distributions,
        "https://b2share.eudat.eu/ontology/b2share/hasDistributionsLink": record.links.files  # Check if the correct approach is to format the link to opint to /distributions/_id

    }

    #if len(record.metadata.descriptions) > 0:
    #    print(record.metadata.descriptions[0])
    #print(record.metadata.descriptions)

    result = jsonld.compact(doc, context)
    #normalized = jsonld.normalize(result)
    #print(normalized)

    return result


# B2SHARE: File (contents)
# Level 4: Distribution layer
def translate_distribution(b2file):
    # The idea is to map each file version in b2file.contents to a fdp.Distribution
    # Therefore, this translator will always return an array of fdp.distributoin with at least 1 element
    # Fields of b2file are mapped to each distribution, e.g. distrib1.b2:quota_size, distrib2.b2:quota_size, distrib3.b2:quota_size
    # Each fdp.distribution b2:hasPriorVersion to the prior. The first in the array does not instantiate this property

    dcat_distributions = []
    for filecontent in b2file.contents:
        dcat_distribution = translate_distribution_item(b2file, filecontent)
        dcat_distributions.append(dcat_distribution)

    return dcat_distributions

# translates a file version to a distribution: check if this is the best approach. Cons: it is necessary to represent the distribution and the distribution version (how FDP approaches it?)
def translate_distribution_item(b2file, filecontent):

    context = {
        # ontologies used in FDP according to spec
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "dcat" : "http://www.w3.org/ns/dcat#",
        "xsd" : "http://www.w3.org/2001/XMLSchema#",
        "owl" : "http://www.w3.org/2002/07/owl#",
        "dct" : "http://purl.org/dc/terms/",
        "lang" : "http://id.loc.gov/vocabulary/iso639-1/",
        "fdp" : "http://rdf.biosemantics.org/ontologies/fdp-o#",
        "foaf" : "http://xmlns.com/foaf/",
        "b2" : "https://b2share.eudat.eu/ontology/b2share/"
    }

    doc = {
        "@id": filecontent.links.selflink,
        "@type": "dcat:Distribution",
        #"http://purl.org/dc/terms/identifier": b2file.identifier,
        "http://purl.org/dc/terms/issued": filecontent.created,
        "http://purl.org/dc/terms/modified": filecontent.updated,
        "http://purl.org/dc/terms/title": filecontent.key,
        #"http://purl.org/dc/terms/license": filecontent.key,  --> license is set up in the dataset level (level 3)
        "http://purl.org/dc/terms/hasVersion": filecontent.version_id,

        "http://purl.org/dc/terms/versionOf": b2file.links.selflink
    }

    return jsonld.compact(doc, context)
