import xml.sax
import re
from xml.sax.xmlreader import AttributesImpl
class MarkupHandler(xml.sax.ContentHandler):
    passthrough = False
    def startElement(self, name, attrs):
        self.start_tag= name
        if self.start_tag == "page":
            self.passthrough = True
            self.out = open(attrs["name"]+".html","w")
            self.out.write("<html><head>\n")
            self.out.write("<title>{}</title>\n".format(attrs["title"]))
            self.out.write("</head><body>\n")
        elif self.passthrough:
            self.out.write("\n<{}".format(self.start_tag))
            for key ,value in attrs.items():
                print(attrs.items()) 
                self.out.write(" {}={}".format(key,value))
            self.out.write(">")
            
    def characters(self, chars):
        if self.passthrough: #re .match for cleaning html file, not actually necessary
            self.out.write(chars)
    def endElement(self, name):
        if name == "page":
            self.passthrough = False
            self.out.write("\n</body></html>")
            self.out.close()
        elif self.passthrough and name == "ul":
            self.out.write(f"\n</{name}>")
        elif self.passthrough:
            self.out.write(f"</{name}>")
        self.start_tag = ""
            


handler = MarkupHandler()
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
parser.parse("website.xml")