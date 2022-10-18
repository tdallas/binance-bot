import json
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.neighbors import KNeighborsClassifier
from tqdm import tqdm
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import plotly.express as px
import requests
import random

PAIRS = ['BNBUSDT', 'BCCUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'TUSDBNB', 'EOSUSDT', 'TUSDUSDT',
         'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'VENUSDT', 'NULSUSDT', 'VETUSDT', 'PAXUSDT',
         'USDCBNB', 'BCHABCUSDT', 'BCHSVUSDT', 'BNBTUSD', 'XRPTUSD', 'EOSTUSD', 'XLMTUSD', 'BNBUSDC', 'XRPUSDC',
         'EOSUSDC', 'XLMUSDC', 'USDCUSDT', 'ADATUSD', 'TRXTUSD', 'NEOTUSD', 'PAXTUSD', 'USDCTUSD', 'USDCPAX',
         'LINKUSDT', 'LINKTUSD', 'LINKUSDC', 'WAVESUSDT', 'WAVESTUSD', 'WAVESUSDC', 'BCHABCTUSD', 'BCHABCUSDC',
         'BCHSVTUSD', 'BCHSVUSDC', 'LTCTUSD', 'LTCUSDC', 'TRXUSDC', 'BTTUSDT', 'BNBUSDS', 'USDSUSDT', 'USDSPAX',
         'USDSTUSD', 'USDSUSDC', 'BTTTUSD', 'BTTUSDC', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT',
         'XMRUSDT', 'ZECUSDT', 'ZECTUSD', 'ZECUSDC', 'IOSTUSDT', 'CELRUSDT', 'ADAUSDC', 'NEOUSDC', 'DASHUSDT',
         'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICUSDT', 'ATOMUSDT', 'ATOMUSDC', 'ATOMTUSD',
         'ETCUSDC', 'ETCTUSD', 'BATUSDC', 'BATTUSD', 'PHBUSDC', 'PHBTUSD', 'TFUELUSDT', 'TFUELUSDC', 'TFUELTUSD',
         'ONEUSDT', 'ONETUSD', 'ONEUSDC', 'FTMUSDT', 'FTMTUSD', 'FTMUSDC', 'BCPTTUSD', 'BCPTUSDC', 'ALGOUSDT',
         'ALGOTUSD', 'ALGOUSDC', 'USDSBUSDT', 'USDSBUSDS', 'GTOUSDT', 'GTOTUSD', 'GTOUSDC', 'ERDUSDT', 'ERDUSDC',
         'DOGEUSDT', 'DOGEUSDC', 'DUSKUSDT', 'DUSKUSDC', 'BGBPUSDC', 'ANKRUSDT', 'ANKRTUSD', 'ANKRUSDC', 'ONTUSDC',
         'WINUSDT', 'WINUSDC', 'COSUSDT', 'TUSDBTUSD', 'NPXSUSDT', 'NPXSUSDC', 'COCOSUSDT', 'MTLUSDT', 'TOMOUSDT',
         'TOMOUSDC', 'PERLUSDC', 'PERLUSDT', 'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT',
         'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'BNBBUSD', 'BUSDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT',
         'RVNUSDT', 'HCUSDT', 'HBARUSDT', 'NKNUSDT', 'XRPBUSD', 'BCHABCBUSD', 'LTCBUSD', 'LINKBUSD', 'ETCBUSD',
         'STXUSDT', 'KAVAUSDT', 'BUSDNGN', 'ARPAUSDT', 'TRXBUSD', 'EOSBUSD', 'IOTXUSDT', 'RLCUSDT', 'MCOUSDT',
         'XLMBUSD', 'ADABUSD', 'CTXCUSDT', 'BCHUSDT', 'BCHUSDC', 'BCHTUSD', 'BCHBUSD', 'TROYUSDT', 'BUSDRUB',
         'QTUMBUSD', 'VETBUSD', 'VITEUSDT', 'FTTUSDT', 'BUSDTRY', 'USDTTRY', 'USDTRUB', 'EURBUSD', 'EURUSDT', 'OGNUSDT',
         'DREPUSDT', 'BULLUSDT', 'BULLBUSD', 'BEARUSDT', 'BEARBUSD', 'TCTUSDT', 'WRXUSDT', 'ICXBUSD', 'BTSUSDT',
         'BTSBUSD', 'LSKUSDT', 'BNTUSDT', 'BNTBUSD', 'LTOUSDT', 'ATOMBUSD', 'DASHBUSD', 'NEOBUSD', 'WAVESBUSD',
         'XTZBUSD', 'EOSBULLUSDT', 'EOSBULLBUSD', 'EOSBEARUSDT', 'EOSBEARBUSD', 'XRPBULLUSDT', 'XRPBULLBUSD',
         'XRPBEARUSDT', 'XRPBEARBUSD', 'BATBUSD', 'ENJBUSD', 'NANOBUSD', 'ONTBUSD', 'RVNBUSD', 'STRATBUSD', 'STRATUSDT',
         'AIONBUSD', 'AIONUSDT', 'MBLUSDT', 'COTIUSDT', 'ALGOBUSD', 'BTTBUSD', 'TOMOBUSD', 'XMRBUSD', 'ZECBUSD',
         'BNBBULLUSDT', 'BNBBULLBUSD', 'BNBBEARUSDT', 'BNBBEARBUSD', 'STPTUSDT', 'USDTZAR', 'BUSDZAR', 'WTCUSDT',
         'DATABUSD', 'DATAUSDT', 'XZCUSDT', 'SOLUSDT', 'SOLBUSD', 'USDTIDRT', 'BUSDIDRT', 'CTSIUSDT', 'CTSIBUSD',
         'HIVEUSDT', 'CHRUSDT', 'GXSUSDT', 'ARDRUSDT', 'ERDBUSD', 'LENDUSDT', 'HBARBUSD', 'MATICBUSD', 'WRXBUSD',
         'ZILBUSD', 'MDTUSDT', 'STMXUSDT', 'KNCBUSD', 'KNCUSDT', 'REPBUSD', 'REPUSDT', 'LRCBUSD', 'LRCUSDT', 'IQBUSD',
         'PNTUSDT', 'GBPBUSD', 'DGBBUSD', 'USDTUAH', 'COMPBUSD', 'COMPUSDT', 'BUSDBIDR', 'USDTBIDR', 'BKRWUSDT',
         'BKRWBUSD', 'SCUSDT', 'ZENUSDT', 'SXPBUSD', 'SNXBUSD', 'SNXUSDT', 'ADAUPUSDT', 'ADADOWNUSDT', 'LINKUPUSDT',
         'LINKDOWNUSDT', 'VTHOBUSD', 'VTHOUSDT', 'DCRBUSD', 'DGBUSDT', 'GBPUSDT', 'STORJBUSD', 'SXPUSDT', 'IRISBUSD',
         'MKRUSDT', 'MKRBUSD', 'DAIUSDT', 'DAIBUSD', 'RUNEBUSD', 'MANABUSD', 'DOGEBUSD', 'LENDBUSD', 'ZRXBUSD',
         'DCRUSDT', 'STORJUSDT', 'AUDBUSD', 'FIOBUSD', 'BNBUPUSDT', 'BNBDOWNUSDT', 'XTZUPUSDT', 'XTZDOWNUSDT',
         'AVABUSD', 'USDTBKRW', 'BUSDBKRW', 'IOTABUSD', 'MANAUSDT', 'AUDUSDT', 'BALBUSD', 'YFIBUSD', 'YFIUSDT',
         'BLZBUSD', 'KMDBUSD', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'USDTDAI', 'BUSDDAI', 'JSTBUSD', 'JSTUSDT',
         'SRMBUSD', 'SRMUSDT', 'ANTBUSD', 'ANTUSDT', 'CRVBUSD', 'CRVUSDT', 'SANDUSDT', 'SANDBUSD', 'OCEANBUSD',
         'OCEANUSDT', 'NMRBUSD', 'NMRUSDT', 'DOTBUSD', 'DOTUSDT', 'LUNABUSD', 'LUNAUSDT', 'IDEXBUSD', 'RSRBUSD',
         'RSRUSDT', 'PAXGBUSD', 'PAXGUSDT', 'WNXMBUSD', 'WNXMUSDT', 'TRBBUSD', 'TRBUSDT', 'BZRXBUSD', 'BZRXUSDT',
         'SUSHIBUSD', 'SUSHIUSDT', 'YFIIBUSD', 'YFIIUSDT', 'KSMBUSD', 'KSMUSDT', 'EGLDBUSD', 'EGLDUSDT', 'DIABUSD',
         'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT', 'EOSUPUSDT', 'EOSDOWNUSDT', 'TRXUPUSDT', 'TRXDOWNUSDT',
         'XRPUPUSDT', 'XRPDOWNUSDT', 'DOTUPUSDT', 'DOTDOWNUSDT', 'USDTNGN', 'BELBUSD', 'BELUSDT', 'SWRVBUSD',
         'WINGBUSD', 'WINGUSDT', 'LTCUPUSDT', 'LTCDOWNUSDT', 'CREAMBUSD', 'UNIBUSD', 'UNIUSDT', 'NBSUSDT', 'OXTUSDT',
         'SUNUSDT', 'AVAXBUSD', 'AVAXUSDT', 'HNTUSDT', 'FLMBUSD', 'FLMUSDT', 'CAKEBUSD', 'UNIUPUSDT', 'UNIDOWNUSDT',
         'ORNUSDT', 'UTKUSDT', 'XVSBUSD', 'XVSUSDT', 'ALPHABUSD', 'ALPHAUSDT', 'VIDTBUSD', 'USDTBRL', 'AAVEBUSD',
         'AAVEUSDT', 'NEARBUSD', 'NEARUSDT', 'SXPUPUSDT', 'SXPDOWNUSDT', 'FILBUSD', 'FILUSDT', 'FILUPUSDT',
         'FILDOWNUSDT', 'YFIUPUSDT', 'YFIDOWNUSDT', 'INJBUSD', 'INJUSDT', 'AERGOBUSD', 'ONEBUSD', 'AUDIOBUSD',
         'AUDIOUSDT', 'CTKBUSD', 'CTKUSDT', 'BCHUPUSDT', 'BCHDOWNUSDT', 'BOTBUSD', 'AKROUSDT', 'KP3RBUSD', 'AXSBUSD',
         'AXSUSDT', 'HARDBUSD', 'HARDUSDT', 'DNTBUSD', 'DNTUSDT', 'CVPBUSD', 'STRAXBUSD', 'STRAXUSDT', 'FORBUSD',
         'UNFIBUSD', 'UNFIUSDT', 'FRONTBUSD', 'BCHABUSD', 'ROSEBUSD', 'ROSEUSDT', 'BUSDBRL', 'AVAUSDT', 'SYSBUSD',
         'XEMUSDT', 'HEGICBUSD', 'AAVEUPUSDT', 'AAVEDOWNUSDT', 'PROMBUSD', 'SKLBUSD', 'SKLUSDT', 'SUSDUSDT',
         'COVERBUSD', 'GHSTBUSD', 'SUSHIUPUSDT', 'SUSHIDOWNUSDT', 'XLMUPUSDT', 'XLMDOWNUSDT', 'DFBUSD', 'GRTUSDT',
         'JUVBUSD', 'JUVUSDT', 'PSGBUSD', 'PSGUSDT', 'BUSDBVND', 'USDTBVND', '1INCHUSDT', 'REEFUSDT', 'OGUSDT',
         'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'TRUBUSD', 'TRUUSDT', 'DEXEBUSD', 'USDCBUSD', 'TUSDBUSD',
         'PAXBUSD', 'CKBBUSD', 'CKBUSDT', 'TWTBUSD', 'TWTUSDT', 'FIROUSDT', 'LITBUSD', 'LITUSDT', 'BUSDVAI', 'SFPBUSD',
         'SFPUSDT', 'FXSBUSD', 'DODOBUSD', 'DODOUSDT', 'CAKEUSDT', 'BAKEBUSD', 'UFTBUSD', '1INCHBUSD', 'BANDBUSD',
         'GRTBUSD', 'IOSTBUSD', 'OMGBUSD', 'REEFBUSD', 'ACMBUSD', 'ACMUSDT', 'AUCTIONBUSD', 'PHABUSD', 'TVKBUSD',
         'BADGERBUSD', 'BADGERUSDT', 'FISBUSD', 'FISUSDT', 'OMBUSD', 'OMUSDT', 'PONDBUSD', 'PONDUSDT', 'DEGOBUSD',
         'DEGOUSDT', 'ALICEBUSD', 'ALICEUSDT', 'CHZBUSD', 'BIFIBUSD', 'LINABUSD', 'LINAUSDT', 'PERPBUSD', 'PERPUSDT',
         'RAMPBUSD', 'RAMPUSDT', 'SUPERBUSD', 'SUPERUSDT', 'CFXBUSD', 'CFXUSDT', 'XVGBUSD', 'EPSBUSD', 'EPSUSDT',
         'AUTOBUSD', 'AUTOUSDT', 'TKOBUSD', 'TKOUSDT', 'PUNDIXUSDT', 'TLMBUSD', 'TLMUSDT', '1INCHUPUSDT',
         '1INCHDOWNUSDT', 'BTGBUSD', 'BTGUSDT', 'HOTBUSD', 'MIRBUSD', 'MIRUSDT', 'BARBUSD', 'BARUSDT', 'FORTHBUSD',
         'FORTHUSDT', 'BAKEUSDT', 'BURGERBUSD', 'BURGERUSDT', 'SLPBUSD', 'SLPUSDT', 'SHIBUSDT', 'SHIBBUSD', 'ICPBUSD',
         'ICPUSDT', 'ARBUSD', 'ARUSDT', 'POLSBUSD', 'POLSUSDT', 'MDXBUSD', 'MDXUSDT', 'MASKBUSD', 'MASKUSDT', 'LPTBUSD',
         'LPTUSDT', 'NUBUSD', 'NUUSDT', 'XVGUSDT', 'RLCBUSD', 'CELRBUSD', 'ATMBUSD', 'ZENBUSD', 'FTMBUSD', 'THETABUSD',
         'WINBUSD', 'KAVABUSD', 'XEMBUSD', 'ATABUSD', 'ATAUSDT', 'GTCBUSD', 'GTCUSDT', 'TORNBUSD', 'TORNUSDT',
         'COTIBUSD', 'KEEPBUSD', 'KEEPUSDT', 'SCBUSD', 'CHRBUSD', 'STMXBUSD', 'HNTBUSD', 'FTTBUSD', 'DOCKBUSD',
         'ERNBUSD', 'ERNUSDT', 'KLAYBUSD', 'KLAYUSDT', 'UTKBUSD', 'IOTXBUSD', 'PHAUSDT', 'BUSDUAH', 'BONDBUSD',
         'BONDUSDT', 'MLNBUSD', 'MLNUSDT', 'DEXEUSDT', 'LTOBUSD', 'ADXBUSD', 'QUICKBUSD', 'C98USDT', 'C98BUSD',
         'CLVBUSD', 'CLVUSDT', 'QNTBUSD', 'QNTUSDT', 'FLOWBUSD', 'FLOWUSDT', 'XECBUSD', 'TVKUSDT', 'MINABUSD',
         'MINAUSDT', 'RAYBUSD', 'RAYUSDT', 'FARMBUSD', 'FARMUSDT', 'ALPACABUSD', 'ALPACAUSDT', 'QUICKUSDT', 'ORNBUSD',
         'MBOXBUSD', 'MBOXUSDT', 'FORUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'WAXPBUSD', 'TRIBEBUSD', 'TRIBEUSDT',
         'GNOUSDT', 'GNOBUSD', 'MTLBUSD', 'OGNBUSD', 'XECUSDT', 'POLYBUSD', 'ELFUSDT', 'DYDXUSDT', 'DYDXBUSD',
         'ELFBUSD', 'POLYUSDT', 'IDEXUSDT', 'VIDTUSDT', 'BNBUSDP', 'USDPBUSD', 'USDPUSDT', 'GALAUSDT', 'GALABUSD',
         'SUNBUSD', 'ILVUSDT', 'ILVBUSD', 'RENBUSD', 'YGGUSDT', 'YGGBUSD', 'STXBUSD', 'SYSUSDT', 'DFUSDT', 'SOLUSDC',
         'FETBUSD', 'ARPABUSD', 'LSKBUSD', 'FIDAUSDT', 'FIDABUSD', 'DENTBUSD', 'FRONTUSDT', 'CVPUSDT', 'AGLDBUSD',
         'AGLDUSDT', 'RADBUSD', 'RADUSDT', 'HIVEBUSD', 'STPTBUSD', 'BETABUSD', 'BETAUSDT', 'RAREBUSD', 'RAREUSDT',
         'TROYBUSD', 'LAZIOUSDT', 'CHESSBUSD', 'CHESSUSDT', 'SCRTBUSD', 'ADXUSDT', 'AUCTIONUSDT', 'CELOBUSD', 'DARUSDT',
         'DARBUSD', 'BNXBUSD', 'BNXUSDT', 'RGTUSDT', 'RGTBUSD', 'LAZIOBUSD', 'OXTBUSD', 'AUDUSDC', 'MOVRBUSD',
         'MOVRUSDT', 'CITYBUSD', 'CITYUSDT', 'ENSBUSD', 'ENSUSDT', 'ANKRBUSD', 'KP3RUSDT', 'QIUSDT', 'QIBUSD',
         'PORTOUSDT', 'POWRUSDT', 'POWRBUSD', 'VGXUSDT', 'JASMYUSDT', 'JASMYBUSD', 'AMPBUSD', 'AMPUSDT', 'PLABUSD',
         'PLAUSDT', 'PYRBUSD', 'PYRUSDT', 'RNDRUSDT', 'RNDRBUSD', 'ALCXBUSD', 'ALCXUSDT', 'SANTOSUSDT', 'MCBUSD',
         'MCUSDT', 'COCOSBUSD', 'ANYBUSD', 'ANYUSDT', 'BICOBUSD', 'BICOUSDT', 'FLUXBUSD', 'FLUXUSDT', 'FXSUSDT',
         'REQBUSD', 'VOXELBUSD', 'VOXELUSDT', 'COSBUSD', 'CTXCBUSD', 'HIGHBUSD', 'HIGHUSDT', 'CVXBUSD', 'CVXUSDT',
         'PEOPLEBUSD', 'PEOPLEUSDT', 'OOKIBUSD', 'OOKIUSDT', 'MDTBUSD', 'NULSBUSD', 'SPELLUSDT', 'SPELLBUSD', 'USTBUSD',
         'USTUSDT', 'JOEBUSD', 'JOEUSDT', 'DUSKBUSD', 'ACHBUSD', 'ACHUSDT', 'IMXBUSD', 'IMXUSDT', 'GLMRBUSD',
         'GLMRUSDT', 'UMABUSD', 'LOKABUSD', 'LOKAUSDT', 'SCRTUSDT', 'API3BUSD', 'API3USDT', 'BTTCUSDT', 'BTTCUSDC',
         'ACABUSD', 'ACAUSDT', 'ANCBUSD', 'ANCUSDT', 'XNOBUSD', 'XNOUSDT', 'WOOBUSD', 'WOOUSDT', 'TFUELBUSD',
         'ALPINEUSDT', 'TUSDT', 'TBUSD', 'ASTRBUSD', 'ASTRUSDT', 'GMTBUSD', 'GMTUSDT', 'KDABUSD', 'KDAUSDT', 'APEUSDT',
         'APEBUSD', 'ALPINEBUSD', 'BSWUSDT', 'BSWBUSD', 'SANTOSBUSD', 'BIFIUSDT', 'MULTIBUSD', 'MULTIUSDT', 'PORTOBUSD',
         'STEEMUSDT', 'BTTCBUSD', 'MBLBUSD', 'MOBUSDT', 'MOBBUSD', 'NEXOUSDT', 'NEXOBUSD', 'REIUSDT', 'GALUSDT',
         'GALBUSD', 'LDOBUSD', 'LDOUSDT', 'EPXUSDT', 'EPXBUSD', 'STEEMBUSD', 'CVCBUSD', 'REIBUSD', 'DREPBUSD',
         'AKROBUSD', 'PUNDIXBUSD', 'LUNCBUSD', 'USTCBUSD', 'OPBUSD', 'OPUSDT', 'OGBUSD', 'KEYBUSD', 'ASRBUSD',
         'FIROBUSD', 'NKNBUSD', 'GTOBUSD', 'LEVERUSDT', 'LEVERBUSD', 'GLMBUSD', 'SSVBUSD', 'STGBUSD', 'STGUSDT',
         'ARKBUSD', 'LOOMBUSD', 'SNMBUSD', 'AMBBUSD', 'LUNCUSDT', 'PHBBUSD', 'GASBUSD', 'NEBLBUSD', 'PROSBUSD',
         'VIBBUSD', 'GMXBUSD', 'GMXUSDT', 'AGIXBUSD', 'NEBLUSDT', 'SNTBUSD', 'POLYXBUSD', 'POLYXUSDT']

n = 10000
simple = False
path_csv = "trades.csv"

df = []
for pair in tqdm(PAIRS):
    trades = requests.get("http://localhost:9000/get-trades/" + pair + "?qty=" + str(n) + "&simple=" + simple).json()
    df = df + trades

df.to_csv(path_csv, header=None, index=None)
