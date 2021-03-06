def nasprotnik(igralec):
     """Vrni nasprotnika od igralca."""
     if igralec == Igra.lisice:
         return Igra.zajci
     elif igralec == Igra.zajci:
         return Igra.lisice


class Igra():

    vstopno_zajec = 'VSTOPNO_ZAJEC'
    vstopno_lisica = 'VSTOPNO_LISICA'
    zmagovalno_zajec = 'ZMAGOVALNO_ZAJEC'
    zmagovalno_lisica = 'ZMAGOVALNO_LISICA'
    navadno = 'NAVADNO'
    zajci = 'ZAJCI'
    lisice = 'LISICE'
    lisica = 'LISICA'
    zajec = 'ZAJEC'
    polje = 'POLJE'
    cakajoci_zajec = 'CAKAJOCI_ZAJEC'
    cakajoca_lisica = 'CAKAJOCA_LISICA'


    povezave = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (11,12), (12,13), (13,14),
                (14,15), (15,16), (16,17), (17,18), (18,19), (0, 19), (20,21), (21,22), (22,23), (23,24), (24,25), (25,26),
                (26,27), (20,27), (0,20), (4,21), (6,22), (10,24), (14,25), (16,26)]

    def __init__(self):
        self.na_potezi = Igra.lisice #zajci ali lisice
        self.lisice = [] #polja, kjer se nahajajo lisice
        self.zajci = [] #polja, kjer se nahajajo zajci
        self.stevilo_lisic_v_igri = 5 #koliko lisic je se vi igri
        self.stevilo_zajcev_v_igri = 5 #koliko zajcev je se v igri
        self.igra_poteka = True
        self.zgodovina = []



    def tip_polja(self, k):
        #vrne tip polja, vstopno, navadno ali zmagovalno
        if k == 0 or k == 6:
            return Igra.vstopno_zajec
        if k == 10 or k == 16:
            return Igra.vstopno_lisica
        if k == 13:
            return Igra.zmagovalno_zajec
        if k == 3:
            return Igra.zmagovalno_lisica
        return Igra.navadno

    def shrani_pozicijo(self):
        #v seznam zgodovina shrani novo pozicijo, ki je oblike ((polja z lisicami, polja z zajci), kdo je na potezi)
        p = (self.lisice, self.zajci)
        self.zgodovina.append((p, self.na_potezi))

    def kopija(self):
        #vrne kopijo trenutne igre, ki je predstavljena s tem kdo je na potezi, polja z lisicami, polja z zajci
        kopija = Igra()
        kopija.lisice = self.lisice
        kopija.zajci = self.zajci
        kopija.na_potezi = self.na_potezi
        return kopija

    def razveljavi(self):
        ((self.lisice, self.zajci), self.na_potezi) = self.zgodovina.pop()

    def povleci_potezo(self, figura, polje):
        if not self.veljavna_poteza(figura, polje):
            return None
        else:
            self.shrani_pozicijo()
            self.spremeni_stanje(figura, polje)
            return (figura, polje)


    def spremeni_stanje(self, figura, polje):
        #updata seznama self.lisice in self.zajci (doda nova polja in odstrani stare)
        if self.igra_poteka:
            if figura[0] == Igra.zajec or figura[0] == Igra.cakajoci_zajec:
                self.zajci.append(polje)
                if figura[1] != None:
                    self.zajci.remove(figura[1])
                self.na_potezi = Igra.lisice
            if figura[0] == Igra.lisica or figura[0] == Igra.cakajoca_lisica:
                self.lisice.append(polje)
                if figura[1] != None:
                    print(figura, self.lisice, 'drugo je self.lisice')
                    self.lisice.remove(figura[1])
                self.na_potezi = Igra.zajci
            #obkoljenega vrze dol za zmerej, torej spremeni stevilo lisic oz zajcev v igri
            for i in self.ali_je_obkoljen(figura, polje):
                if i in self.zajci:
                    self.zajci.remove(i)
                    self.stevilo_zajcev_v_igri -= 1
                if i in self.lisice:
                    self.lisice.remove(i)
                    self.stevilo_lisic_v_igri -= 1

            if self.ali_je_zmaga(figura, polje) != None:
                self.igra_poteka = False




    def stanje_igre(self):
        #vrne zmagovalca ali pa None, če igre ni konec
        if 3 in self.lisice:
            return Igra.lisice
        if 13 in self.zajci:
            return Igra.zajci
        else:
            return None


    def veljavna_poteza(self, figura, polje):
        #če je polje zasedeno, vrne False
        if polje in self.lisice or polje in self.zajci:
            return False
        #polje ni zasedeno, preveri če je sosedno
        if figura[0] == Igra.zajec:
            if ((figura[1], polje) in Igra.povezave) or ((polje, figura[1]) in Igra.povezave):
                return True
        if figura[0] == Igra.cakajoci_zajec and self.tip_polja(polje) == Igra.vstopno_zajec:
            return True

        if figura[0] == Igra.lisica:
            if ((figura[1], polje) in Igra.povezave) or ((polje, figura[1]) in Igra.povezave):
                return True
        if figura[0] == Igra.cakajoca_lisica and self.tip_polja(polje) == Igra.vstopno_lisica:
            return True



    def ali_je_obkoljen(self, figura, polje):
        obkoljeni = []
        for povezava in Igra.povezave:
            if polje in povezava:
                (x, y) = povezava
                if x == polje:
                    sosed = y
                if y == polje:
                    sosed = x
                #PREVERJAMO ČE JE LISICA OBKOLILA ZAJCA
                if (figura[0] == Igra.lisica or figura[0] == Igra.cakajoca_lisica) and sosed in self.zajci:
                    je_kandidat = True
                    sosedi_nasprotnika = []
                    for naveza in Igra.povezave:
                        (a,b) = naveza
                        if sosed in naveza:
                            if sosed == a:
                                sosedi_nasprotnika.append(b)

                            else:
                                sosedi_nasprotnika.append(a)
                    for element in sosedi_nasprotnika:
                        if element not in self.lisice:
                            je_kandidat = False
                    if je_kandidat:
                        obkoljeni.append(sosed)
                #PREVERJAMO ČE JE ZAJEC OBKOLIL LISICO
                if (figura[0] == Igra.zajec or figura[0] == Igra.cakajoci_zajec) and sosed in self.lisice:
                    je_kandidat = True
                    sosedi_nasprotnika = []
                    for naveza in Igra.povezave:
                        (a,b) = naveza
                        if sosed in naveza:
                            if sosed == a:
                                sosedi_nasprotnika.append(b)
                            else:
                                sosedi_nasprotnika.append(a)
                    for element in sosedi_nasprotnika:
                        if element not in self.zajci:
                            je_kandidat = False
                    if je_kandidat:
                        obkoljeni.append(sosed)
        return obkoljeni

    def ali_je_zmaga(self, figura, polje):
        #vrne zmagovalca ali pa None, če ni zmagovalca, s tem da dobi za parameter premaknjeno figuro
        if figura[0] == Igra.lisica and self.tip_polja(polje) == Igra.zmagovalno_lisica:
            return Igra.lisice
        if figura[0] == Igra.zajec and self.tip_polja(polje) == Igra.zmagovalno_zajec:
            return Igra.zajci
        if self.stevilo_lisic_v_igri == 0:
            return Igra.zajci
        if self.stevilo_zajcev_v_igri == 0:
            return Igra.lisice

    def veljavne_poteze(self):
        #vrne slovar z dvema kljucema, mozne poteze za zajce in mozne poteze lisic. oblika: {mozne lisice: [((kdo, kje je zdaj), [mozna polja])]}
        mozne_poteze = {}
        mozne_poteze_lisic= []
        mozne_poteze_zajcev = []
        for i in self.lisice:
            mozne_poteze_lisic.append(((Igra.lisica, i), self.mozna_polja((Igra.lisica, i))))
        if len(self.lisice) < self.stevilo_lisic_v_igri:
            mozne_poteze_lisic.append(((Igra.cakajoca_lisica, None), self.mozna_polja((Igra.cakajoca_lisica, None))))

        for i in self.zajci:
            mozne_poteze_zajcev.append(((Igra.zajec, i), self.mozna_polja((Igra.zajec, i))))
        if len(self.zajci) < self.stevilo_zajcev_v_igri:
            mozne_poteze_zajcev.append(((Igra.cakajoci_zajec, None), self.mozna_polja((Igra.cakajoci_zajec, None))))

        mozne_poteze[Igra.lisice]= mozne_poteze_lisic
        mozne_poteze[Igra.zajci] = mozne_poteze_zajcev
        return mozne_poteze



    def mozna_polja(self, figura):
        #pogleda mozna polja, kam lahko gre figura. vrne seznam za pobarvat, ki ga uporabi tudi funkcija v Guiju, ki jih pobarva za uporabnika
        if figura != None:
            za_pobarvat = []
            if figura[0] == Igra.lisica or figura[0] == Igra.zajec:
                for povezava in Igra.povezave:
                    if figura[1] in povezava:
                        (x,y) = povezava
                        if x == figura[1]:
                            if (y not in self.zajci) or (y not in self.lisice):
                                za_pobarvat.append(y)
                        else:
                            if (y not in self.zajci) or (y not in self.lisice):
                                za_pobarvat.append(x)
            if figura[0] == self.cakajoca_lisica and 10 not in (self.lisice or self.zajci):
                za_pobarvat.append(10)
            if figura[0] == self.cakajoca_lisica and 16 not in (self.lisice or self.zajci):
                za_pobarvat.append(16)
            if figura[0] == self.cakajoci_zajec and 0 not in (self.lisice or self.zajci):
                za_pobarvat.append(0)
            if figura[0] == self.cakajoci_zajec and 6 not in (self.lisice or self.zajci):
                za_pobarvat.append(6)
            return za_pobarvat
