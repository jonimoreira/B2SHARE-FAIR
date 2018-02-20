from mapper import Model, Field, NestedField


class LinksModel(Model):
    selflink = Field(name='self')

    def __repr__(self):
        return '{"self": "%s"}' % self.selflink


class Role(Model):
    name = Field(name='name')
    description = Field(name='description')
    identifier = Field(name='id')


class WebAppModel(Model):
    """
    B2Share webapp model schema abstraction.
    """
    CONST_B2SHARE_REPOSITORY_ID = "https://trng-b2share.eudat.eu/"
    CONST_B2SHARE_FDP_REPOSITORY_ID = "https://trng-b2share.eudat.eu/fdp-repositoryID"
    CONST_B2SHARE_REPOSITORY_NAME = "EUDAT B2SHARE data repository"
    CONST_B2SHARE_REPOSITORY_DESCRIPTION = "The EUDAT B2SHARE data repository as a web application"
    CONST_B2SHARE_REPOSITORY_CREATED = "01/01/2016"
    CONST_B2SHARE_REPOSITORY_UPDATED = "23/02/2018"
    CONST_B2SHARE_REPOSITORY_INSTITUTION = "SURFsara"
    CONST_B2SHARE_REPOSITORY_INSTITUTION_COUNTRY = "The Netherlands"

    CONST_FDP_METADATA_ID = "https://trng-b2share.eudat.eu/fdp-metadataID"


    identifier = CONST_B2SHARE_REPOSITORY_ID  # Field(name='id')
    name = CONST_B2SHARE_REPOSITORY_NAME  # Field(name='name')
    description = CONST_B2SHARE_REPOSITORY_DESCRIPTION  # Field(name='description')
    created = CONST_B2SHARE_REPOSITORY_CREATED  # Field(name='created')
    updated = CONST_B2SHARE_REPOSITORY_UPDATED  # Field(name='updated')
    publisher = CONST_B2SHARE_REPOSITORY_INSTITUTION
    fdp_repository_id = CONST_B2SHARE_FDP_REPOSITORY_ID
    institution = CONST_B2SHARE_REPOSITORY_INSTITUTION
    institution_country = CONST_B2SHARE_REPOSITORY_INSTITUTION_COUNTRY

    fdp_metadata_id = CONST_FDP_METADATA_ID

    site_function = Field(name='site_function')
    training_site_link = Field(name='training_site_link')
    version = Field(name='version')
    b2access_registration_link = Field(name='b2access_registration_link')
    b2note_url = Field(name='b2note_url')
    terms_of_use_link = Field(name='terms_of_use_link')

    resource_name = ''


class CommunityModel(Model):
    """
    B2Share community model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')
    logo = Field(name='logo')
    publication_workflow = Field(name='publication_workflow')
    restricted_submission = Field(name='restricted_submission')
    links = NestedField(name='links', cls=LinksModel)
    roles = NestedField(name='roles', cls=Role, multiple=True)

    resource_name = 'communities'


class RecordMetadataModel(Model):
    community = Field(name='community')
    contact_email = Field(name='contact_email')
    language = Field(name='language')
    version = Field(name='version')
    publisher = Field(name='publisher')

    descriptions = Field(name='descriptions')
    keywords = Field(name='keywords')


class RecordModel(Model):
    """
    B2Share record model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')

    links = NestedField(name='links', cls=LinksModel)

    metadata = NestedField(name='metadata', cls=RecordMetadataModel)

    resource_name = 'records'


class ContentsModel(Model):
    version_id = Field(name='version_id')

    def __repr__(self):
        return '{"self": "%s"}' % self.selflink


class FileModel(Model):
    """
    B2Share file model schema abstraction.
    """

    identifier = Field(name='id')
    locked = Field(name='locked')
    size = Field(name='size')
    max_file_size = Field(name='max_file_size')
    quota_size = Field(name='quota_size')

    created = Field(name='created')
    updated = Field(name='updated')

    #links = NestedField(name='links', cls=LinksModel)

    #contents = NestedField(name='contents', cls=ContentsModel)

    resource_name = 'files'
