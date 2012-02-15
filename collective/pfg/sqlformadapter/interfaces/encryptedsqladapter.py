from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from collective.pfg.sqlformadapter import sqlformadapterMessageFactory as _



class IEncryptedSQLAdapter(Interface):
    """PFG Adapter to write to an encrypted msSQL table"""

    # -*- schema definition goes here -*-
    table = schema.TextLine(
        title=_(u"Database Table"),
        required=True,
        description=_(u"Table to insert data into"),
    )
#
    name = schema.TextLine(
        title=_(u"Database Name"),
        required=True,
        description=_(u"Name of the MySQL Database you want to use"),
    )
#
    password = schema.TextLine(
        title=_(u"Database Password"),
        required=True,
        description=_(u"Password"),
    )
#
    username = schema.TextLine(
        title=_(u"Database Username"),
        required=True,
        description=_(u"User with write permissions on the database"),
    )
#
    url = schema.TextLine(
        title=_(u"Database URL"),
        required=True,
        description=_(u"The URL of the MySQl Database"),
    )
#
