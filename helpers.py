from posixpath import join as urljoin
from datetime import datetime as dt
from urllib.parse import unquote
from enum import Enum

import requests

Sozluk = Enum(
    'Sozluk',    
    [('GuncelTurkceSozlugu'              , 'gts'     ),
     ('BatiKokenliKelimelerSozlugu'      , 'bati'    ),
     ('TaramaSozlugu'                    , 'tarama'  ),
     ('DerlemeSozlugu'                   , 'derleme' ),
     ('AtasozuVeDeyimlerSozlugu'         , 'atasozu' ),
     ('YabanciSozlereKarsiliklarKilavuzu', 'kilavuz' ),
     ('EtimolojiSozlugu'                 , 'etms'    )]
    )
Gore  = Enum( 'Gore', 'AdaGore AnlamaGore')
Cins  = Enum( 'Cins', 'Kiz Erkek ErkekVeKiz')
Lehce = Enum(
    'Cins',
    ['TurkiyeTurkcesi'   ,
     'KazakTurkcesi'     ,
     'OzbekTurkcesi'     ,
     'AzerbaycanTurkcesi',
     'UygurTurkcesi'     ,
     'BaskurtTurkcesi'   ,
     'TurkmenTurkcesi'   ,
     'TatarTurkcesi'     ,
     'KirgizTurkcesi'    ,
     'Rusça'             ]
    )

class TDK:
    base = 'https://sozluk.gov.tr'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://sozluk.gov.tr/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
    def __init__( self ):
        self.client = requests.Session()

    def __enter__( self ):
        print( f'[ {dt.now()} ] - Initializing Client Session...' )
        self.__init_session__()
        return self

    def __exit__( self, *args ):
        print( f'[ {dt.now()} ] - Closing Session...' )
        self.close()

    def __init_session__( self ):
        self.fetch( as_json=False )

    def Sozlukler( self, ara:str, sozluk:Sozluk=Sozluk.GuncelTurkceSozlugu ):
        return self.fetch( sozluk.value, { 'ara': ara } )
    
    def KisiAdlariSozlugu( self, ara:str, gore:Gore=Gore.AdaGore, cins:Cins=Cins.ErkekVeKiz ):
        return self.fetch( 'adlar', { 'ara': ara, 'gore': gore.value, 'cins': cins.value } )

    def KarsilastirmaliTurkceLehceleriSozlugu( self, ara:str, lehce:Lehce=Lehce.AzerbaycanTurkcesi ):
        return self.fetch( 'lehceler', { 'ara': ara, 'lehce': lehce.value } )

    def BilimVeSanatTerimleriSozlugu( self, ara ):
        tumu = self.fetch( 'terim', { 'ara': ara, 'eser_ad': 'tümü' } )
        tumu.extend( self.fetch( 'hemsirelik', { 'ara': ara } ) )
        tumu.extend( self.fetch( 'eczacilik' , { 'ara': ara } ) )
        tumu.extend( self.fetch( 'metroloji' , { 'ara': ara } ) )
        return tumu
                                                                                             
    def fetch( self, endpoint:str='', params=None, headers=None, as_json=True ):
        url    = urljoin( TDK.base, endpoint)
        
        if headers is None: headers = TDK.headers
        if endpoint == Sozluk.YabanciSozlereKarsiliklarKilavuzu:
            params |= { 'prm': 'ysk' }
        
        with self.client.get( url, params=params, headers=headers ) as resp:
            resp.raise_for_status()
            print( f'[ {dt.now()} ] - {unquote(resp.url)}' )
            if as_json:
                resp = resp.json()
                if isinstance( resp, dict ) and 'error' in resp:
                    return []
            return resp
        
    def close( self ):        
        self.client.close()
