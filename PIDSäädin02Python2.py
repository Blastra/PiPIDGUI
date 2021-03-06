#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import math as m
import random
import smbus as sb
import RPi.GPIO as RPIO

class Form(QDialog):    

    

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("PID-saadin")        

        #Tekstikilvet
        OhjeArvoKilpi = QLabel("Ohjearvo")
        POhjKilpi = QLabel("Proportionaalikerroin")
        IOhjKilpi = QLabel("Integraalikerroin")
        IAikaOhjKilpi = QLabel("Integrointivali\naskelissa")
        DOhjKilpi = QLabel("Differentiaalikerroin")
        DAikaOhjKilpi = QLabel("Derivointivali\naskelissa")
        AskelOhjKilpi = QLabel("Askelpituus")
        NaytOttoTaajuusKilpi = QLabel("Naytteenottotaajuus")

        SigSisaanKilpi = QLabel("Signaali sisaan")
        SigUlosKilpi = QLabel("Signaali ulos")

        PKomponenttiKilpi = QLabel("P-komponentti")
        IKomponenttiKilpi = QLabel("I-komponentti")
        DKomponenttiKilpi = QLabel("D-komponentti")

        #Vaantonapit

        OhjeArvoOhjain = QDial()
        POhjain = QDial()
        IOhjain = QDial()
        IAikaOhjain = QDial()
        DOhjain = QDial()
        DAikaOhjain = QDial()
        NaytOttoTaajOhjain = QDial()

        #Syotekentat

        OhjeArvoKentta = QLineEdit("0")
        PKentta = QLineEdit("0")
        IKentta = QLineEdit("0")
        IAikaKentta = QLineEdit("1")
        DKentta = QLineEdit("0")
        DAikaKentta = QLineEdit("100")
        NaytOttoTaajKentta = QLineEdit("3")
        

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

        OhjeArvoLaatikko = QVBoxLayout()
        POhjLaatikko = QVBoxLayout()
        IOhjLaatikko = QVBoxLayout()
        IAikaOhjLaatikko = QVBoxLayout()
        DOhjLaatikko = QVBoxLayout()
        DAikaOhjLaatikko = QVBoxLayout()
        NaytOttoTaajuusLaatikko = QVBoxLayout()

        OhjeArvoDialJaLineBox = QHBoxLayout()
        PDialJaLineBox = QHBoxLayout()
        IDialJaLineBox = QHBoxLayout()
        IAikaDialJaLineBox = QHBoxLayout()
        DDialJaLineBox = QHBoxLayout()
        DAikaDialJaLineBox = QHBoxLayout()
        NaytOttoDialJaLineBox = QHBoxLayout()

        OhjainRivi.addLayout(OhjeArvoLaatikko)
        OhjainRivi.addLayout(POhjLaatikko)
        OhjainRivi.addLayout(IOhjLaatikko)
        OhjainRivi.addLayout(IAikaOhjLaatikko)
        OhjainRivi.addLayout(DOhjLaatikko)
        OhjainRivi.addLayout(DAikaOhjLaatikko)
        OhjainRivi.addLayout(NaytOttoTaajuusLaatikko)

        #Ensimmaisen rivin kilvet

        OhjeArvoLaatikko.addWidget(OhjeArvoKilpi)
        POhjLaatikko.addWidget(POhjKilpi)
        IOhjLaatikko.addWidget(IOhjKilpi)
        IAikaOhjLaatikko.addWidget(IAikaOhjKilpi)
        DOhjLaatikko.addWidget(DOhjKilpi)
        DAikaOhjLaatikko.addWidget(DAikaOhjKilpi)
        NaytOttoTaajuusLaatikko.addWidget(NaytOttoTaajuusKilpi)

        #Dialien ja LineEditien tilat kilpien alla

        OhjeArvoLaatikko.addLayout(OhjeArvoDialJaLineBox)
        POhjLaatikko.addLayout(PDialJaLineBox)
        IAikaOhjLaatikko.addLayout(IAikaDialJaLineBox)
        IOhjLaatikko.addLayout(IDialJaLineBox)
        DAikaOhjLaatikko.addLayout(DAikaDialJaLineBox)
        DOhjLaatikko.addLayout(DDialJaLineBox)
        NaytOttoTaajuusLaatikko.addLayout(NaytOttoDialJaLineBox)

        #Kaantonapit ja syotekentat

        OhjeArvoDialJaLineBox.addWidget(OhjeArvoOhjain)
        OhjeArvoDialJaLineBox.addWidget(OhjeArvoKentta)

        PDialJaLineBox.addWidget(POhjain)
        PDialJaLineBox.addWidget(PKentta)

        IDialJaLineBox.addWidget(IOhjain)
        IDialJaLineBox.addWidget(IKentta)

        
        IAikaDialJaLineBox.addWidget(IAikaOhjain)
        IAikaDialJaLineBox.addWidget(IAikaKentta)

        DDialJaLineBox.addWidget(DOhjain)
        DDialJaLineBox.addWidget(DKentta)

        
        DAikaDialJaLineBox.addWidget(DAikaOhjain)
        DAikaDialJaLineBox.addWidget(DAikaKentta)

        
        NaytOttoDialJaLineBox.addWidget(NaytOttoTaajOhjain)
        NaytOttoDialJaLineBox.addWidget(NaytOttoTaajKentta)

        def PaivitaOhjeArvoKentta():
            OhjeArvoKentta.setText(str(round(OhjeArvoOhjain.value()*80,2)))

        def PaivitaPKentta():
            PKentta.setText(str(round(POhjain.value()*0.2,2)))

        def PaivitaIKentta():
            IKentta.setText(str(round(IOhjain.value()*0.2,2)))

        def PaivitaIAikaKentta():
            IAikaKentta.setText(str(max(1,round(IAikaOhjain.value()))))

        def PaivitaDKentta():
            DKentta.setText(str(round(DOhjain.value()*0.2,2)))

        def PaivitaDAikaKentta():
            DAikaKentta.setText(str(max(1,round(DAikaOhjain.value()))))

        def PaivitaNaytOttoTaajKentta():
            NaytOttoTaajKentta.setText(str(round(NaytOttoTaajOhjain.value())))
            tick.stop()
            tick.start(1000/round(float(NaytOttoTaajKentta.text())))

        def PaivitaOhjeArvoOhjain():
            try:
                OhjeArvoOhjain.setValue(float(PKentta.text())/80)
            except:
                pass

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

        def PaivitaIAikaOhjain():
            try:
                IAikaOhjain.setValue(max(1,float(IAikaKentta.text())))
            except:
                pass

        def PaivitaDOhjain():
            try:
                DOhjain.setValue(float(DKentta.text())*5)
            except:
                pass

        def PaivitaDAikaOhjain():
            try:
                DAikaOhjain.setValue(max(1,float(DAikaKentta.text())))
            except:
                pass

        def PaivitaNaytOttoTaajOhjain():
            try:
                NaytOttoTaajOhjain.setValue(float(NaytOttoTaajKentta.text()))
                tick.stop()
                tick.start(1000/round(float(NaytOttoTaajKentta.text())))
            except:
                pass

        self.connect(OhjeArvoOhjain,SIGNAL("sliderReleased()"), PaivitaOhjeArvoKentta)
        self.connect(POhjain,SIGNAL("sliderReleased()"), PaivitaPKentta)
        self.connect(IOhjain,SIGNAL("sliderReleased()"), PaivitaIKentta)
        self.connect(IAikaOhjain,SIGNAL("sliderReleased()"), PaivitaIAikaKentta)
        self.connect(DOhjain,SIGNAL("sliderReleased()"), PaivitaDKentta)
        self.connect(DAikaOhjain,SIGNAL("sliderReleased()"), PaivitaDAikaKentta)
        self.connect(NaytOttoTaajOhjain,SIGNAL("sliderReleased()"), PaivitaNaytOttoTaajKentta)

        self.connect(OhjeArvoKentta,SIGNAL("editingFinished()"), PaivitaOhjeArvoOhjain)
        self.connect(PKentta,SIGNAL("editingFinished()"), PaivitaPOhjain)
        self.connect(IKentta,SIGNAL("editingFinished()"), PaivitaIOhjain)
        self.connect(IAikaKentta,SIGNAL("editingFinished()"), PaivitaIAikaOhjain)
        self.connect(DKentta,SIGNAL("editingFinished()"), PaivitaDOhjain)
        self.connect(DAikaKentta,SIGNAL("editingFinished()"), PaivitaDAikaOhjain)
        self.connect(NaytOttoTaajKentta,SIGNAL("editingFinished()"), PaivitaNaytOttoTaajOhjain)

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

        #Datavaylien maarittely
        #Huom. anturina GY-30 BH1750FVI
        #Anturin kytkennat Raspberryyn:
        #VCC: Pin 2
        #SDA: Pin 3
        #SCL: Pin 5
        #GND: Pin 6
        
        bus = sb.SMBus(1)

        #Kanavan 7 LEDin Inputin alustus
        #Etuvastuksella 330R-470R

        RPIO.setmode(RPIO.BOARD)
        RPIO.setup(7, RPIO.OUT)
        self.inputVayla = RPIO.PWM(7, 50)   #Kanava 7, taajuus 50Hz
        self.inputVayla.start(0)
        
        self.otetutIAskeleet = 0
        
        self.otetutDAskeleet = 0
        

        
        def kayrienSiirto():

            askel = 4
            #Datan lukeminen anturilta            

            dataSisaan = bus.read_i2c_block_data(0x23,0x11)
    
            #print((dataSisaan[1]+(256*dataSisaan[0]))/1.2)
            
            dataPiste = (dataSisaan[1]+(256*dataSisaan[0]))/1.2
            print("inputData:" +str(dataPiste))
            
            #dataPiste = random.randint(-10,10)

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

            ohjeArvo = 500 #float(OhjeArvoKilpi.text())
            try:
                PdataPiste = (dataPiste-ohjeArvo)*float(PKentta.text())
                print "PdataPiste: "+str(PdataPiste)
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

            self.otetutIAskeleet += 1
            saadettyIVali = int(float(IAikaKentta.text()))            

            uusiIDataPiste = seurDataPiste-ohjeArvo

              
            try:
                self.summainKertyma= float(IKentta.text())*(0.9*self.summainKertyma+0.1*uusiIDataPiste)  #min(-100,self.summainKertyma+uusiIDataPiste)
                #self.summainKertyma= max(100,self.summainKertyma)
                """
                tapausYksi = False
                #Eri integrointitapaukset
                
                #Molemmat arvot positiivisia
                if self.viimeDataPiste >= 0 and uusiIDataPiste >= 0:
                    tapausYksi = True
                    suurempi = max(self.viimeDataPiste,uusiIDataPiste)
                    pienempi = min(self.viimeDataPiste,uusiIDataPiste)
                    #Lisätään kolmio ja laatikko
                    self.summainKertyma += (((suurempi-pienempi)*askel/2*+askel*pienempi)*float(IKentta.text()))
                    #print "Tapaus 1 "+str((((suurempi-pienempi)*askel/2*+askel*pienempi)*float(IKentta.text())))
                elif self.viimeDataPiste < 0 and uusiIDataPiste > 0:
                    #Edellinen arvo negatiivinen, jälkimmäinen positiivinen
                    c = uusiIDataPiste
                    d = self.viimeDataPiste
                    self.summainKertyma += ((c**2/(c-d)*askel/2 - d**2/(c-d)*askel/2 )*float(IKentta.text()))
                    #print "Tapaus 2 "+str(((c**2/(c-d)*askel/2 - d**2/(c-d)*askel/2 )*float(IKentta.text())))
                elif self.viimeDataPiste > 0 and uusiIDataPiste < 0:
                    #Edellinen arvo positiivinen, jälkimmäinen negatiivinen
                    c = uusiIDataPiste
                    d = self.viimeDataPiste
                    self.summainKertyma += ((d**2/(d-c)*askel/2 - c**2/(d-c)*askel/2)*float(IKentta.text()))
                    #print "Tapaus 3 "+str(((d**2/(d-c)*askel/2 - c**2/(d-c)*askel/2)*float(IKentta.text())))
                elif self.viimeDataPiste <= 0 and uusiIDataPiste <= 0 and tapausYksi == False:
                    #Molemmat arvot negatiivisia                     
                    suurempi = max(self.viimeDataPiste,uusiIDataPiste)
                    pienempi = min(self.viimeDataPiste,uusiIDataPiste)
                    #Lisätään kolmio ja laatikko
                    self.summainKertyma -= (((pienempi-suurempi)*askel/2*+askel*suurempi)*float(IKentta.text()))
                    #print "Tapaus 4 "+str((((pienempi-suurempi)*askel/2*+askel*suurempi)*float(IKentta.text())))
                    #print "Kolmio "+str((pienempi-suurempi)*askel/2)
                    #print "Suorakulmio "+str(askel*suurempi)
                else:
                    self.summainKertyma += 0
                #self.summainKertyma = m.log10(abs(self.summainKertyma))*self.summainKertyma
                """
            except:
                IdataPiste = 0
            
            #Kertymän dataan sijoitus tai odotuttaminen
            if self.otetutIAskeleet >= saadettyIVali:
                #print("integrointivali saavutettu")
                self.otetutIAskeleet = 0
                ### Kertymään lisääminen
                IdataPiste = self.summainKertyma*float(IKentta.text())
            else:
                IdataPiste = self.IviimeSigYYksi

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

            saadettyDVali = int(float(DAikaKentta.text()))
            self.otetutDAskeleet += 1 

            if self.otetutDAskeleet >= saadettyDVali:
                #print("derivointivali saavutettu")
                self.otetutDAskeleet = 0
                try:
                    DdataPiste = ((self.viimeDataPiste-ohjeArvo)-(seurDataPiste-ohjeArvo))/askel*float(DKentta.text())
                except:
                    DdataPiste = 0
            else:
                try:
                    DdataPiste = self.DviimeSigYYksi
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

            if PdataPiste < 0:
                PdataPisteMerkki = -1
            if PdataPiste > 0:
                PdataPisteMerkki = 1
            if PdataPiste == 0:
                PdataPisteMerkki = 0

            if IdataPiste < 0:
                IdataPisteMerkki = -1
            if IdataPiste > 0:
                IdataPisteMerkki = 1
            if IdataPiste == 0:
                IdataPisteMerkki = 0

            if DdataPiste < 0:
                DdataPisteMerkki = -1
            if DdataPiste > 0:
                DdataPisteMerkki = 1
            if DdataPiste == 0:
                DdataPisteMerkki = 0

            #summaLaskuri = 100-(m.log(abs(PdataPiste)+1)*PdataPisteMerkki+m.log(abs(IdataPiste)+1)*IdataPisteMerkki+m.log(abs(DdataPiste)+1)*DdataPisteMerkki)
            summaLaskuri = max(0,-(PdataPiste+IdataPiste+DdataPiste))
            summaLaskuri = min(100,summaLaskuri)
            #print "komponenttien summa: "+str(m.log(abs(PdataPiste)+1)*PdataPisteMerkki+m.log(abs(IdataPiste)+1)*IdataPisteMerkki+m.log(abs(DdataPiste)+1)*DdataPisteMerkki)
            
            #ohjPiste = max(1,ohjPiste)
            summaDataPiste = summaLaskuri
            print "ohjausarvo: "+str(summaDataPiste)
            
            #### Summan vaikutus LEDin syöttöön ####

            #print "ohjausPiste: "+str(summaDataPiste)
            self.inputVayla.ChangeDutyCycle(10)
            
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

    
                 
        tick = QTimer(self)
        tick.start(200)  
        
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

def poistuminen():
    print("Cleaning up GPIO")
    form.inputVayla.stop()
    RPIO.cleanup()
    

form = Form()
form.connect(app,SIGNAL("aboutToQuit()"),poistuminen)
form.show()
app.exec_()

        
