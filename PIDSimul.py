import sys
from PySide.QtCore import *
from PySide.QtGui import *
import inspect
import math as m
import random

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

        PKenttä = QLineEdit("0")
        IKenttä = QLineEdit("0")
        DKenttä = QLineEdit("0")

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

        def PäivitäPOhjain():
            try:
                POhjain.setValue(float(PKenttä.text())*5)
            except:
                pass

        def PäivitäIOhjain():
            try:
                IOhjain.setValue(float(IKenttä.text())*5)
            except:
                pass

        def PäivitäDOhjain():
            try:
                DOhjain.setValue(float(DKenttä.text())*5)
            except:
                pass
        
        self.connect(POhjain,SIGNAL("sliderReleased()"), PäivitäPKenttä)
        self.connect(IOhjain,SIGNAL("sliderReleased()"), PäivitäIKenttä)
        self.connect(DOhjain,SIGNAL("sliderReleased()"), PäivitäDKenttä)

        self.connect(PKenttä,SIGNAL("editingFinished()"), PäivitäPOhjain)

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
        
        sisäSignAlkuPiste = round(SisäSignNäkymä.width()/1.5)
        sisäSignLeveys = int(round(SisäSignNäkymä.width()/1.5))
        sigY = 20*m.sin((sisäSignLeveys-10)*0.1)

        self.summainKertymä = 0
                        
        
        def käyrienSiirto():

            askel = 4
            #"Data sisään"
            dataPiste = random.randint(-30,30)

            #Näkymän rajan asettelu (Skaalauksen muuttuessa vielä TODO bugikorjausta
            #signaalin piirtymisessä)
            
            alku = round(SisäSignNäkymä.width())
            summaAlku = round(UlosSignNäkymä.width())

            Palku = round(PSignNäkymä.width())
            Ialku = round(ISignNäkymä.width())
            Dalku = round(DSignNäkymä.width())

            PKäyränPalat = PSignNäytös.items()
            IKäyränPalat = ISignNäytös.items()
            DKäyränPalat = DSignNäytös.items()
            
            käyränPalat = SisäänSignNäytös.items()
            summaKäyränPalat = UlosSignNäytös.items()
            

            ########## Syötesignaalin käyrän piirto ################
            
            janaSiirretty = 0
            for pätkä in käyränPalat:                
                xYksi = pätkä.line().x1()
                xKaksi = pätkä.line().x2()
                yYksi = pätkä.line().y1()
                yKaksi = pätkä.line().y2()
                
                
                if xKaksi < askel:
                    pätkä.setLine(xYksi+askel,yYksi,xKaksi+askel,yKaksi)
                    
                else:                    
                    janaSiirretty +=1
                    
                    if janaSiirretty >= 2:
                        poistettavaIndeksi = SisäänSignNäytös.items().index(pätkä)
                        SisäänSignNäytös.removeItem(SisäänSignNäytös.items()[poistettavaIndeksi])
                    try:
                        pätkä.setLine(-alku,dataPiste,-alku+askel,self.viimeSigYYksi)
                        self.viimeDataPiste = self.viimeSigYYksi
                    except:
                        pätkä.setLine(-alku,dataPiste,-alku+askel,0)
                        self.viimeDataPiste = 0
                    
                    viimeSiirtoJana = pätkä
                    self.viimeSigYYksi = viimeSiirtoJana.line().y1()
            if janaSiirretty == 0:
                try:
                    SisäänSignNäytös.addLine(-alku,dataPiste,-alku+askel,self.viimeSigYYksi)
                    self.viimeDataPiste = self.viimeSigYYksi
                except:
                    pass
                self.viimeSigYYksi = dataPiste

            #Datapisteiden siirto derivointia ja integrointia varten
            
            seurDataPiste = dataPiste
            

            ############## P-Käyrän piirto #################

            try:
                PdataPiste = dataPiste*float(PKenttä.text())
            except:
                PdataPiste = 0
            PjanaSiirretty = 0
            for Ppätkä in PKäyränPalat:                
                PxYksi = Ppätkä.line().x1()
                PxKaksi = Ppätkä.line().x2()
                PyYksi = Ppätkä.line().y1()
                PyKaksi = Ppätkä.line().y2()
                
                
                if PxKaksi < askel:
                    Ppätkä.setLine(PxYksi+askel,PyYksi,PxKaksi+askel,PyKaksi)
                    
                else:                    
                    PjanaSiirretty +=1
                    
                    if PjanaSiirretty >= 2:
                        PpoistettavaIndeksi = PSignNäytös.items().index(Ppätkä)
                        PSignNäytös.removeItem(PSignNäytös.items()[PpoistettavaIndeksi])
                    try:
                        Ppätkä.setLine(-Palku,PdataPiste,-Palku+askel,self.PviimeSigYYksi)    
                    except:
                        Ppätkä.setLine(-Palku,PdataPiste,-Palku+askel,0)
                    
                    PviimeSiirtoJana = Ppätkä
                    self.PviimeSigYYksi = PviimeSiirtoJana.line().y1()
            if PjanaSiirretty == 0:
                try:
                    PSignNäytös.addLine(-Palku,PdataPiste,-Palku+askel,self.PviimeSigYYksi)
                except:
                    pass
                self.PviimeSigYYksi = PdataPiste

            ########### I-käyrän piirto ####################
            
            try:
                self.summainKertymä += (self.viimeDataPiste-seurDataPiste)*askel/2*float(IKenttä.text())
                IdataPiste = self.summainKertymä
            except:
                IdataPiste = 0

            IjanaSiirretty = 0
            for Ipätkä in IKäyränPalat:                
                IxYksi = Ipätkä.line().x1()
                IxKaksi = Ipätkä.line().x2()
                IyYksi = Ipätkä.line().y1()
                IyKaksi = Ipätkä.line().y2()
                
                
                if IxKaksi < askel:
                    Ipätkä.setLine(IxYksi+askel,IyYksi,IxKaksi+askel,IyKaksi)
                    
                else:                    
                    IjanaSiirretty +=1
                    
                    if IjanaSiirretty >= 2:
                        IpoistettavaIndeksi = ISignNäytös.items().index(Ipätkä)
                        ISignNäytös.removeItem(ISignNäytös.items()[IpoistettavaIndeksi])
                    try:
                        Ipätkä.setLine(-Ialku,IdataPiste,-Ialku+askel,self.IviimeSigYYksi)    
                    except:
                        Ipätkä.setLine(-Ialku,IdataPiste,-Ialku+askel,0)
                    
                    IviimeSiirtoJana = Ipätkä
                    self.IviimeSigYYksi = IviimeSiirtoJana.line().y1()
            if IjanaSiirretty == 0:
                try:
                    ISignNäytös.addLine(-Ialku,IdataPiste,-Ialku+askel,self.IviimeSigYYksi)
                except:
                    pass
                self.IviimeSigYYksi = IdataPiste

            ############## D-käyrän piirto ####################

            try:
                DdataPiste = (self.viimeDataPiste-seurDataPiste)/askel*float(DKenttä.text())
            except:
                DdataPiste = 0
            #DdataPiste = dataPiste*float(DKenttä.text())
            DjanaSiirretty = 0
            for Dpätkä in DKäyränPalat:                
                DxYksi = Dpätkä.line().x1()
                DxKaksi = Dpätkä.line().x2()
                DyYksi = Dpätkä.line().y1()
                DyKaksi = Dpätkä.line().y2()
                
                
                if DxKaksi < askel:
                    Dpätkä.setLine(DxYksi+askel,DyYksi,DxKaksi+askel,DyKaksi)
                    
                else:                    
                    DjanaSiirretty +=1
                    
                    if DjanaSiirretty >= 2:
                        DpoistettavaIndeksi = DSignNäytös.items().index(Dpätkä)
                        DSignNäytös.removeItem(DSignNäytös.items()[DpoistettavaIndeksi])
                    try:
                        Dpätkä.setLine(-Dalku,DdataPiste,-Dalku+askel,self.DviimeSigYYksi)    
                    except:
                        Dpätkä.setLine(-Dalku,DdataPiste,-Dalku+askel,0)
                    
                    DviimeSiirtoJana = Dpätkä
                    self.DviimeSigYYksi = DviimeSiirtoJana.line().y1()
            if DjanaSiirretty == 0:
                try:
                    DSignNäytös.addLine(-Dalku,DdataPiste,-Dalku+askel,self.DviimeSigYYksi)
                except:
                    pass
                self.DviimeSigYYksi = DdataPiste
            
            ######## Summa(ulostulo)käyrän piirto ################

            summaDataPiste = PdataPiste+IdataPiste+DdataPiste

            summaJanaSiirretty = 0
            for summaPätkä in summaKäyränPalat:                
                summaxYksi = summaPätkä.line().x1()
                summaxKaksi = summaPätkä.line().x2()
                summayYksi = summaPätkä.line().y1()
                summayKaksi = summaPätkä.line().y2()
                
                
                if summaxKaksi < askel:
                    summaPätkä.setLine(summaxYksi+askel,summayYksi,summaxKaksi+askel,summayKaksi)
                    
                else:                    
                    summaJanaSiirretty +=1
                    
                    if summaJanaSiirretty >= 2:
                        summaPoistettavaIndeksi = UlosSignNäytös.items().index(summaPätkä)
                        UlosSignNäytös.removeItem(UlosSignNäytös.items()[summaPoistettavaIndeksi])
                    try:
                        summaPätkä.setLine(-summaAlku,summaDataPiste,-summaAlku+askel,self.summaViimeSigYYksi)    
                    except:
                        summaPätkä.setLine(-summaAlku,summaDataPiste,-summaAlku+askel,0)
                    
                    summaViimeSiirtoJana = summaPätkä
                    self.summaViimeSigYYksi = summaViimeSiirtoJana.line().y1()
            if summaJanaSiirretty == 0:
                try:
                    UlosSignNäytös.addLine(-summaAlku,summaDataPiste,-summaAlku+askel,self.summaViimeSigYYksi)
                except:
                    pass
                self.summaViimeSigYYksi = summaDataPiste            

    
            #Ledi kiinni kanavaan 12
            #Etuvastuksella 330R-470R
                
            #print(pätkä.line().x1())

        tick = QTimer(self)
        tick.start(50)

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

        
