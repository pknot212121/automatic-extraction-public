import re
def regex_creator(*elementy):
    wzorzec_czesci = []
    for element in elementy:
        element="r:"+element
        if isinstance(element, re.Pattern):
            wzorzec_czesci.append(zmieniony.pattern)
        elif isinstance(element, str) and element.startswith('r:'):
            zmieniony=element[2:].replace("(","(")
            zmieniony=zmieniony.replace("(?:?:","(?:")
            wzorzec_czesci.append(zmieniony)
        else:
            wzorzec_czesci.append(re.escape(str(element)))
    wzorzec = r'[\s\S]*?'.join(f'({part})' for part in wzorzec_czesci)
    return wzorzec


pattern={'sale':r'([s$S]?( )?[pn]( )?(r|_l|n)( )?(z)( )?[eęk\&]( )?(ę)?( )?[dż]( )?(_)?(\.)?[adz]( )?(_)?[djłli;:\]]( )?(_)?[czo]?( )?[eęąyaic€]?)[ ,\n:]|sp›\'\&daj|sprz \(\)|spned%|sprzedaje:|edają:|spncdś/ł.u\'%zom|sprzedz|sprzeda ',
         'Cena':r'((kwo(cie)?|po|[cv]en(i)?[eę]|brutto|netto)( )?[\n]{0,3}( )?(((\d+|i\d+)([,\.; ](\d{3}))([,\.; ]\d{2,3})?)|(\d{2,15})|[,\.]\d{2})(,)?( zł)?( EUR)?)|((([ \n]\d+|[ \n]i\d+)([,\.; ](\d{2,3}))([,\.; ]\d{2,3})?|( \d{2,15}))(,)?( zł| EUR| \([^\(\)]+\) złotych))',
         'łączna_cena':r'łączn(ej|ą|a)([ \n]cen(ie|a|ę)[ \n]w)?[ \n]kwo(cie|ta|tę)( )?[\n]{0,3}( )?(((\d+|i\d+)([,\.; ](\d{2,3}))([,\.; ]\d{2,3})?))|łączn(ej|ą|a)[\n]{0,3}( )?(((\d+|i\d+)([,\.; ](\d{2,3}))([,\.; ]\d{2,3})?))|cał(ej|ą)([ \n]cen(y|ę)([ \n]sprzedaży)?([ \n]w[ \n]kwocie)?|[ \n]kwo(ty|tę|cie)([ \n]w[ \n]cenie)?)[ \n](((\d+|i\d+)([,\.; ](\d{2,3}))([,\.; ]\d{2,3})?))',
         'cena_po_ileś':r'po[ \n](((\d+|i\d+)([,\.; ](\d{2,3}))([,\.; ]\d{2,3})?))',
         'cena_słowna':r'\((\w+[ \n])*?(złotych\)|euro\)|\w+\) zł|groszy\))',
         'Cena2':r'(\d+|i\d+)([,\. ](\d{2,3}))([,\. ]\d{2,3})?(?! ha| m)',
         'cena_łączna_i_słowna':r'łączn(ej|ą|a)([ \n]cen(ie|a|ę)[ \n]w)?[ \n]kwo(cie|ta|tę).{0,15}\((\w+[ \n])*?(złotych\)|euro\)|\w+\) zł|groszy\))|łączn(ej|ą|a).{0,15}\((\w+[ \n])*?(złotych\)|euro\)|\w+\) zł|groszy\))|cał(ej|ą)([ \n]cen(y|ę)([ \n]sprzedaży)?([ \n]w[ \n]kwocie)?|[ \n]kwo(ty|tę|cie)([ \n]w[ \n]cenie)?).{0,15}\((\w+[ \n])*?(złotych\)|euro\)|\w+\) zł|groszy\))',
         'sep':r'([\n]\$|[\n]8( )\d{1}(?!\.)\b)',
         'piwnica':r'[Pp]iwnic[a,y]|[Bb]alkon(u)?|[Nn]ieruchomoś(ć|ci) [Ww]spóln(a|ej)',
         'UMOWA':r'(\n)?[Uu]( )?[Mm]( )?[Oo]( )?[Ww]( )?[AaYy] .{0,30}',
         'Plik':r'FILE:(?P<TAK>.*\.pdf)',
         'buy':r'([Kk]upu[jif](f)?[e,ą](i)?|[Kk]upi[łl][aiy]?)[,\. \n]|nabywa|nabył|nabyła|nabyć|zapłacić|zapłaci|zapłata|zapłacił|zapłat[eę]|zapłaty|podaną|podane|[ \n]w[ \n]tym[ \n]|oświadcza',
         'summary':r'( zł| \([^\(\)]{3,200}\) złotych)',
         'dzialki':r'Działki',
         'powierzchnia':r'\d+[\.,]\d+([ \n])?(\n)*ha|(obszaru|powierzchni|pow\.)[ \n]\d+[\.,]\d+\n',
         'data':r'(199[1-9]|200[0-9]|201[0-9]|202[0-5])[-\.]\d{2}[-\.]\d{2}|\d{2}[-\.]\d{2}[-\.](199[1-9]|200[0-9]|201[0-9]|202[0-5])',
         'numer_działki':r'(nr|numer)[ \n]((\d+/\d{1,2})|([1-9][1-9]\d{1,3}))[ ,\n]',
         'numery_wielokrotne_iteracja':r'\d{2,5}(/\d+)?(,)?([ \n]\((\w+[ \n])*?\w+\))?([ \n])?(obsz|o[ \n]pow)',
         'numer_repetytorium':r'\d{1,5}/(20|19)\d{2}[ ,.\n]',
         'udział_w_drodze':r'udziały|udział',
         'obręb':r'obręb(ie)?([ \n]ewidencyjn(y|ym))?([ \n]nr)?([ \n]numer)?[ \n](\d+|\w+)',
         'miejscowosc':r'położon(y|ej|a|ą|ych|e)([ \n]jest)?[ \n]w(e)?([ \n]miej[sś][cć]ow[ou]ści)?([ \n]wsi)?[ \n]\w+([ \n]\w+)?',
         'pomiejscowosc':r'położon(y|ej|a|ą|ych|e)([ \n]jest)?[ \n]w(e)?([ \n]miej[sś][cć]ow[ou]ści)([ \n]wsi)?[ \n]\w+([ \n]\w+)?',
         'słownik_numer_powierzchnia':r'(\d+/)?\d+(,)?([ \n]\((\w+[ \n])*?\w+\))?([ \n])?(obszaru|(o[ \n])?pow\.|(o[ \n])?powierzchni)[ \n]\d+[\.,]\d+'}

folder="D:/AKTY/mien"
text_file="D:/teksty/mien.txt"
