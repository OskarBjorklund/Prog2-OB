import re

def convert_multiple_formats(input_str):
    # Split the input string into lines
    lines = input_str.splitlines()
    
    # Process each line
    converted_lines = []
    for line in lines:
        # Replace one or more spaces with a single tab character
        converted_line = re.sub(r'\s+', '\t', line).strip()  # Use strip() to remove any leading/trailing tabs
        converted_lines.append(converted_line)
    
    # Join the converted lines with newline characters
    return '\n'.join(converted_lines)

# Example usage
input_str = """PB	GU	Fallskärmsjägare 	7	7	6	9	2	6	7	A	9	A	A
GB	GU	Fallskärmsjägare 	5	7	5	9	3	7	7	A	9	A	A
GB	GU	Kustjägare (GB)	7	7	6	9	2	6	7	A	9	A	A
GB	GU	Dykare Amfibie	5	7	5	9	3	6	7	A	9	A	A
GB	GU	Jägarsoldat Armen (GB)	7	7	5	9	2	6	7	B	1	A	A
GB	GU	Förstärkningssoldat J-Bat (GB)	5	5	5	9	2	5	6	B	1	A	B
GB	GU	Förstärkningssoldat Jägarförband (GB)	5	5	5	9	2	5	6	B	9	A	B
Menig	GU	Jägarsoldat Armen	5	6	5	9	2	6	7	B	1	A	A
Menig	GU	Förstärkningssoldat J-Bat 	 	5	5	9	2	5	6	B	1	A	B
Menig	GU	Förstärkningssoldat Jägarförband	 	5	5	9	2	5	6	B	9	A	B
GB	GU	Flygbasjägare (GB)	6	6	5	9	2	6	7	B	1	A	A
Menig	GU	Flygbasjägare	5	5	5	9	2	6	7	B	1	A	A
GB	GU	Jägargruppbefäl	7	7	5	9	2	6	7	B	1	A	A
Menig	GU	Jägare	5	6	5	9	2	6	7	B	1	A	A
GB	GU	Underrättelsegruppbefäl	7	7	5	9	2	6	7	B	1	A	A
Menig	GU	Underrättelsesoldat	5	5	5	9	2	6	7	B	1	A	A
PB	GU	Spaningsplutonbefäl	6	6	6	9	3	6	6	A	9	A	A
GB	GU	Spaningssoldat Armen (GB)	5	5	5	9	2	6	6	B	1	A	B
Menig	GU	Spaningssoldat Armen	 	5	4	9	2	6	6	B	1	A	B
PB	GU	Närskyddsplutonsbefäl	6	6	6	9	2	3	4	B	1	A	D
PB	GU	Skytteplutonbefäl	6	6	6	9	3	5	5	B	9	A	B
GB	GU	Markstridssoldat Armèn (GB)	5	5	5	9	2	4	6	B	1	A	B
GB	GU	Basskyddssoldat Marinen (GB)	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Beriden Högvakt/skyttesoldat Armen (GB)	5	5	5	9	3	4	5	B	1	A	B
GB	GU	Säkgruppbefäl	5	5	5	9	2	5	6	B	1	A	B
GB	GU	Högvakt/skyttesoldat Armen (GB)	5	5	5	9	2	4	6	B	1	A	B
GB	GU	Skyttegruppchef 	5	5	5	9	2	5	6	B	1	A	B
GB	GU	Sjöstrid sonaroperatör 	5	5	5	9	2	2	4	B	9	A	B
GB	GU	Flygbassäkerhetssoldat 	5	5	5	9	2	4	6	B	1	A	B
GB	GU	STRIL-säkerhetssoldat 	5	5	5	9	2	4	6	B	1	A	B
Menig	GU	Skyttesoldat	 	5	4	9	2	4	6	B	1	A	B
Menig	GU	Markstridssoldat Armen	 	5	4	9	2	4	6	B	1	A	B
Menig	GU	Beriden Högvakt/skyttesoldat Armen	 	5	4	9	3	4	5	B	1	A	B
Menig	GU	Säksoldat	 	5	5	9	2	5	6	B	1	A	B
Menig	GU	Högvakt/skyttesoldat Armen	 	5	4	9	2	4	6	B	1	A	B
Menig	GU	Skyttesoldat Armén	 	5	4	9	2	4	6	B	1	A	B
Menig	GU	Basskyddssoldat Marinen	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Flygbassäkerhetssoldat	 	5	4	9	2	4	6	B	1	A	B
PB	GU	Stridsfordonsplutonsbefäl	7	6	6	8	3	3	4	A	9	A	B
PB	GU	Stridsvagnsplutonsbefäl	7	6	6	8	3	3	4	A	9	A	B
GB	GU	Vagnchef stridsfordon/förare 	5	6	5	8	2	4	5	A	9	A	B
GB	GU	Vagnchef	5	6	6	8	2	4	5	A	9	A	B
GB	GU	Stridsvagn skytt/laddare 	5	6	5	8	2	4	5	A	9	A	B
GB	GU	Vagnchef stridsvagn/förare 	5	6	5	8	2	4	5	A	9	A	B
GB	GU	Stridsvagnsskytt	5	6	5	8	2	4	5	A	9	A	B
GB	GU	Skyttesoldat strf Armén (GB)	5	5	5	8	2	4	6	B	1	A	B
GB	GU	Stridsfordonsskytt 	5	6	5	8	2	4	5	A	9	A	B
Menig	GU	Stridsfordonsskytt	 	6	5	8	2	4	5	A	9	A	B
Menig	GU	Stridsvagnsförare	 	5	5	8	2	4	5	A	9	A	B
Menig	GU	Stridsfordonsförare	 	5	5	8	2	4	5	A	9	A	B
Menig	GU	Stridsvagn skytt/laddare	 	6	5	8	2	4	5	A	9	A	B
Menig	GU	Skyttesoldat Strf Armen	 	5	4	8	2	4	6	B	1	A	B
PB	GU	Eldledningsplutonsbefäl	7	6	6	9	2	3	4	B	9	A	B
GB	GU	Eldledningssoldat Armen (GB)	5	5	5	9	2	3	4	B	1	A	B
Menig	GU	Eldledningssoldat Armen	 	5	4	9	2	3	4	B	1	A	B
PB	GU	Granatkastarplutonsbefäl	6	6	6	9	2	3	4	B	9	A	B
GB	GU	Granatkastargruppchef 	5	5	5	9	2	3	4	B	1	A	B
Menig	GU	Granatkastarsoldat/förare Armen	 	5	4	9	2	3	4	B	9	A	B
Menig	GU	Granatkastarsoldat Armen	 	5	4	9	2	3	4	B	1	A	B
GB	GU	Artillerisoldat Armen (GB)	5	5	5	9	2	3	5	C	9	A	B
GB	GU	Artillerisoldat/förare Armen 	5	5	5	9	2	3	5	C	1	A	B
Menig	GU	Artillerisoldat Armen	 	5	5	9	2	3	5	C	9	A	B
Menig	GU	Artillerisoldat/förare Armen	 	5	4	9	2	3	5	C	1	A	B
PB	GU	Luftvärnsplutonsbefäl Sensor	6	6	6	9	2	4	4	B	1	A	B
PB	GU	Luftvärnsplutonsbefäl	7	6	6	9	3	3	4	B	9	A	B
PB	GU	Luftvärnsplutonsbefäl Sensor	7	6	6	9	3	3	4	B	1	A	B
GB	GU	Luftvärnsoldat Armen (GB)	5	5	5	9	2	3	4	B	1	A	B
Menig	GU	Luftvärnsoldat Armen	 	5	4	9	2	3	4	B	1	A	B
GB	GU	Skyttesoldat gruppchef	5	5	5	9	2	2	4	B	1	A	E
Menig	GU	Skyttesoldat/förare PB 8	 	4	4	9	1	2	4	C	1	A	J
Menig	GU	Skyttesoldat/skarpskytt	 	4	4	9	1	2	4	C	1	A	J
Menig	GU	Skyttesoldat/signalist 	 	4	4	9	1	2	4	C	1	A	J
Menig	GU	Skyttesoldat/förare bandvagn	 	4	4	8	1	2	4	C	1	A	J
Menig	GU	Skyttesoldat/stridssjukvård 	 	5	4	9	2	3	4	C	1	A	D
Menig	GU	Skyttesoldat	 	4	4	9	1	2	4	C	1	A	J
GB	GU	Amfibiesoldat (GB)	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Skyttesoldat Amfibie 	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Robot-/grksoldat Amfibie 	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Eldledningssoldat Amfibie 	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Stridsbåtsförare Amfibie	6	6	6	9	3	5	6	A	9	A	B
GB	GU	Säkerhetssoldat Sjö (GB)	5	5	5	9	2	5	6	B	1	A	B
GB	GU	Mingruppbefäl Amfibie	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Bevakningsbåtsoldat (GB)	5	5	5	9	2	3	4	B	9	A	B
GB	GU	Samband/ledningssoldat Amfibie 	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Logistiksoldat Amfibie 	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Sjukvårdssoldat Amfibie (GB)	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Fordonsförare Amfibie (GB)	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Kock Amfibie (GB)	5	5	5	9	2	5	6	B	9	A	B
Menig	GU	Amfibiesoldat	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Skyttesoldat Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Robot-/grksoldat Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Eldledningssoldat Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Säkerhetssoldat Sjö	 	5	4	9	2	5	6	B	1	A	B
Menig	GU	Minsoldat Amfibie 	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Bevakningsbåtsoldat	 	5	4	9	2	3	4	B	9	A	B
Menig	GU	Samband/ledningssoldat Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Logistiksoldat Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Sjukvårdssoldat Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Fordonsförare Amfibie	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	Kock Amfibie	 	5	4	9	2	5	6	B	9	A	B
GB	GU	Stridsbåtsförare MarinB	6	6	6	9	3	5	6	B	9	A	B
GB	GU	Sambandsoperatör MarinB  (GB)	5	5	5	9	2	2	4	B	9	A	B
GB	GU	Ubåtsmatros ledning	5	5	5	9	2	2	4	B	9	A	B
GB	GU	Sjöstrid samband 	5	5	5	9	2	2	4	B	9	A	B
GB	GU	Sjöstrid signalmatros	5	5	5	9	2	2	4	B	9	A	B
Menig	GU	Sambandsoperatör MarinB	 	5	4	9	2	2	4	B	9	A	B
GB	GU	Ubåtsmatros sensor 	5	5	5	9	2	2	4	B	9	A	B
GB	GU	Röjdykare	5	7	5	9	3	6	7	A	9	A	A
GB	GU	Teknik sjöman Marinen 	5	5	5	9	2	2	4	C	9	A	B
GB	GU	Teknik soldat Marinen 	5	5	5	9	2	2	4	C	9	A	B
GB	GU	Ubåtsmatros teknik 	5	5	5	9	2	2	4	C	9	A	B
Menig	GU	Teknik soldat Marinen	 	5	4	9	2	2	4	C	9	A	B
GB	GU	Ubåtskock (GB)	5	5	5	9	2	2	4	C	9	A	B
GB	GU	Kock Sjöstrid (GB)	5	5	5	9	2	2	4	C	9	A	B
Menig	GU	Ubåtskock	 	5	4	9	2	2	4	C	9	A	B
Menig	GU	Kock Sjöstrid	 	5	4	9	2	2	4	C	9	A	B
PB	GU	Motorredskapsplutonbefäl	6	6	6	9	2	3	4	C	1	A	D
PB	GU	Broplutonchef	6	6	6	9	3	4	4	C	1	A	B
PB	GU	Ingenjörplutonchef	6	6	6	9	2	4	4	C	1	A	D
GB	GU	Fältarbetessoldat/förare Armen 	5	5	5	9	2	4	6	B	1	A	B
GB	GU	Fältarbetessoldat Armen 	5	5	5	9	2	4	6	B	1	A	B
GB	GU	Fältarbetsdykare (GB)	5	6	5	9	4	5	6	A	9	A	A
Menig	GU	Fältarbetessoldat Armen	 	5	4	9	2	4	6	B	1	A	B
Menig	GU	Fältarbetsdykare 	 	6	4	9	4	5	6	A	9	A	A
Menig	GU	Fältarbetessoldat/förare Armen	 	5	4	9	2	4	6	B	1	A	B
PB	GU	Pionjärplutonsbefäl	6	6	6	9	2	5	5	B	9	A	D
Menig	GU	Motorredskapsförare Armen	 	5	5	9	2	3	4	C	1	A	D
PB	GU	CBRN-befäl	6	6	6	9	3	2	4	C	1	A	D
GB	GU	CBRN GRUPPCHEF	5	5	5	9	2	3	5	C	1	A	B
Menig	GU	CBRN SOLDAT	 	5	4	9	2	3	5	C	1	A	B
Menig	GU	Skyddsman(cbrnsoldat)	 	5	5	9	2	4	6	B	9	A	B
GB	GU	R3 Räddningssoldat Flyg (GB)	5	5	5	9	2	5	6	B	9	A	B
GB	GU	R3 Fälthållningssoldat Flyg (GB)	5	5	5	9	2	3	4	C	1	A	D
Menig	GU	R3 Räddningssoldat Flyg	 	5	4	9	2	5	6	B	9	A	B
Menig	GU	R3 Fälthållningssoldat Flyg	 	5	4	9	2	3	4	C	1	A	D
GB	GU	Spaningsoperatör MarinB (GB)	5	5	5	9	2	2	4	B	9	A	B
GB	GU	Sjöövervakningoperatör MarinB (GB)	5	5	5	9	2	2	4	B	9	A	B
Menig	GU	Spaningsoperatör MarinB	 	5	4	9	2	2	4	B	9	A	B
Menig	GU	Sjöövervakningoperatör MarinB	 	5	4	9	2	2	4	B	9	A	B
GB	GU	Samband/ledningssoldat Flyg (GB)	5	5	5	9	2	2	4	C	9	A	D
GB	GU	Luftbevakningssoldat (GB)	5	5	5	9	2	2	4	C	9	A	D
GB	GU	Samband/ledningssoldat STRIL (GB)	5	5	5	9	2	2	4	C	9	A	D
Menig	GU	Samband/ledningssoldat Flyg	 	5	4	9	2	2	4	C	9	A	D
Menig	GU	Samband/ledningssoldat STRIL	 	5	4	9	2	3	4	C	9	A	D
PB	GU	Ledningsplutonsbefäl	6	6	6	9	2	3	4	C	9	A	D
PB	GU	Radiolänkplutonsbefäl	6	6	6	9	2	3	4	C	1	A	B
PB	GU	Radiolänktroppchef	6	6	6	9	2	3	4	C	1	A	B
GB	GU	Radiolänkgruppchef	5	5	5	9	2	3	4	C	9	A	B
Menig	GU	Radiolänksoldat (Radiolänkman)	 	5	4	9	2	3	4	C	9	A	B
GB	GU	Samband/lednsoldat Armén(GB)	5	5	5	9	2	2	4	C	1	A	D
Menig	GU	Samband/ledningssoldat Armen	 	5	4	9	2	2	4	C	1	A	D
Menig	GU	Motorcykelordonnans	 	5	4	9	2	3	4	C	1	A	D
GB	GU	Underättelsesoldat Armen (GB)	5	6	5	9	1	3	5	C	1	A	B
GB	GU	Underrättelseassistent Flyg (GB)	6	6	5	9	1	2	5	C	1	A	B
GB	GU	Stabsassistent Armen (GB)	5	5	5	9	2	3	4	C	1	A	D
GB	GU	Stabsassistent (GB)	5	5	5	9	2	2	4	C	9	A	D
Menig	GU	Stabsassistent Armen	 	5	4	9	2	2	4	C	1	A	D
Menig	GU	Stabsbiträde	 	5	4	9	2	3	4	C	1	A	D
PB	GU	Ledningsplutonsbefäl	6	6	6	9	2	4	4	A	9	A	B
GB	GU	Informationssoldat	5	5	5	9	2	3	4	C	1	A	D
Menig	GU	Informationssoldat	 	5	5	9	2	3	4	C	9	A	D
Menig	GU	Driftbiträde	 	5	4	9	2	3	4	C	9	A	D
PB	GU	Underhållsplutonsbefäl	6	6	6	9	2	3	4	C	1	A	D
PB	GU	Kvartermästare	6	6	6	9	2	3	4	C	1	A	D
PB	GU	Trossplutonsbefäl	6	6	6	9	2	3	4	C	1	A	D
GB	GU	Flygterminalsoldat (GB)	5	5	5	9	2	2	4	C	1	A	D
GB	GU	Logistikgruppchef	5	5	5	9	2	3	4	C	1	A	D
Menig	GU	Logistiksoldat Armen	 	5	4	9	2	3	4	C	1	A	D
Menig	GU	Flygterminalsoldat	 	5	4	9	2	2	4	C	1	A	D
GB	GU	Kock MarinB (GB)	5	5	5	9	2	2	4	C	9	A	B
GB	GU	Kock Armen(GB)	5	5	5	9	2	3	4	C	1	A	D
GB	GU	Kock Flyg (GB)	5	5	5	9	2	2	4	C	1	A	D
GB	GU	Kokgruppchef	5	5	5	9	2	3	4	C	1	A	D
Menig	GU	Kock MarinB	 	5	4	9	2	2	4	C	9	A	B
Menig	GU	Kock Armen 	 	5	4	9	2	3	4	C	1	A	D
Menig	GU	Kock Flyg	 	5	4	9	2	2	4	C	1	A	D
GB	GU	Drivmedelssoldat Flyg (GB)	5	5	5	9	2	2	4	C	1	A	D
Menig	GU	Drivmedelsman	 	5	4	9	2	3	4	C	1	A	D
Menig	GU	Drivmedelssoldat Flyg	 	5	4	9	2	2	4	C	1	A	D
PB	GU	Sjukvårdsplutonsbefäl	6	6	6	9	2	3	4	C	1	A	D
PB	GU	Sjukvårdsplutonsbefäl	6	6	6	9	2	3	4	C	1	A	D
GB	GU	Sjukvårdssoldat Flyg	5	5	5	9	2	2	5	C	9	A	D
GB	GU	Sjukvårdssoldat/förare Flyg	5	5	5	9	2	2	5	C	9	A	D
GB	GU	Sjukvårdssoldat Armén(GB)	5	5	5	9	2	3	4	C	9	A	D
GB	GU	Sjukvårdsgruppchef 	5	5	5	9	2	3	4	C	9	A	D
Menig	GU	Sjukvårdare	 	5	4	9	2	3	4	C	9	A	D
Menig	GU	Sjuktransportman	 	5	4	9	2	3	4	C	1	A	D
PB	GU	Trafikplutonbefäl (KB)	6	6	6	9	2	3	4	C	1	A	D
GB	GU	Trafikgruppbefäl	5	5	5	9	2	3	4	C	1	A	D
Menig	GU	Trafikman	 	5	4	9	2	2	4	C	1	A	D
PB	GU	Transportplutonsbefäl	6	6	6	9	2	3	4	C	1	A	D
GB	GU	Fordonsförare Armen (GB)	5	5	5	9	2	2	4	C	1	A	D
GB	GU	Fordonsförare Flyg (GB)	5	5	5	9	2	2	4	C	1	A	D
GB	GU	Logistiksoldat Flyg (GB)	5	5	5	9	2	2	4	C	1	A	D
Menig	GU	Fordonsförare Armen	 	5	4	9	2	3	4	C	1	A	D
Menig	GU	Fordonsförare Flyg	 	5	4	9	2	2	4	C	1	A	D
Menig	GU	Lastbilsförare	 	5	4	9	2	2	4	C	1	A	D
Menig	GU	Logistiksoldat Flyg	 	5	4	9	2	2	4	C	1	A	D
Menig	GU	Bandvagnsförare 	 	5	4	9	2	3	4	C	9	A	D
PB	GU	Reparationsplutonchef	6	6	6	9	2	3	4	C	1	A	D
PB	GU	Reparationsplutonsbefäl	6	6	6	9	2	3	4	C	9	A	D
GB	GU	Mekaniker mekanik Armen (GB)	5	5	5	9	2	3	4	C	9	A	D
GB	GU	Markmekaniker mekanik Flyg	5	5	5	9	2	2	4	C	9	A	D
Menig	GU	Mekaniker mekanik Armen	 	5	4	9	2	3	4	C	9	A	D
GB	GU	Mekaniker elektronik Armen (GB)	5	5	5	9	2	3	4	C	9	A	D
GB	GU	Markmekaniker elektronik Flyg	5	5	5	9	2	2	4	C	9	A	D
Menig	GU	Mekaniker elektronik Armen	 	5	4	9	2	3	4	C	9	A	D
GB	GU	Bärgningsgruppchef	5	5	5	9	2	4	5	C	9	A	B
Menig	GU	Bärgningsman	 	5	4	9	2	4	5	B	9	A	B
GB	GU	Flygmaterielmekaniker helikopter	5	5	5	9	2	2	4	C	9	A	D
GB	GU	Flygmekaniker	5	5	5	9	2	2	4	C	9	A	D
GB	GU	Militärpolis Armen	5	5	5	9	4	4	6	B	9	A	B
GB	GU	Militärpolis/förare Armen	5	5	5	9	4	4	6	B	9	A	B
GB	GU	Telekrig sjöstrid	5	5	5	9	2	2	4	B	9	A	B
Menig	GU	Ledning/telekrigsoldat Armen	 	6	6	9	2	3	5	C	1	A	B
Menig	GU	Ledning/telekrigsoldat Armen Förare	 	6	6	9	2	3	5	C	1	A	B
GB	GU	Cybersoldat (GB)	5	5	6	9	1	2	4	C	1	A	D
Menig	GU	Cybersoldat	 	5	6	9	1	2	4	C	1	A	D
Menig	GU	Förhörssoldat	6	6	6	9	1	2	4	C	1	A	D
PB	GU	Systemtekniker	6	6	6	9	2	2	4	C	9	A	D
GB	GU	Systemtekniker	5	5	5	9	2	3	4	C	9	A	D
GB	GU	Marktelemekaniker Flyg	5	5	5	9	2	2	4	C	9	A	D
GB	GU	Teknik soldat Amfibie 	5	5	5	9	2	5	6	B	9	A	B
GB	GU	Mekaniker Amfibie (GB)	5	5	5	9	3	5	6	B	9	A	B
Menig	GU	Mekaniker Amfibie	 	5	4	9	2	5	6	B	9	A	B
GB	GU	Stridsbåtsförare Amfibie	6	6	6	9	3	5	6	A	9	A	B
"""

converted_str = convert_multiple_formats(input_str)
print(converted_str)
