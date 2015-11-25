import cherrypy
import tinycss
from tinycss.css21 import RuleSet
import urllib.request

global parsed_bootstrap
      
class BootstrapLookup(object):
    exposed = True
    
    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, var=None, **params):
        global parsed_bootstrap
        splitter = cherrypy.request.config['bootstrap.splitter']
        cherrypy.log("{}.GET invoked with {}".format(type(self).__name__, str(params)))
        rule_names = []
        for rule in parsed_bootstrap.rules:
            if type(rule) is RuleSet:
                css_names = rule.selector.as_css()
                rule_names.extend(css_names.split(splitter))
        rep = '","'.join(rule_names)
        rep = '["'+rep+'"]'
        return rep
#         return str(rule_names)

class StaticPage(object):
    exposed = True
#     @cherrypy.expose
#     def index(self):
#         pass

def parse_bootstrap(bootstrap_url):
    parser = tinycss.make_parser('page3')
    global parsed_bootstrap
    with urllib.request.urlopen(bootstrap_url) as url: 
        parsed_bootstrap = parser.parse_stylesheet_bytes(url.read())
        cherrypy.log("parsed bootstrap {} from {}".format(bootstrap_url, str(parsed_bootstrap)))

if __name__ == '__main__':

    cherrypy.tree.mount(
        BootstrapLookup(), '/bootstraplookup',
        "bootstraplookup.config"
    )
    
    app = cherrypy.tree.mount(
        StaticPage(), '/',
        "bootstraplookup.config"
    )
    
    # TODO write a tutorial on lambda
    # TODO dig why bootstrap.url returns error message in log
    cherrypy.engine.subscribe('start', lambda: parse_bootstrap(app.config['/']['bootstrap.url']))
    
    cherrypy.engine.start()
    cherrypy.engine.block()