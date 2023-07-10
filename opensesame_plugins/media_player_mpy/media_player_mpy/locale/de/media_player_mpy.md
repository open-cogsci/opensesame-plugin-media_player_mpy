# MoviePy-basiertes Media Player-Plugin

Urheberrecht 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

Das media_player_mpy-Plugin fügt Wiedergabemöglichkeiten für Videos zum [OpenSesame-Experiment-Builder][opensesame] hinzu. Dieses Plugin verwendet [Moviepy][mpy_home] als Grundlage. Es sollte in der Lage sein, die meisten modernen Video- und Audioformate zu verarbeiten, vorausgesetzt, ihre Streams sind nicht beschädigt. Wenn eine Datei nicht zu funktionieren scheint, versuchen Sie, eine bessere Version zu finden, oder versuchen Sie, sie in ein anderes Format zu kodieren.

Die beste Wiedergabe wird erreicht, wenn das hardwarebeschleunigte Psychopy oder Expyriment-Backend verwendet wird. Die Leistung könnte bei Verwendung des Legacy-Backends und bei hoher Auflösung oder Bildrate des Films beeinträchtigt sein.

## Plugin-Einstellungen
Das Plugin bietet die folgenden Konfigurationsoptionen aus der GUI:

- *Videodatei* - die abzuspielende Videodatei. Dieses Feld erlaubt variable Notationen wie [video_file], deren Wert Sie in Loop-Elementen angeben können.
- *Audio abspielen* - gibt an, ob das Video mit Audio oder stumm (stummgeschaltet) abgespielt werden soll.
- *Video an Bildschirm anpassen* - gibt an, ob das Video in seiner ursprünglichen Größe wiedergegeben werden soll oder ob es an die Größe des Fensters/Bildschirms skaliert werden soll. Das Skalierungsverfahren behält das ursprüngliche Seitenverhältnis des Films bei.
- *Loop* - gibt an, ob das Video geloopt werden soll, was bedeutet, dass es von Anfang an wieder startet, sobald das Ende des Films erreicht ist.
- *Dauer* - gibt an, wie lange der Film angezeigt werden soll. Erwartet einen Wert in Sekunden, 'keypress' oder 'mouseclick'. Wenn es einen der letzten Werte hat, stoppt die Wiedergabe, wenn eine Taste gedrückt wird oder die Maustaste angeklickt wird.

## Benutzerdefinierter Python-Code für die Behandlung von Tastendruck- und Mausklick Ereignissen
Dieses Plugin bietet auch die Möglichkeit, benutzerdefinierten Ereignisbehandlungscode nach jedem Frame oder nach einem Tastendruck oder Mausklick auszuführen (Beachten Sie, dass die Ausführung von Code nach jedem Frame die 'keypress'-Option im Dauerfeld außer Kraft setzt; Escape-Drücken wird jedoch weiterhin beachtet). Dies ist zum Beispiel nützlich, wenn man zählen möchte, wie oft ein Teilnehmer während der Anzeigedauer des Films die Leertaste (oder eine andere Taste) drückt.

Es gibt einige Variablen, die Sie in dem hier eingegebenen Skript verwenden können:

- `continue_playback` (Wahr oder Falsch) - Bestimmt, ob der Film weiter abgespielt werden soll. Diese Variable ist standardmäßig auf Wahr gesetzt, während der Film abgespielt wird. Wenn Sie die Wiedergabe aus Ihrem Skript heraus stoppen möchten, setzen Sie diese Variable einfach auf Falsch und die Wiedergabe wird gestoppt.
- `exp` - Eine bequeme Variable, die auf das self.experiment-Objekt zeigt
- `frame` - Die Nummer des gerade angezeigten Frames
- `mov_width` - Die Breite des Films in px
- `mov_height` - Die Höhe des Films in px
- `paused` - *Wahr*, wenn die Wiedergabe derzeit pausiert ist, *Falsch*, wenn der Film zurzeit läuft
- `event` - Diese Variable ist etwas besonderes, da ihr Inhalt davon abhängt, ob während des letzten Frames eine Taste oder Maustaste gedrückt wurde. Ist dies nicht der Fall, weist die Event-Variable einfach auf *None* hin. Wenn eine Taste gedrückt wurde, enthält das Ereignis ein Tupel mit an der ersten Position dem Wert "key" und an der zweiten Position dem Wert der gedrückten Taste, zum Beispiel ("key","space"). Wenn eine Maustaste angeklickt wurde, enthält die Ereignisvariable ein Tupel mit an der ersten Position dem Wert "mouse" und an der zweiten Position der Nummer der angeklickten Maustaste, zum Beispiel ("mouse", 2). In dem seltenen Fall, dass während eines Frames mehrere Tasten oder Tasten gleichzeitig gedrückt wurden, enthält die Ereignisvariable eine Liste dieser Ereignisse, zum Beispiel [("key","space"),("key", "x"),("mouse",2)]. In diesem Fall müssen Sie diese Liste in Ihrem Code durchlaufen und alle für Sie relevanten Ereignisse extrahieren.

Neben diesen Variablen haben Sie auch die folgenden Funktionen zur Verfügung:

- `pause()` - Pausiert die Wiedergabe, wenn der Film läuft, und setzt sie fort, wenn dies nicht der Fall ist (Sie könnten es als Pause/Unpause-Umschaltung betrachten)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/
