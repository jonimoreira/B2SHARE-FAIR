from mapper import Model, Field, NestedField


class NestedModel(Model):
    name = Field(name='name')
    description = Field(name='description')


class LinksModel(Model):
    selflink = Field(name='self')

    def __repr__(self):
        return '{"self": "%s"}' % self.selflink


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

    resource_name = 'communities'


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

    resource_name = 'records'


class FileModel(Model):
    """
    B2Share file model schema abstraction.
    """

    identifier = Field(name='id')
    name = Field(name='name')
    description = Field(name='description')
    created = Field(name='created')
    updated = Field(name='updated')

    links = NestedField(name='links', cls=LinksModel)

    resource_name = 'files'


class WebAppModel(Model):
    """
    B2Share webapp model schema abstraction.
    """
    CONST_B2SHARE_REPOSITORY_ID = "EUDAT_B2SHARE_WEBAPP"
    CONST_B2SHARE_REPOSITORY_NAME = "EUDAT B2SHARE data repository"
    CONST_B2SHARE_REPOSITORY_DESCRIPTION = "The EUDAT B2SHARE data repository as a web application"
    CONST_B2SHARE_REPOSITORY_CREATED = "01/01/2018"
    CONST_B2SHARE_REPOSITORY_UPDATED = "01/01/2018"

    identifier = CONST_B2SHARE_REPOSITORY_ID  # Field(name='id')
    name = CONST_B2SHARE_REPOSITORY_NAME  # Field(name='name')
    description = CONST_B2SHARE_REPOSITORY_DESCRIPTION  # Field(name='description')
    created = CONST_B2SHARE_REPOSITORY_CREATED  # Field(name='created')
    updated = CONST_B2SHARE_REPOSITORY_UPDATED  # Field(name='updated')
    publisher = ''

    site_function = Field(name='site_function')
    training_site_link = Field(name='training_site_link')
    version = Field(name='version')
    b2access_registration_link = Field(name='b2access_registration_link')
    b2note_url = Field(name='b2note_url')
    terms_of_use_link = Field(name='terms_of_use_link')

    resource_name = ''
