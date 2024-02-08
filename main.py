import xml.sax
import os
from xml.sax import ContentHandler
class MethodSelector:
    # will be in start elemnt method
    def call_method(self,prefix,name,attrs=None):
        mname = prefix+name.capitalize() #methodname for page, directory
        dname = "default"+prefix.capitalize() #defaultname
        method = getattr(self,mname,None)
        if callable(method): args = () # needs more than one arg, so tuple
        else:
            method = getattr(self,dname,None)
            if callable(method): args = name, 
# because a default(li,h1,p) only needs name, as in    defaultStart("li")
        if prefix == "start": args += attrs,
        if callable(method): method(*args)
    
    def startElement(self,name,attrs):
        self.call_method("start",name,attrs)
    
    def endElement(self,name):
        self.call_method("end",name)

# types of tags to take care of: page, directory, and rest of the other (default) tags
class MarkupHandler(MethodSelector,ContentHandler):
    in_page = False
    def __init__(self,directory):
        self.directory = [directory]
        self.implementDirectory()
    def implementDirectory(self):
        current_path = os.path.join(*self.directory)
        os.makedirs(current_path,exist_ok=True)
        # current_path = os.path.join(*self.directory)
    
    def startPage(self,attrs):
        self.in_page = True
        self.title = f"{attrs['title']}"
        self.name = f"{attrs['name']}"+".html"
        filename = os.path.join(*self.directory,self.name)
        self.out = open(filename,"w")
        self.writeHeader()
    def endPage(self):
        self.in_page = False
        self.writeFooter()
        self.out.close()
    
    def defaultStart(self,name,attrs):
        if self.in_page:
            self.out.write(f"<{name}")
            for key,value in attrs.items():
                self.out.write(f" {key}= {value}")
            if name == "ul":self.out.write(">\n")
            else: self.out.write(">")
    def defaultEnd(self,name):
        if self.in_page:
            self.out.write(f"</{name}>\n")
    def characters(self, content: str):
        if self.in_page :
            self.out.write(content)
    def writeHeader(self):
        self.out.write(f"<html><head>\n<title>{self.title}</title>\n</head><body>\n")
    def writeFooter(self):
        self.out.write(f"\n</body></html>\n")

    def startDirectory(self,attrs):
        self.directory.append(attrs["name"])
        self.implementDirectory()

    def endDirectory(self):
        self.directory.pop()

handler = MarkupHandler("website")
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
parser.parse("website.xml")

