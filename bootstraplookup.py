import json
import cherrypy
import tinycss
from tinycss.css21 import RuleSet
import urllib.request

global parsed_bootstrap
global parsed_bootstrap_dict
      
class BootstrapLookup(object):
    exposed = True
    
    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, var=None, **params):
        cherrypy.log("{}.GET invoked with {}".format(type(self).__name__, str(params)))
        
        global parsed_bootstrap
        splitter = cherrypy.request.config['bootstrap_splitter']
        term_name = cherrypy.request.config['bootstrap_term_name']
        term = params.get(term_name);
        
        rule_names = []
        for rule in parsed_bootstrap.rules:
            if type(rule) is RuleSet:
                css_names = rule.selector.as_css()
                css_names_list = css_names.split(splitter)
                css_names_list = [name for name in css_names_list if term in name]
                rule_names.extend(css_names_list)
        rep = '","'.join(rule_names)
        rep = '["'+rep+'"]'
        return rep

class BootstrapDefLookup(object):
    exposed = True
    
    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, var=None, **params):
        cherrypy.log("{}.GET invoked with {}".format(type(self).__name__, str(params)))
        global parsed_bootstrap_dict
        term = params.get(term_name);
        definition = parsed_bootstrap_dict.get(term)
        return definition
        
    def extractDef(self):
        for rule in parsed_bootstrap.rules:
            if type(rule) is RuleSet:
                css_names = rule.selector.as_css()
                css_names_list = css_names.split(splitter)
                definition = ""
                for declaration in rule.declarations:
                    definition += declaration.name
                    definition += ":"
                    definition += ",".join(declaration.value)
                    definition += "\\n"
                for css_name in css_names_list:
                    parsed_bootstrap_dict[css_name] = definition
                    
class StaticPage(object):
    exposed = True
    @cherrypy.expose
    def index(self):
        pass

def parse_bootstrap(bootstrap_url):
    parser = tinycss.make_parser('page3')
    global parsed_bootstrap
    with urllib.request.urlopen(bootstrap_url) as url: 
        parsed_bootstrap = parser.parse_stylesheet_bytes(url.read())
        cherrypy.log("parsed bootstrap {} from {}".format(bootstrap_url, str(parsed_bootstrap)))
        
class TestLink(object):
    exposed = True
    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, var=None, **params):
        return "data:1,2\\nzelta:3,4"

if __name__ == '__main__':

    cherrypy.tree.mount(
        BootstrapLookup(), '/bootstraplookup',
        "bootstraplookup.config"
    )
    
    app = cherrypy.tree.mount(
        BootstrapDefLookup(), '/bootstrapdeflookup',
        "bootstraplookup.config"
    )
    
#     app = cherrypy.tree.mount(
#         StaticPage(), '/',
#         "bootstraplookup.config"
#     )
#     
#     app = cherrypy.tree.mount(
#         TestLink(), '/testlink',
#         "bootstraplookup.config"
#     )
    
    # TODO write a tutorial on lambda
    cherrypy.engine.subscribe('start', lambda: parse_bootstrap(app.config['/']['bootstrap_url']))
    
    cherrypy.engine.start()
    cherrypy.engine.block()