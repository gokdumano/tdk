from helpers import Sozluk, Gore, Cins, Lehce
from helpers import TDK
        
with TDK() as tdk:
    anne     = tdk.Sozlukler( 'anne', Sozluk.GuncelTurkceSozlugu )
    otomobil = tdk.Sozlukler( 'otomobil', Sozluk.BatiKokenliKelimelerSozlugu )

    defne = tdk.KisiAdlariSozlugu( 'defne', Gore.AdaGore, Cins.Kiz )
    cesur = tdk.KisiAdlariSozlugu( 'cesur', Gore.AnlamaGore, Cins.Kiz )
