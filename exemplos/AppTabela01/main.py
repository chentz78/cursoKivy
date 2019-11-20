import kivy
from kivy.app import App

#Widgets da interface
from kivy.uix.boxlayout import BoxLayout

#Importa componente de Tabela
import cTable

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
Builder.load_file('main.kv')
    
class Main(BoxLayout):
  
  def onBtnCarga(self):
    print("Carga")
    
    #Acessa componente pelo id definido no arq kv
    tab = self.ids.tabEx
    
    dt = [] #Lista que vai manter os dados
    #Lista com texto dos cabeçalho
    colunasCab = ["Nome", "Idade", "Endereço"]
    colWidth = None #Usado apenas quando quiser definir a largura das colunas manualmente
    
    #Gerando dados aleatórios
    for i in range(20):
      ##Lista dos valores para uma determinada linha
      dt.append(["Aluno " + str(i), str(i*2), 'Rua ' + str(i*3)])
      
    #Carga dos dados na tabela
    tab.loadData(colunasCab, colWidth, dt) 
    
  def onBtnSair(self):
    print("Sair")
    sys.exit(0)
  
class TabelaApp(App):
  def build(self):    
    self.title = 'App Tabela 1'
        
    return Main()    

if __name__ == '__main__':
    TabelaApp().run()