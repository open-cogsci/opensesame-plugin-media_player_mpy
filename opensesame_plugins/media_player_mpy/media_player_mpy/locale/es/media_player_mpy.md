# Plugin de Reproductor de Medios basado en MoviePy

Derechos de autor 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

El plugin media_player_mpy agrega capacidades de reproducción de video a [OpenSesame experiment builder][opensesame]. Este plugin utiliza [Moviepy][mpy_home] como su base. Debe ser capaz de manejar la mayoría de los formatos modernos de video y audio, aunque es importante que sus flujos no estén corrompidos. Si un archivo no parece funcionar, vea si puede encontrar una versión mejor, o intente volver a codificarlo en un formato diferente.

La mejor reproducción se logrará utilizando el backend acelerado por hardware Psychopy o Expyriment. El rendimiento puede ser deficiente al usar el legado y la película tiene una alta resolución o velocidad de fotogramas.

## Configuraciones del plugin 
El plugin ofrece las siguientes opciones de configuración desde la GUI:

- *Archivo de Video* - el archivo de video a reproducir. Este campo permite notaciones variables tales como [video_file], de las cuales puedes especificar el valor en elementos loop.
- *Reproducir audio* - especifica si el video se reproduce con audio o en silencio (muteado).
- *Ajustar video a pantalla* - especifica si el video debe reproducirse en su tamaño original, o si debe escalarse para adaptarse al tamaño de la ventana/pantalla. El procedimiento de escalado mantiene la relación de aspecto original de la película.
- *Loop* - especifica si el video debe reproducirse en un bucle, lo que significa que comenzará de nuevo desde el principio una vez que se llega al final de la película.
- *Duración* - especifica cuánto tiempo debe mostrarse la película. Espera un valor en segundos, 'keypress' o 'mouseclick'. Si tiene uno de estos últimos valores, la reproducción se detendrá cuando se presione una tecla o se haga clic con el botón del ratón.

## Código Python personalizado para manejo de eventos de tecla y click del ratón
Este plugin también ofrece funcionalidad para ejecutar código personalizado de manejo de eventos después de cada frame, o después de una pulsación de tecla o un click de ratón (Nota que la ejecución de código después de cada frame anula la opción 'keypress' en el campo de duración; sin embargo, aún se escuchan pulsaciones de Escape). Esto es útil, por ejemplo, si uno quiere contar cuántas veces un participante presiona espacio (o cualquier otro botón) durante el tiempo de proyección de la película.

Hay un par de variables accesibles en el script que ingresas aquí:

- `continue_playback` (Verdadero o Falso) - Determina si la película debe seguir reproduciéndose. Esta variable se establece en Verdadero por defecto mientras la película se está reproduciendo. Si quieres detener la reproducción desde tu script, simplemente establece esta variable en Falso y la reproducción se detendrá.
- `exp` - Una variable de conveniencia que apunta al objeto self.experiment
- `frame` - El número del frame actual que se está mostrando
- `mov_width` - El ancho de la película en px
- `mov_height` - La altura de la película en px
- `paused` - *Verdadero* cuando la reproducción está actualmente en pausa, *Falso* si la película está actualmente en ejecución
- `event` - Esta variable es algo especial, ya que su contenido depende de si se presionó una tecla o un botón del ratón durante el último frame. Si este no es el caso, la variable del evento simplemente apuntará a *Ninguno*. Si se presionó una tecla, el evento contendrá una tupla con en la primera posición el valor "key" y en la segunda posición el valor de la tecla que fue presionada, por ejemplo ("key","space"). Si se hizo clic en un botón del ratón, la variable del evento contendrá una tupla con en la primera posición el valor "mouse" y en la segunda posición el número del botón del ratón que fue cliqueado, por ejemplo ("mouse", 2). En la rara ocasión de que varios botones o teclas fueron presionados al mismo tiempo durante un frame, la variable del evento contendrá una lista de estos eventos, por ejemplo [("key","space"),("key", "x"),("mouse",2)]. En este caso, tendrás que recorrer esta lista en tu código y sacar todos los eventos relevantes para ti.

Además de estas variables, también tienes las siguientes funciones a tu disposición:

- `pause()` - Pausa la reproducción cuando la película está en ejecución, y la reanuda en caso contrario (podrías considerarlo como un interruptor de pausa/reanudación)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/