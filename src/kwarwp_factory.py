"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/01/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: ©2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2013/01/09 $Date$"
"""
def noop(nop=''):
    pass
HANDLER = {"_NOOP_":'noop()'}
VKHANDLER = dict([(k,noop) for k in range(32,40)])

def uuid():
    r = jsptrand()
    return '%i'%(JSObject(jsptdate).getTime()*1000+r)

def jshandler(event):
    code = event.keyCode
    if code in VKHANDLER:
        VKHANDLER[code]()
    #alert(event.keyCode)
    
doc.onkeypress=jshandler

def eventify(owner):
    #alert('owner :'+owner)
    HANDLER[owner]()

class GUI:
    def __init__(self,panel):
        self.args = {}
        self.panel =panel
        
    def get_args(self):
        args = self.args
        for key, value in self.args.items():
            args[key]= 'eventify(\\"%s\\")'%value
        self.args = {}
        p='"'
        if len(args) != 0:
            args = ', '+','.join(['%s = %s%s%s'%(k,p,v,p)
                                     for k, v in args.items()])
        else:
            args = ''
        return args
            

    def text(self, text,x=150,y=25, font_size=22,text_anchor="middle",
      style= {}):
      element = SVG.text(text,x=x,y=y,
      font_size=font_size,text_anchor=text_anchor,
      style=style)
      self.panel <= element
      return element
  
    def path(self, d,style={}, onMouseOver="noop",  onMouseOut="noop"):
        exec('element = SVG.path(d=%s,style=%s%s)'%(
            str(d),str(style),self.get_args()))
        self.panel <= element
        return element
  
    def image(self,  href, x=0, y=0, width=100, height=50):
        exec('element = SVG.image(href="%s", x=%i, y=%i, width=%i, height=%i%s)'%(
            href, x, y, width, height,self.get_args()))
        self.panel <= element
        return element
  
    def rect(self, x=0, y=0, width=100, height=50,style={}):
        exec('element = SVG.rect(x=%i, y=%i, width=%i, height=%i,style=%s%s)'%(
            x, y, width, height,str(style),self.get_args()))
        self.panel <= element
        return element
    
    def _decorate(self, handler, **kw):
      self.args = {} #kw #dict(kw)
      #alert(' '.join([k for k,v in kw.items()]))
      for key, value in kw.items():
          handler_id = uuid()
          HANDLER[handler_id] = handler
          self.args[key] = handler_id
          #alert(key+':'+ self.args[key])
          x =self.args
      #alert(' ,'.join([k+':'+v for k,v in x.items()]))
      return self
    def click(self,handler):
      self._decorate(handler, onClick=handler)
      return self
    def over(self,handler):
      self._decorate(handler, onMouseOver=handler)
      return self
        
class Avatar:
    def _load_images(self,img,gui):
        cardinames = [c for c in 'nesw']
        self.images =[]
        for direction in cardinames:
            line = []
            for step in range(3):
                im = gui.image(href=img%(direction,step),
                    x=100,y=100, width=32,height=32)
                im.setAttribute("visibility",'hidden')
                line.append(im)
            self.images.append(line)
        self.heading = 1
        self.current = 0
    def _show(self):
        self.current = (self.current + 1) % 3
        self.avatar.setAttribute("visibility",'hidden')
        self.avatar= self.images[self.heading][self.current]
        self.avatar.setAttribute('x', self.x) 
        self.avatar.setAttribute('y', self.y)
        self.avatar.setAttribute("visibility",'visible')
    def move(self, x, y):
        self.x, self.y = x, y
        self._show()
    def go_left(self):
        self.heading = (self.heading - 1)%4
        self._show()
    def go_right(self):
        self.heading = (self.heading + 1)%4
        self._show()

    def __init__(self,gui):
        VKHANDLER[37]=self.go_left
        VKHANDLER[39]=self.go_right
        print( 'Avatar,init') 
        self.x, self.y = 0, 0
        self._load_images(REPO%'smkp-%s0%d.gif',gui)
        self.avatar = self.images[self.heading][self.current]

class Sprite:
    def _show(self, x, y):
        self.avatar.setAttribute('x', x) 
        self.avatar.setAttribute('y', y)
        self.avatar.setAttribute("visibility",'visible')
    def move(self, place,x,y):
        self.place, self.x, self.y = place, x, y
        self._show(*place.get_position(x=x,y=y))
    def __init__(self,gui, img, place, x, y):
        self.avatar = gui.image(href=REPO%img,
                    x=100,y=100, width=32,height=32)
        self.move(place, x, y)
