# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################



## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

#
# Themes being Hammered into web2py starts here (look away).
#

import os
import gluon.template

class ThemeableTemplateParser(gluon.template.TemplateParser):
    def __init__(self, text,
                 name="ParserContainer",
                 context=dict(),
                 path='views/',
                 writer='response.write',
                 lexers={},
                 delimiters=('{{', '}}'),
                 _super_nodes = [],
                 theme_path= 'themes/default'
                 ):
        self.theme_path = theme_path
        super(ThemeableTemplateParser, self).__init__(text, name, context, path, writer, lexers, delimiters, _super_nodes)
        

    def _get_file_text(self, filename):
        if self.theme_path:
            theme_filename = os.path.join(self.theme_path, filename[1:-1])
            if os.path.exists(theme_filename):
                try:
                    fileobj = open(theme_filename, 'rb')
                    text = fileobj.read()
                    fileobj.close()
                except IOError:
                    self._raise_error('Unable to open included view file: ' + theme_filename)
                return text

        return super(ThemeableTemplateParser, self)._get_file_text(filename)


def parse_template(filename,
                   path='views/',
                   context=dict(),
                   lexers={},
                   delimiters=('{{', '}}')
                   ):
    """
    Args:
        filename: can be a view filename in the views folder or an input stream
        path: is the path of a views folder
        context: is a dictionary of symbols used to render the template
        lexers: dict of custom lexers to use
        delimiters: opening and closing tags
    """
    from gluon import current

    # First, if we have a str try to open the file
    if isinstance(filename, str):
        try:
            fp = open(os.path.join(path, filename), 'rb')
            text = fp.read()
            fp.close()
        except IOError:
            raise RestrictedError(filename, '', 'Unable to find the file')
    else:
        text = filename.read()

    if current.response.theme_path:
        return str(ThemeableTemplateParser(text, context=context, path=path, lexers=lexers, delimiters=delimiters, theme_path=current.response.theme_path))
    return str(gluon.template.TemplateParser(text, context=context, path=path, lexers=lexers, delimiters=delimiters))


import gluon.compileapp
if request.vars.theme:
    session.theme = request.vars.theme
theme = session.theme or 'default'
response.theme_path = os.path.join(request.folder, 'static', 'themes', theme)
gluon.compileapp.__dict__['parse_template'] = parse_template
execfile(os.path.join(request.folder, 'static', 'themes', theme, 'run.py'))

