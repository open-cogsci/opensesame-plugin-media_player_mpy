# Plugin Media Player basato su MoviePy

Copyright 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

Il plugin media_player_mpy aggiunge le funzionalità di riproduzione video al [costruttore di esperimenti OpenSesame][opensesame]. Questo plugin utilizza [Moviepy][mpy_home] come base. Dovrebbe essere in grado di gestire la maggior parte dei moderni formati video e audio, anche se è importante che i loro flussi non siano corrotti. Se un file non sembra funzionare, vedi se puoi trovare una versione migliore, o prova a riconvertire in un formato differente.

La migliore riproduzione sarà ottenuta utilizzando il backend accellerato da hardware Psychopy o Expyriment. Le prestazioni potrebbero essere scarse quando si usa il vecchio backend e il filmato ha una alta risoluzione o frame rate.

## Impostazioni del plugin
Il plugin offre le seguenti opzioni di configurazione dall'interfaccia utente:

- *File video* - il file video da riprodurre. Questo campo consente notazioni variabili come [file_video], di cui è possibile specificare il valore negli elementi loop.
- *Riproduci audio* - specifica se il video deve essere riprodotto con audio o in silenzio (muto).
- *Adatta video allo schermo* - specifica se il video deve essere riprodotto nella sua dimensione originale, o se deve essere ridimensionato per adattarsi alle dimensioni della finestra/schermo. La procedura di ridimensionamento mantiene il rapporto d'aspetto originale del filmato.
- *Loop* - specifica se il video deve essere messo in loop, il che significa che partirà di nuovo dall'inizio una volta raggiunta la fine del filmato.
- *Durata* - Specifica per quanto tempo il filmato deve essere visualizzato. Si aspetta un valore in secondi, 'keypress' o 'mouseclick'. Se ha uno degli ultimi valori, la riproduzione si fermerà quando verrà premuto un tasto o cliccato il pulsante del mouse.

## Codice Python personalizzato per gestire gli eventi di pressione dei tasti e click del mouse
Questo plugin offre anche la funzionalità di eseguire codice personalizzato per la gestione degli eventi dopo ogni fotogramma, o dopo una pressione di tasti o un click del mouse (Si noti che l'esecuzione del codice dopo ogni fotogramma annulla l'opzione 'keypress' nel campo durata; Tuttavia le pressioni Escape vengono comunque ascoltate). Questo è utile, ad esempio, se si vuole contare quante volte un partecipante preme lo spazio (o qualsiasi altro tasto) durante la proiezione del filmato.

Ci sono un paio di variabili accessibili nello script che inserisci qui:

- `continue_playback` (True o False) - Determina se il filmato deve continuare a essere riprodotto. Questa variabile è impostata su True di default mentre il filmato è in riproduzione. Se vuoi interrompere la riproduzione dal tuo script, semplicemente imposta questa variabile su False e la riproduzione si fermerà.
- `exp` - Una variabile di comodità che punta all'oggetto self.experiment
- `frame` - Il numero del fotogramma corrente che viene visualizzato
- `mov_width` - La larghezza del filmato in px
- `mov_height` - L'altezza del filmato in px
- `paused` - *True* quando la riproduzione è attualmente in pausa, *False* se il filmato è attualmente in esecuzione
- `event` - Questa variabile è un po' speciale, poiché il suo contenuto dipende da se un tasto o un pulsante del mouse è stato premuto durante l'ultimo fotogramma. Se ciò non è il caso, la variabile event semplicemente punterà a *None*. Se è stato premuto un tasto, event conterrà una tupla con al primo posto il valore "chiave" e al secondo posto il valore del tasto che è stato premuto, ad esempio ("chiave","spazio"). Se è stato cliccato un pulsante del mouse, la variabile event conterrà una tupla con al primo posto il valore "mouse" e al secondo posto il numero del pulsante del mouse che è stato cliccato, ad esempio ("mouse", 2). Nella rara occasione in cui più pulsanti o tasti sono stati premuti contemporaneamente durante un fotogramma, la variabile event conterrà un elenco di questi eventi, ad esempio [("tasto","spazio"), ("tasto", "x"), ("mouse",2)]. In questo caso, dovrai attraversare questo elenco nel tuo codice e estrarre tutti gli eventi rilevanti per te.

Oltre a queste variabili hai anche a disposizione le seguenti funzioni:

- `pause()` - Mette in pausa la riproduzione quando il filmato è in esecuzione, e la riprende altrimenti (potrebbe essere considerata un interruttore di pausa/riprendi)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/