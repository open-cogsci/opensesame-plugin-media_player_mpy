# Plugin lecteur multimédia basé sur MoviePy

Copyright 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

Le plugin media_player_mpy ajoute des capacités de lecture vidéo au [constructeur d'expériences OpenSesame][opensesame]. Ce plugin utilise [Moviepy][mpy_home] comme base. Il devrait être capable de gérer la plupart des formats vidéo et audio modernes, bien qu'il soit important que leurs flux ne soient pas corrompus. Si un fichier ne semble pas fonctionner, voyez si vous pouvez trouver une meilleure version, ou essayez de le réencoder dans un format différent.

La meilleure lecture sera obtenue en utilisant le backend accéléré par matériel Psychopy ou Expyriment. Les performances peuvent être insuffisantes lors de l'utilisation de l'ancien système et le film a une haute résolution ou vitesse d'images.

## Paramètres du plugin
Le plugin offre les options de configuration suivantes depuis l'interface graphique :

- *Fichier vidéo* - le fichier vidéo à lire. Ce champ permet des notations variables telles que [video_file], dont vous pouvez spécifier la valeur dans les éléments de boucle.
- *Lire l'audio* - spécifie si la vidéo doit être lue avec de l'audio ou en silence (muet).
- *Adapter la vidéo à l'écran* - spécifie si la vidéo doit être lue dans sa taille d'origine, ou si elle doit être mise à l'échelle pour s'adapter à la taille de la fenêtre/écran. La procédure de redimensionnement maintient le rapport d'aspect original du film.
- *Boucle* - spécifie si la vidéo doit être en boucle, ce qui signifie qu'elle recommencera depuis le début une fois la fin du film atteinte.
- *Durée* - Spécifie combien de temps le film doit être affiché. Attend une valeur en secondes, 'keypress' ou 'mouseclick'. S'il a l'une des dernières valeurs, la lecture s'arrête quand une touche est pressée ou le bouton de la souris est cliqué.

## Code Python personnalisé pour gérer les événements appuyez sur une touche et clic de souris
Ce plugin offre également la possibilité d'exécuter du code personnalisé pour gérer les événements après chaque image, ou après une pression de touche ou un clic de souris (Notez que l'exécution du code après chaque image annule l'option 'keypress' dans le champ de durée ; cependant, les pressions escape sont toujours écoutées). C'est par exemple utile si l'on veut compter combien de fois un participant appuie sur espace (ou tout autre bouton) pendant la durée du film.

Il y a quelques variables accessibles dans le script que vous entrez ici :

- `continue_playback` (True ou False) - Détermine si le film doit continuer à être lu. Cette variable est définie sur Vrai par défaut pendant la lecture du film. Si vous voulez arrêter la lecture depuis votre script, il vous suffit de définir cette variable sur False et la lecture s'arrête.
- `exp` - Une variable de commodité pointant vers l'objet self.experiment
- `frame` - Le numéro de l'image actuelle qui est affichée
- `mov_width` - La largeur du film en px
- `mov_height` - La hauteur du film en px
- `paused` - *True* lorsque la lecture est actuellement en pause, *False* si le film est actuellement en cours d'exécution
- `event` - Cette variable est un peu spéciale, car son contenu dépend de la pression d'une touche ou d'un bouton de souris lors de la dernière image. Si ce n'est pas le cas, la variable d'événement pointera simplement vers *None*. Si une touche a été pressée, l'événement contiendra un tuple avec à la première position la valeur "key" et à la seconde position la valeur de la touche qui a été pressée, par exemple ("key", "space"). Si un bouton de souris a été cliqué, la variable d'événement contiendra un tuple avec à la première position la valeur "mouse" et à la seconde position le numéro du bouton de souris qui a été cliqué, par exemple ("mouse", 2). Dans le cas rare où plusieurs boutons ou touches ont été pressés en même temps lors d'une image, la variable d'événement contiendra une liste de ces événements, par exemple [("key", "space"),("key", "x"),("mouse",2)]. Dans ce cas, vous devrez parcourir cette liste dans votre code et retirer tous les événements qui vous concernent.

En plus de ces variables, vous avez aussi les fonctions suivantes à votre disposition :

- `pause()` - Met en pause la lecture lorsque le film est en cours d'exécution, et la dépause autrement (vous pourriez le considérer comme une bascule pause/dépause)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/