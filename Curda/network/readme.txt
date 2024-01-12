Till en början tänkte jag att det skulle var en smart ide att endast servern skickar en lista med alla spelare. Sedan så sår klienten jämföra sin föregående spelarlista
med den nya spelarlistan som servern skickat. Däremot var det jobbigare än vad jag hade tänk mig eftersom det finns 3 olika perspektiv mellan alla spelare där dessa
perspektiv har olia vyer. Nu funkar det ganska bra förutom att det blev lite många if-satser på grund av de många olika perspektiven. En ganska stor bugg med programmet
är att om ena klienten väljer sitt val, men sedan ansluter en till klient innan den andre spelaren har gjort sitt val så går programmet bananas. Det har något att göra
med att när en ny klient ansluter mid-game så skickar servern en ny lista som återställer spelarvalen vilket förstör programmet. Om man bortser från detta fungerar det 
ganska bra. Det är ett sten sax påse spel fast med 5 olika val istället för de traditionella 3.
