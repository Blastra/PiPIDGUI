import sys
from PySide.QtCore import *
from PySide.QtGui import *
import inspect

import atexit
#import pyaudio
import wave
import threading
import platform

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

        

        #asd

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

        self.showMaximized()
        self.setLayout(hyllystö)
        
        
app = QApplication(sys.argv)
#Cleanup on exit

form = Form()
#form.connect(app,SIGNAL("aboutToQuit()"),clearSound)
form.show()
app.exec_()

        
