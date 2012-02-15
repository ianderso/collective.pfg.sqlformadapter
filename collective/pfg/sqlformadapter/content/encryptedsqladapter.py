"""Definition of the Encrypted SQL Adapter content type
"""

from zope.interface import implements

from Products.Archetypes import atapi

from Products.PloneFormGen.content.actionAdapter import \
    FormActionAdapter, FormAdapterSchema

from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from collective.pfg.sqlformadapter import sqlformadapterMessageFactory as _

from collective.pfg.sqlformadapter.interfaces import IEncryptedSQLAdapter
from collective.pfg.sqlformadapter.config import PROJECTNAME

import pymssql
import logging
dblog = logging.getLogger('collective.pfg.sqlformadapter.dblog')

EncryptedSQLAdapterSchema = FormAdapterSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'table',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Database Table"),
            description=_(u"Table to insert data into"),
        ),
        required=True,
    ),


    atapi.StringField(
        'name',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Database Name"),
            description=_(u"Name of the MySQL Database you want to use"),
        ),
        required=True,
    ),


    atapi.StringField(
        'password',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Database Password"),
            description=_(u"Password"),
        ),
        required=False,
    ),


    atapi.StringField(
        'username',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Database Username"),
            description=_(u"User with write permissions on the database"),
        ),
        required=True,
    ),


    atapi.StringField(
        'url',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Database URL"),
            description=_(u"The URL of the MySQl Database"),
        ),
        required=True,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

EncryptedSQLAdapterSchema['title'].storage = atapi.AnnotationStorage()
EncryptedSQLAdapterSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(EncryptedSQLAdapterSchema, moveDiscussion=False)


class EncryptedSQLAdapter(FormActionAdapter):
    """PFG Adapter to write to an encrypted MySQL table"""
    implements(IEncryptedSQLAdapter)

    meta_type = "EncryptedSQLAdapter"
    schema = EncryptedSQLAdapterSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    table = atapi.ATFieldProperty('table')

    name = atapi.ATFieldProperty('name')

    password = atapi.ATFieldProperty('password')

    username = atapi.ATFieldProperty('username')

    url = atapi.ATFieldProperty('url')

    key = atapi.ATFieldProperty('key')

    def onSuccess(self, fields, REQUEST=None):
        """
        saves data.
        """
        try:
            dbconn = pymssql.connect (host = self.url,
                user = self.username,
                passwd = self.password,
                db = self.name)
            dbconn.autocommit(False)
        except pymssql.Error, e:
            dblog.error("MySQL error %d: %s"  % (e.args[0], e.args[1]))
            return

        disallowed_types = ('FormLabelField', 'FormFolder', 'FieldsetFolder',
                            'FormCaptchaField', 'FormRichLabelField',
                            'FormMailerAdapter', 'FomrSaveDataAdapter',
                            'FormThanksPage', 'FormCustomScriptAdapter')

        data = {}
        for f in fields:
            if f.portal_type not in disallowed_types:
                data[f] = REQUEST.form.get(f.fgField.getName(),'')

        value_strings = list()
        for v in data.values():
            value_strings.append(dbconn.escape_string(str(v)))

        try:
            cursor = dbconn.cursor()
            dblog.info("INSERT INTO %s (%s) VALUES (%s);" % (self.table, ", ".join([k.id for k in data.keys()]), ", ".join([v for v in value_strings])))
            cursor.execute("INSERT INTO %s (%s) VALUES (%s);" % (self.table, ", ".join([k.id for k in data.keys()]), ", ".join([v for v in value_strings])))
            dbconn.commit()
            cursor.close()
        except pymssql.Error, e:
            dbconn.rollback()
            dblog.error("Transaction aborted %d: %s" % (e.args[0], e.args[1]))
            cursor.close()

        dbconn.close()


atapi.registerType(EncryptedSQLAdapter, PROJECTNAME)
