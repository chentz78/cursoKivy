#Kivy imports
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty

from os.path import join, dirname, abspath

Builder.load_file(join(dirname(abspath(__file__)), 'cTable.kv'))


class BoxLayoutBC(BoxLayout):
  pass

class TableHeader(BoxLayoutBC):
    """Fixed table header that scrolls x with the data table"""

    def __init__(self, cTab, cols=None, colWidth=[], *args, **kwargs):
        super(TableHeader, self).__init__(*args, **kwargs)
        self.cTab = cTab
        self.fName = self.cTab.fName
        self.fSize = self.cTab.fSize
        defCWidth = 60
        w = 0
        for i in range(len(cols)):
          w = colWidth[i] if colWidth[i] else defCWidth
          lbl = Label(text=cols[i],size_hint=(None, 1),width=w,
              size=(w,self.height))
          lbl.padding = (0, 0)
          lbl.font_name = self.fName
          lbl.font_size = self.fSize
          lbl.bold = True
          lbl.texture_update()
          self.add_widget(lbl)
  
class TableData(RecycleView):
  nCols = NumericProperty(None)
  colsMin = DictProperty({})    
    
  def __init__(self, cTab, cols=[], dList=[], *args, **kwargs):
    self.cTab = cTab
    self.nCols = len(cols)    
    
    d = {i:cols[i] for i in range(len(cols))}    
    self.colsMin = d    
    #self.colsMin = DictProperty(dict(cols))
    
    super(TableData, self).__init__(*args, **kwargs)    
    #Config the style
    dgl = self.ids.dGLayout 
    dgl.default_size = (None, 20)
    dgl.default_size_hint=(1, None)
    dgl.size_hint=(None, None)    
    
    self.data = []
    for el in dList:
      for e in el:        
        self.data.append({'text':e})
    
class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super(SelectableLabel, self).__init__(*args, **kwargs)
      
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        
        self.index = index
        cTab = rv.parent.parent
        if cTab :
          self.font_name=cTab.fName
          self.font_size=cTab.fSize
        
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected        
            
class CTable(BoxLayout):
  '''Chentz Table implementation'''
  #Builtin fonts for Kivy: https://github.com/kivy/kivy/tree/master/kivy/data/fonts
  #_defFontName = 'Arial'
  #_defFontName = 'Roboto'
  _defFontName = 'DejaVuSans'  
  _defFontSize = 12
  scrollToBotton = True
  
  def __init__(self, *args, **kwargs):
    super(CTable, self).__init__(*args, **kwargs)
    self.fName = self._defFontName
    self.fSize = self._defFontSize
   
  def clear(self):
    self.clear_widgets()
    
  def calcSizeCols(self, cols, data, colMin=None):
    rt = []
    for i in range(len(cols)):
      s = len(cols[i])
      s = max(s, max([0]+[len(x[i]) for x in data if len(x)>0]))
        
      lbl = Label(text="Z"*s)
      lbl.font=self.fName
      lbl.font_size=self.fSize
      lbl.texture_update()
      cs = lbl.texture.size[0]       
      cs+= 20
      
      rt.append(cs)
      
    if colMin:
      for i in range(len(colMin)):
        if colMin[i] > rt[i]: rt[i] = colMin[i]          
      
    return rt
    
  def loadData(self, cols, cWidth, data):
    self.clear_widgets()
    cSizes = cWidth if cWidth else self.calcSizeCols(cols, data)
    self.__tHeader = TableHeader(self, cols, cSizes)
    self.__tData = TableData(self, cSizes, data)
    
    self.__cont = GridLayout(cols=1, rows=3)
    self.__cont.add_widget(self.__tHeader)
    self.__cont.add_widget(self.__tData)
    self.add_widget(self.__cont)
    
    if self.scrollToBotton : self.__tData.scroll_y = 0
    
if __name__ == '__main__':
  from kivy.app import App
  from kivy.config import Config
  
  Config.set("input", "mouse", "mouse, disable_multitouch")
  
  class CTableTest(App):
    def build(self):
      self.title = 'chentz Table Test'
      main_window = CTable()
      return main_window
    
  CTableTest().run()