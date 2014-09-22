import sys
from PySide.QtCore import *
from PySide.QtGui import *
import inspect
import math as m

import atexit
#import pyaudio
import wave
import threading
import platform

class SignaaliKäyrä(QPainterPath):
    def __init__(self, parent=None):
        super(SignaaliKäyrä, self).__init__(parent)

    def getPos():
        print(self.currentPosition)

class Form(QDialog):    

    

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("PID-säädin")        

        #Tekstikilvet
        POhjKilpi = QLabel("Proportionaalikerroin")
        IOhjKilpi = QLabel("Integraalikerroin")
        DOhjKilpi = QLabel("Differentiaalikerroin")

        SigSisäänKilpi = QLabel("Signaali sisään")
        SigUlosKilpi = QLabel("Signaali ulos")

        PKomponenttiKilpi = QLabel("P-komponentti")
        IKomponenttiKilpi = QLabel("I-komponentti")
        DKomponenttiKilpi = QLabel("D-komponentti")

        #Vääntönapit

        POhjain = QDial()
        IOhjain = QDial()
        DOhjain = QDial()

        #Syötekentät

        PKenttä = QLineEdit()
        IKenttä = QLineEdit()
        DKenttä = QLineEdit()

        #Piirtoalueet

        SisäSignNäkymä = QGraphicsView()
        UlosSignNäkymä = QGraphicsView()
        
        PSignNäkymä = QGraphicsView()
        ISignNäkymä = QGraphicsView()
        DSignNäkymä = QGraphicsView()

        SisäänSignNäytös = QGraphicsScene()
        UlosSignNäytös = QGraphicsScene()

        PSignNäytös = QGraphicsScene()
        ISignNäytös = QGraphicsScene()
        DSignNäytös = QGraphicsScene()

        SisäSignNäkymä.setScene(SisäänSignNäytös)
        UlosSignNäkymä.setScene(UlosSignNäytös)
        
        PSignNäkymä.setScene(PSignNäytös)
        ISignNäkymä.setScene(ISignNäytös)
        DSignNäkymä.setScene(DSignNäytös)

        #Taustalayout
        hyllystö = QVBoxLayout()

        #Ohjainten sijoittelu
        
        OhjainRivi = QHBoxLayout()
        hyllystö.addLayout(OhjainRivi)
        
        POhjLaatikko = QVBoxLayout()
        IOhjLaatikko = QVBoxLayout()
        DOhjLaatikko = QVBoxLayout()
        PDialJaLineBox = QHBoxLayout()
        IDialJaLineBox = QHBoxLayout()
        DDialJaLineBox = QHBoxLayout()

        OhjainRivi.addLayout(POhjLaatikko)
        OhjainRivi.addLayout(IOhjLaatikko)
        OhjainRivi.addLayout(DOhjLaatikko)

        #Ensimmäisen rivin kilvet

        POhjLaatikko.addWidget(POhjKilpi)
        IOhjLaatikko.addWidget(IOhjKilpi)
        DOhjLaatikko.addWidget(DOhjKilpi)

        #Dialien ja LineEditien tilat kilpien alla

        POhjLaatikko.addLayout(PDialJaLineBox)
        IOhjLaatikko.addLayout(IDialJaLineBox)
        DOhjLaatikko.addLayout(DDialJaLineBox)

        #Kääntönapit ja syötekentät

        PDialJaLineBox.addWidget(POhjain)
        PDialJaLineBox.addWidget(PKenttä)

        IDialJaLineBox.addWidget(IOhjain)
        IDialJaLineBox.addWidget(IKenttä)

        DDialJaLineBox.addWidget(DOhjain)
        DDialJaLineBox.addWidget(DKenttä)

        def PäivitäPKenttä():
            PKenttä.setText(str(round(POhjain.value()*0.2,2)))

        def PäivitäIKenttä():
            IKenttä.setText(str(round(IOhjain.value()*0.2,2)))

        def PäivitäDKenttä():
            DKenttä.setText(str(round(DOhjain.value()*0.2,2)))
        
        self.connect(POhjain,SIGNAL("sliderReleased()"), PäivitäPKenttä)
        self.connect(IOhjain,SIGNAL("sliderReleased()"), PäivitäIKenttä)
        self.connect(DOhjain,SIGNAL("sliderReleased()"), PäivitäDKenttä)

        #Tulo- ja lähtösignaalien alueet

        SignaaliLaatikkoRivi = QHBoxLayout()
        hyllystö.addLayout(SignaaliLaatikkoRivi)
        SisäänSignLaatikko = QVBoxLayout()
        UlosSignLaatikko = QVBoxLayout()

        SignaaliLaatikkoRivi.addLayout(SisäänSignLaatikko)
        SignaaliLaatikkoRivi.addLayout(UlosSignLaatikko)
        
        SisäänSignLaatikko.addWidget(SisäSignNäkymä)
        UlosSignLaatikko.addWidget(UlosSignNäkymä)

        SisäänSignLaatikko.addWidget(SigSisäänKilpi)
        UlosSignLaatikko.addWidget(SigUlosKilpi)

        #Komponenttirivi

        KomponenttiRivi = QHBoxLayout()
        hyllystö.addLayout(KomponenttiRivi)
        PKompLaatikko = QVBoxLayout()
        IKompLaatikko = QVBoxLayout()
        DKompLaatikko = QVBoxLayout()
        KomponenttiRivi.addLayout(PKompLaatikko)
        KomponenttiRivi.addLayout(IKompLaatikko)
        KomponenttiRivi.addLayout(DKompLaatikko)

        #Komponenttirivin piirtoalueet        

        PKompLaatikko.addWidget(PSignNäkymä)
        PKompLaatikko.addWidget(PKomponenttiKilpi)

        IKompLaatikko.addWidget(ISignNäkymä)
        IKompLaatikko.addWidget(IKomponenttiKilpi)
        
        DKompLaatikko.addWidget(DSignNäkymä)
        DKompLaatikko.addWidget(DKomponenttiKilpi)        

        #Funktioiden kuvaajia varten aloitettavat kynät ja pensselit

        kaariKynä = QPen()

        kaariPensseli = QBrush()

        #Funktioiden polkujen piirto
        
        sisäSignAlkuPiste = round(SisäSignNäkymä.width()/2)
        sisäSignLeveys = int(round(SisäSignNäkymä.width()/2))
        sigY = 20*m.sin((sisäSignLeveys-2)*0.1)

        """
        

                

        
            #nextX = syötePolku.currentPosition().toTuple()[0]
            #nextY = syötePolku.currentPosition().toTuple()[1]+5
            #syötePolku.translate(nextX,nextY)
            #SisäänSignNäytös.update()
        """ 
        """
            try:
                paikka+=4
            except:
                paikka=0
            

            
            
            
            #print(SisäSignNäkymä.width())
            syötePolku.moveTo(sisäSignAlkuPiste+30+paikka,0)
        """
        while sisäSignLeveys > 2:
            sisäSignLeveys-=2
            
            sigYsec = 20*m.sin(sisäSignLeveys*0.1)
            SisäänSignNäytös.addLine(-sisäSignLeveys,sigY,-sisäSignLeveys+2,sigYsec,kaariKynä)
            sigY = 20*m.sin((sisäSignLeveys+2)*0.1)

        
        def käyrienSiirto():
            käyränPalat = SisäänSignNäytös.items()
            print(dir(käyränPalat[0]))
            #for pätkä in käyränPalat:
            #    pätkä.trans+=5

        tick = QTimer(self)
        tick.start(100)

        #print(SisäänSignNäytös.items())
        
        #self.connect(tick,SIGNAL("timeout()"),uudelleenPiirto)
        self.connect(tick,SIGNAL("timeout()"),käyrienSiirto)

        
        

        #self.showMaximized()
        self.setLayout(hyllystö)

        """
        def uudelleenPiirto():
            SisäänSignNäytös.clear()
            print("dirr")
            sisäSignAlkuPiste = round(SisäSignNäkymä.width()/2)
            sisäSignLeveys = int(round(SisäSignNäkymä.width()/2))
            sigY = 20*m.sin((sisäSignLeveys-2)*0.1)
                
            while sisäSignLeveys > 2:
                sisäSignLeveys-=2
                
                sigYsec = 20*m.sin(sisäSignLeveys*0.1)
                SisäänSignNäytös.addLine(-sisäSignLeveys,sigY,-sisäSignLeveys+2,sigYsec,kaariKynä)
                sigY = 20*m.sin((sisäSignLeveys+2)*0.1)
            SisäänSignNäytös.advance()    
                
            

        
        """
    
        
app = QApplication(sys.argv)
#Cleanup on exit

form = Form()
#form.connect(app,SIGNAL("aboutToQuit()"),clearSound)
form.show()
app.exec_()

        
