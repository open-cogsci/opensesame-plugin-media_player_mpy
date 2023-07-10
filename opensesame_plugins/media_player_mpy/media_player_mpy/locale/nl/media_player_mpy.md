# MoviePy-gebaseerde Media Player-plugin

Copyright 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

De media_player_mpy plug-in voegt videoweergave functionaliteiten toe aan de [OpenSesame experiment builder][opensesame]. Deze plug-in gebruikt [Moviepy][mpy_home] als basis. Het zou in staat moeten zijn om de meeste moderne video- en audioformaten te verwerken, hoewel het belangrijk is dat hun streams niet beschadigd zijn. Als een bestand niet lijkt te werken, kijk dan of je een betere versie kunt vinden, of probeer het opnieuw te coderen naar een ander formaat.

De beste weergave wordt bereikt door gebruik te maken van de hardwareversnelde Psychopy of Expyriment backend. De prestaties kunnen achterblijven als de legacy wordt gebruikt en de film een hoge resolutie of framerate heeft.

## Plugin-instellingen
De plugin biedt de volgende configuratie-opties vanuit de GUI:

- *Videobestand* - het videobestand dat moet worden afgespeeld. Dit veld staat variabele notaties toe, zoals [video_file], waarvan u de waarde kunt opgeven in loop items.
- *Audio afspelen* - specificeert of de video wordt afgespeeld met audio of in stilte (gedempt).
- *Video aanpassen aan scherm* - specificeert of de video moet worden afgespeeld in de oorspronkelijke grootte, of dat het moet worden geschaald om te passen in de grootte van het venster/scherm. De herschaling procedure behoudt de oorspronkelijke beeldverhouding van de film.
- *Herhalen* - specificeert of de video moet worden herhaald, wat betekent dat deze opnieuw zal starten vanaf het begin zodra het einde van de film is bereikt.
- *Duur* - Geeft aan hoe lang de film moet worden weergegeven. Verwacht een waarde in seconden, 'keypress' of 'mouseclick'. Als het een van deze laatste waarden heeft, stopt de weergave wanneer een toets is ingedrukt of de muisknop is geklikt.

## Aangepaste Python-code voor het afhandelen van keypress en mouseclick gebeurtenissen
Deze plugin biedt ook functionaliteit om aangepaste code voor gebeurtenisafhandeling uit te voeren na elke frame, of na een toetsaanslag of muis klik (let op: uitvoering van code na elke frame ontkracht de 'keypress'-optie in het duurveld; het indrukken van Escape wordt echter nog steeds beluisterd). Dit is bijvoorbeeld nuttig, als men wil tellen hoe vaak een deelnemer op spatie (of een andere knop) drukt tijdens de afspeeltijd van de film.

Hier zijn een aantal variabelen beschikbaar in het script dat je hier invoert:

- `continue_playback` (True of False) - Bepaalt of de film moet blijven spelen. Deze variabele is standaard ingesteld op True terwijl de film wordt afgespeeld. Als je de weergave wilt stoppen vanuit je script, zet je deze variabele eenvoudigweg op False en de weergave stopt.
- `exp` - Een handige variabele die wijst naar het self.experiment object
- `frame` - Het nummer van de huidige frame die wordt weergegeven
- `mov_width` - De breedte van de film in px
- `mov_height` - De hoogte van de film in px
- `paused` - *True* wanneer de weergave momenteel is gepauzeerd, *False* als de film momenteel draait
- `event` - Deze variabele is enigszins speciaal, aangezien de inhoud ervan afhangt van het feit of er tijdens de laatste frame een sleutel of muisknop is ingedrukt. Als dit niet het geval is, zal de event variabele eenvoudigweg naar *None* verwijzen. Als er een toets is ingedrukt, zal event een tuple bevatten met op de eerste plaats de waarde "key" en op de tweede plaats de waarde van de ingedrukte toets, bijvoorbeeld ("key","space"). Als er een muisknop is geklikt, zal de event variabele een tuple bevatten met op de eerste plaats de waarde "mouse" en op de tweede plaats het nummer van de geklikte muisknop, bijvoorbeeld ("mouse", 2). In het zeldzame geval dat er tegelijkertijd meerdere knoppen of toetsen zijn ingedrukt tijdens een frame, zal de event variabele een lijst van deze gebeurtenissen bevatten, bijvoorbeeld [("key","space"),("key", "x"),("mouse",2)]. In dit geval, zul je deze lijst moeten doorlopen in je code en alle voor jou relevante gebeurtenissen eruit moeten halen.

Naast deze variabelen heb je ook de volgende functies tot je beschikking:

- `pause()` - Pauzeert de weergave wanneer de film wordt afgespeeld, en hervat deze anders (je zou het kunnen beschouwen als een pause/unpause toggle)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/
