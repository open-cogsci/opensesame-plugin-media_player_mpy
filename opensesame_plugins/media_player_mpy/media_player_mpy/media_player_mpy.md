# MoviePy based Media Player plugin

Copyright 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

The media_player_mpy plug-in adds video playback capabilities to the [OpenSesame experiment builder][opensesame]. This plug-in uses [Moviepy][mpy_home] as its basis. It should be able to handle most modern video and audio formats, although it is important that their streams are not corrupted. If a file does not appear to work, see if you can find a better version, or try to reencode it into a different format.

The best playback will be achieved by using the hardware accelerated Psychopy or Expyriment backend. Performance might be lacking when using the legacy and  the movie has a high resolution or frame rate.

## Plugin settings
The plugin offers the following configuration options from the GUI:

- *Video file* - the video file to be played. This field allows variable notations such as [video_file], of which you can specify the value in loop items.
- *Play audio* - specifies whether the video is to be played with audio or in silence (muted).
- *Fit video to screen* - specifies whether the video should be played in its original size, or if it should be scaled to fit the size of the window/screen. The rescaling procedure maintains the original aspect ratio of the movie.
- *Loop* - specifies if the video should be looped, meaning that it will start again from the beginning once the end of of the movie is reached.
- *Duration* - Specifies how long the movie should be displayed. Expects a value in seconds, 'keypress' or 'mouseclick'. It it has one of the last values, playback will stop when a key is pressed or the mouse button is clicked.

## Custom Python code for handling keypress and mouseclick events
This plugin also offers functionality to execute custom event handling code after each frame, or after a key press or mouse click (Note that execution of code after each frame nullifies the 'keypress' option in the duration field; Escape presses however are still listened to). This is for instance useful, if one wants to count how many times a participants presses space (or any other button) during the showtime of the movie.

There are a couple of variables accessible in the script you enter here:

- `continue_playback` (True or False) - Determines if the movie should keep on playing. This variable is set to True by default while the movie is playing. If you want to stop playback from your script, simply set this variable to False and playback will stop.
- `exp` - A convenience variable pointing to the self.experiment object
- `frame` - The number of the current frame that is being displayed
- `mov_width` - The width of the movie in px
- `mov_height` - The height of the movie in px
- `paused` - *True* when playback is currently paused, *False* if movie is currently running
- `event` - This variable is somewhat special, as its contents depend on whether a key or mouse button was pressed during the last frame. If this is not the case, the event variable will simply point to *None*. If a key was pressed, event will contain a tuple with at the first position the value "key" and at the second position the value of the key that was pressed, for instance ("key","space"). If a mouse button was clicked, the event variable will contain a tuple with at the first position the value "mouse" and at the second position the number of the mouse button that was clicked, for instance ("mouse", 2). In the rare occasion that multiple buttons or keys were pressed at the same time during a frame, the event variable will contain a list of these events, for instance [("key","space"),("key", "x"),("mouse",2)]. In this case, you will need to traverse this list in your code and pull out all events relevant to you.

Next to these variables you also have the following functions at your disposal:

- `pause()` - Pauses playback when the movie is running, and unpauses it otherwise (you could regard it as a pause/unpause toggle)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/

