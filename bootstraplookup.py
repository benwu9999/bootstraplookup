import cherrypy
      
class BootstrapLookup(object):
    exposed = True
    
    def _cp_dispatch(self, vpath):
        print(vpath)
    
    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return """{"suggestions": ["United Arab Emirates", "United States"]}"""

class StaticPage(object):
    exposed = True
#     @cherrypy.expose
#     def index(self):
#         pass

#cherrypy.quickstart(BootstrapLookup(), "/", "bootstrapLookup.config")
if __name__ == '__main__':

    cherrypy.tree.mount(
        BootstrapLookup(), '/bootstraplookup',
        "bootstraplookup.config"
    )
    
    cherrypy.tree.mount(
        StaticPage(), '/',
        "bootstraplookup.config"
    )
    
    cherrypy.engine.start()
    cherrypy.engine.block()