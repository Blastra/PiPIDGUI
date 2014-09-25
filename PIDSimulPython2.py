#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

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


class SignaaliKayra(QPainterPath):
    def __init__(self, parent=None):
        super(SignaaliKayra, self).__init__(parent)

    def getPos():
        print(self.currentPosition)

class Form(QDialog):    

    

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("PID-saadin")        

        #Tekstikilvet
        POhjKilpi = QLabel("Proportionaalikerroin")
        IOhjKilpi = QLabel("Integraalikerroin")
        DOhjKilpi = QLabel("Differentiaalikerroin")

        SigSisaanKilpi = QLabel("Signaali sisaan")
        SigUlosKilpi = QLabel("Signaali ulos")

        PKomponenttiKilpi = QLabel("P-komponentti")
        IKomponenttiKilpi = QLabel("I-komponentti")
        DKomponenttiKilpi = QLabel("D-komponentti")

        #Vaantonapit

        POhjain = QDial()
        IOhjain = QDial()
        DOhjain = QDial()

        #Syotekentat

        PKentta = QLineEdit("0")
        IKentta = QLineEdit("0")
        DKentta = QLineEdit("0")

        #Piirtoalueet

        SisaSignNakyma = QGraphicsView()
        UlosSignNakyma = QGraphicsView()
        
        PSignNakyma = QGraphicsView()
        ISignNakyma = QGraphicsView()
        DSignNakyma = QGraphicsView()

        SisaanSignNaytos = QGraphicsScene()
        UlosSignNaytos = QGraphicsScene()

        PSignNaytos = QGraphicsScene()
        ISignNaytos = QGraphicsScene()
        DSignNaytos = QGraphicsScene()

        SisaSignNakyma.setScene(SisaanSignNaytos)
        UlosSignNakyma.setScene(UlosSignNaytos)
        
        PSignNakyma.setScene(PSignNaytos)
        ISignNakyma.setScene(ISignNaytos)
        DSignNakyma.setScene(DSignNaytos)

        #Taustalayout
        hyllysto = QVBoxLayout()

        #Ohjainten sijoittelu
        
        OhjainRivi = QHBoxLayout()
        hyllysto.addLayout(OhjainRivi)
        
        POhjLaatikko = QVBoxLayout()
        IOhjLaatikko = QVBoxLayout()
        DOhjLaatikko = QVBoxLayout()
        PDialJaLineBox = QHBoxLayout()
        IDialJaLineBox = QHBoxLayout()
        DDialJaLineBox = QHBoxLayout()

        OhjainRivi.addLayout(POhjLaatikko)
        OhjainRivi.addLayout(IOhjLaatikko)
        OhjainRivi.addLayout(DOhjLaatikko)

        #Ensimmaisen rivin kilvet

        POhjLaatikko.addWidget(POhjKilpi)
        IOhjLaatikko.addWidget(IOhjKilpi)
        DOhjLaatikko.addWidget(DOhjKilpi)

        #Dialien ja LineEditien tilat kilpien alla

        POhjLaatikko.addLayout(PDialJaLineBox)
        IOhjLaatikko.addLayout(IDialJaLineBox)
        DOhjLaatikko.addLayout(DDialJaLineBox)

        #Kaantonapit ja syotekentat

        PDialJaLineBox.addWidget(POhjain)
        PDialJaLineBox.addWidget(PKentta)

        IDialJaLineBox.addWidget(IOhjain)
        IDialJaLineBox.addWidget(IKentta)

        DDialJaLineBox.addWidget(DOhjain)
        DDialJaLineBox.addWidget(DKentta)

        def PaivitaPKentta():
            PKentta.setText(str(round(POhjain.value()*0.2,2)))

        def PaivitaIKentta():
            IKentta.setText(str(round(IOhjain.value()*0.2,2)))

        def PaivitaDKentta():
            DKentta.setText(str(round(DOhjain.value()*0.2,2)))

        def PaivitaPOhjain():
            try:
                POhjain.setValue(float(PKentta.text())*5)
            except:
                pass

        def PaivitaIOhjain():
            try:
                IOhjain.setValue(float(IKentta.text())*5)
            except:
                pass

        def PaivitaDOhjain():
            try:
                DOhjain.setValue(float(DKentta.text())*5)
            except:
                pass
        
        self.connect(POhjain,SIGNAL("sliderReleased()"), PaivitaPKentta)
        self.connect(IOhjain,SIGNAL("sliderReleased()"), PaivitaIKentta)
        self.connect(DOhjain,SIGNAL("sliderReleased()"), PaivitaDKentta)

        self.connect(PKentta,SIGNAL("editingFinished()"), PaivitaPOhjain)

        #Tulo- ja lahtosignaalien alueet

        SignaaliLaatikkoRivi = QHBoxLayout()
        hyllysto.addLayout(SignaaliLaatikkoRivi)
        SisaanSignLaatikko = QVBoxLayout()
        UlosSignLaatikko = QVBoxLayout()

        SignaaliLaatikkoRivi.addLayout(SisaanSignLaatikko)
        SignaaliLaatikkoRivi.addLayout(UlosSignLaatikko)
        
        SisaanSignLaatikko.addWidget(SisaSignNakyma)
        UlosSignLaatikko.addWidget(UlosSignNakyma)

        SisaanSignLaatikko.addWidget(SigSisaanKilpi)
        UlosSignLaatikko.addWidget(SigUlosKilpi)

        #Komponenttirivi

        KomponenttiRivi = QHBoxLayout()
        hyllysto.addLayout(KomponenttiRivi)
        PKompLaatikko = QVBoxLayout()
        IKompLaatikko = QVBoxLayout()
        DKompLaatikko = QVBoxLayout()
        KomponenttiRivi.addLayout(PKompLaatikko)
        KomponenttiRivi.addLayout(IKompLaatikko)
        KomponenttiRivi.addLayout(DKompLaatikko)

        #Komponenttirivin piirtoalueet        

        PKompLaatikko.addWidget(PSignNakyma)
        PKompLaatikko.addWidget(PKomponenttiKilpi)

        IKompLaatikko.addWidget(ISignNakyma)
        IKompLaatikko.addWidget(IKomponenttiKilpi)
        
        DKompLaatikko.addWidget(DSignNakyma)
        DKompLaatikko.addWidget(DKomponenttiKilpi)        

        #Funktioiden kuvaajia varten aloitettavat kynat ja pensselit

        kaariKyna = QPen()

        kaariPensseli = QBrush()

        #Funktioiden polkujen piirto
        
        sisaSignAlkuPiste = round(SisaSignNakyma.width()/1.5)
        sisaSignLeveys = int(round(SisaSignNakyma.width()/1.5))
        sigY = 20*m.sin((sisaSignLeveys-10)*0.1)

        self.summainKertyma = 0
                        
        
        def kayrienSiirto():

            askel = 4
            #"Data sisaan"
            dataPiste = random.randint(-30,30)

            #Nakyman rajan asettelu (Skaalauksen muuttuessa viela TODO bugikorjausta
            #signaalin piirtymisessa)
            
            alku = round(SisaSignNakyma.width())
            summaAlku = round(UlosSignNakyma.width())

            Palku = round(PSignNakyma.width())
            Ialku = round(ISignNakyma.width())
            Dalku = round(DSignNakyma.width())

            PKayranPalat = PSignNaytos.items()
            IKayranPalat = ISignNaytos.items()
            DKayranPalat = DSignNaytos.items()
            
            kayranPalat = SisaanSignNaytos.items()
            summaKayranPalat = UlosSignNaytos.items()
            

            ########## Syotesignaalin kayran piirto ################
            
            janaSiirretty = 0
            for patka in kayranPalat:                
                xYksi = patka.line().x1()
                xKaksi = patka.line().x2()
                yYksi = patka.line().y1()
                yKaksi = patka.line().y2()
                
                
                if xKaksi < askel:
                    patka.setLine(xYksi+askel,yYksi,xKaksi+askel,yKaksi)
                    
                else:                    
                    janaSiirretty +=1
                    
                    if janaSiirretty >= 2:
                        poistettavaIndeksi = SisaanSignNaytos.items().index(patka)
                        SisaanSignNaytos.removeItem(SisaanSignNaytos.items()[poistettavaIndeksi])
                    try:
                        patka.setLine(-alku,dataPiste,-alku+askel,self.viimeSigYYksi)
                        self.viimeDataPiste = self.viimeSigYYksi
                    except:
                        patka.setLine(-alku,dataPiste,-alku+askel,0)
                        self.viimeDataPiste = 0
                    
                    viimeSiirtoJana = patka
                    self.viimeSigYYksi = viimeSiirtoJana.line().y1()
            if janaSiirretty == 0:
                try:
                    SisaanSignNaytos.addLine(-alku,dataPiste,-alku+askel,self.viimeSigYYksi)
                    self.viimeDataPiste = self.viimeSigYYksi
                except:
                    pass
                self.viimeSigYYksi = dataPiste

            #Datapisteiden siirto derivointia ja integrointia varten
            
            seurDataPiste = dataPiste
            

            ############## P-Kayran piirto #################

            try:
                PdataPiste = dataPiste*float(PKentta.text())
            except:
                PdataPiste = 0
            PjanaSiirretty = 0
            for Ppatka in PKayranPalat:                
                PxYksi = Ppatka.line().x1()
                PxKaksi = Ppatka.line().x2()
                PyYksi = Ppatka.line().y1()
                PyKaksi = Ppatka.line().y2()
                
                
                if PxKaksi < askel:
                    Ppatka.setLine(PxYksi+askel,PyYksi,PxKaksi+askel,PyKaksi)
                    
                else:                    
                    PjanaSiirretty +=1
                    
                    if PjanaSiirretty >= 2:
                        PpoistettavaIndeksi = PSignNaytos.items().index(Ppatka)
                        PSignNaytos.removeItem(PSignNaytos.items()[PpoistettavaIndeksi])
                    try:
                        Ppatka.setLine(-Palku,PdataPiste,-Palku+askel,self.PviimeSigYYksi)    
                    except:
                        Ppatka.setLine(-Palku,PdataPiste,-Palku+askel,0)
                    
                    PviimeSiirtoJana = Ppatka
                    self.PviimeSigYYksi = PviimeSiirtoJana.line().y1()
            if PjanaSiirretty == 0:
                try:
                    PSignNaytos.addLine(-Palku,PdataPiste,-Palku+askel,self.PviimeSigYYksi)
                except:
                    pass
                self.PviimeSigYYksi = PdataPiste

            ########### I-kayran piirto ####################
            
            try:
                self.summainKertyma += (self.viimeDataPiste-seurDataPiste)*askel/2*float(IKentta.text())
                IdataPiste = self.summainKertyma
            except:
                IdataPiste = 0

            IjanaSiirretty = 0
            for Ipatka in IKayranPalat:                
                IxYksi = Ipatka.line().x1()
                IxKaksi = Ipatka.line().x2()
                IyYksi = Ipatka.line().y1()
                IyKaksi = Ipatka.line().y2()
                
                
                if IxKaksi < askel:
                    Ipatka.setLine(IxYksi+askel,IyYksi,IxKaksi+askel,IyKaksi)
                    
                else:                    
                    IjanaSiirretty +=1
                    
                    if IjanaSiirretty >= 2:
                        IpoistettavaIndeksi = ISignNaytos.items().index(Ipatka)
                        ISignNaytos.removeItem(ISignNaytos.items()[IpoistettavaIndeksi])
                    try:
                        Ipatka.setLine(-Ialku,IdataPiste,-Ialku+askel,self.IviimeSigYYksi)    
                    except:
                        Ipatka.setLine(-Ialku,IdataPiste,-Ialku+askel,0)
                    
                    IviimeSiirtoJana = Ipatka
                    self.IviimeSigYYksi = IviimeSiirtoJana.line().y1()
            if IjanaSiirretty == 0:
                try:
                    ISignNaytos.addLine(-Ialku,IdataPiste,-Ialku+askel,self.IviimeSigYYksi)
                except:
                    pass
                self.IviimeSigYYksi = IdataPiste

            ############## D-kayran piirto ####################

            try:
                DdataPiste = (self.viimeDataPiste-seurDataPiste)/askel*float(DKentta.text())
            except:
                DdataPiste = 0
            #DdataPiste = dataPiste*float(DKentta.text())
            DjanaSiirretty = 0
            for Dpatka in DKayranPalat:                
                DxYksi = Dpatka.line().x1()
                DxKaksi = Dpatka.line().x2()
                DyYksi = Dpatka.line().y1()
                DyKaksi = Dpatka.line().y2()
                
                
                if DxKaksi < askel:
                    Dpatka.setLine(DxYksi+askel,DyYksi,DxKaksi+askel,DyKaksi)
                    
                else:                    
                    DjanaSiirretty +=1
                    
                    if DjanaSiirretty >= 2:
                        DpoistettavaIndeksi = DSignNaytos.items().index(Dpatka)
                        DSignNaytos.removeItem(DSignNaytos.items()[DpoistettavaIndeksi])
                    try:
                        Dpatka.setLine(-Dalku,DdataPiste,-Dalku+askel,self.DviimeSigYYksi)    
                    except:
                        Dpatka.setLine(-Dalku,DdataPiste,-Dalku+askel,0)
                    
                    DviimeSiirtoJana = Dpatka
                    self.DviimeSigYYksi = DviimeSiirtoJana.line().y1()
            if DjanaSiirretty == 0:
                try:
                    DSignNaytos.addLine(-Dalku,DdataPiste,-Dalku+askel,self.DviimeSigYYksi)
                except:
                    pass
                self.DviimeSigYYksi = DdataPiste
            
            ######## Summa(ulostulo)kayran piirto ################

            summaDataPiste = PdataPiste+IdataPiste+DdataPiste

            summaJanaSiirretty = 0
            for summaPatka in summaKayranPalat:                
                summaxYksi = summaPatka.line().x1()
                summaxKaksi = summaPatka.line().x2()
                summayYksi = summaPatka.line().y1()
                summayKaksi = summaPatka.line().y2()
                
                
                if summaxKaksi < askel:
                    summaPatka.setLine(summaxYksi+askel,summayYksi,summaxKaksi+askel,summayKaksi)
                    
                else:                    
                    summaJanaSiirretty +=1
                    
                    if summaJanaSiirretty >= 2:
                        summaPoistettavaIndeksi = UlosSignNaytos.items().index(summaPatka)
                        UlosSignNaytos.removeItem(UlosSignNaytos.items()[summaPoistettavaIndeksi])
                    try:
                        summaPatka.setLine(-summaAlku,summaDataPiste,-summaAlku+askel,self.summaViimeSigYYksi)    
                    except:
                        summaPatka.setLine(-summaAlku,summaDataPiste,-summaAlku+askel,0)
                    
                    summaViimeSiirtoJana = summaPatka
                    self.summaViimeSigYYksi = summaViimeSiirtoJana.line().y1()
            if summaJanaSiirretty == 0:
                try:
                    UlosSignNaytos.addLine(-summaAlku,summaDataPiste,-summaAlku+askel,self.summaViimeSigYYksi)
                except:
                    pass
                self.summaViimeSigYYksi = summaDataPiste            

    
            #Ledi kiinni kanavaan 12
            #Etuvastuksella 330R-470R
                
            #print(patka.line().x1())

        tick = QTimer(self)
        tick.start(200)

        #print(SisaanSignNaytos.items())
        
        #self.connect(tick,SIGNAL("timeout()"),uudelleenPiirto)
        self.connect(tick,SIGNAL("timeout()"),kayrienSiirto)

        
        

        #self.showMaximized()
        self.setLayout(hyllysto)

        """
        def uudelleenPiirto():
            SisaanSignNaytos.clear()
            print("dirr")
            sisaSignAlkuPiste = round(SisaSignNakyma.width()/2)
            sisaSignLeveys = int(round(SisaSignNakyma.width()/2))
            sigY = 20*m.sin((sisaSignLeveys-2)*0.1)
                
            while sisaSignLeveys > 2:
                sisaSignLeveys-=2
                
                sigYsec = 20*m.sin(sisaSignLeveys*0.1)
                SisaanSignNaytos.addLine(-sisaSignLeveys,sigY,-sisaSignLeveys+2,sigYsec,kaariKyna)
                sigY = 20*m.sin((sisaSignLeveys+2)*0.1)
            SisaanSignNaytos.advance()    
                
            

        
        """
    
        
app = QApplication(sys.argv)
#Cleanup on exit

form = Form()
#form.connect(app,SIGNAL("aboutToQuit()"),clearSound)
form.show()
app.exec_()

        
