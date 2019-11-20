import kivy
from kivy.app import App

#Widgets da interface
from kivy.uix.boxlayout import BoxLayout

from kivy.logger import Logger
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder

import sys

# Desabilita mensagens na tela
#Logger.disabled = True

#Desabilita vários toques 
Config.set("input", "mouse", "mouse, disable_multitouch")

#Configura tamanho inicial da tela
Window.size = (900, 600)

#Especifica o arquivo KV
Builder.load_file('ex01.kv')
    
class Main(BoxLayout):
  
  def onBtnCad(self):
    print("Cadastro")
    
  def onBtnSair(self):
    print("Sair")
    sys.exit(0)
  
class CadApp(App):
  def build(self):    
    self.title = 'App Cadastro 1'
        
    return Main()    

if __name__ == '__main__':
    CadApp().run()