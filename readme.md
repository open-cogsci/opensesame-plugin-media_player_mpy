# MoviePy media player plugin for OpenSesame

This plugin enables movie playback in OpenSesame using the MoviePy module. To use it, copy the folder `media_player_mpy` into your OpenSesame plugins directory. Alternatively, if you are on Linux or Mac OS, you can also place it in your homefolder under `~/.opensesame/plugins/media_player_mpy` and OpenSesame should pick it up. If properly detected, the plugin should appear as a draggable item in the items list. This plugin should work on all major platforms such as Windows, Mac OS X and Linux.

*Note:* the first time that you run an experiment that makes use of htis plugin, moviepy will try to determine if ffmpeg (which it uses to read and decode movies) is installed on your system. If it doesn't detect it, moviepy will attempt to download ffmpeg for you. This may take a while and will lock up the OpenSesame interface in the mean time. If you experience a froze interface on the first run, please be patient to let the download of ffmpeg in the background finish. You should see an indication of the download progress in your terminal.

## Dependencies

This module depends on the following other libraries. So make sure you have them installed if you run OpenSesame from source (the distributed versions of OpenSesame should already contain these libraries, so no further action is required.)

- mediadecoder (http://github.com/dschreij/python-mediadecoder)
- MoviePy (http://zulko.github.io/moviepy/)
- pyAudio (https://people.csail.mit.edu/hubert/pyaudio/)
- pygame (http://www.pygame.org/)
- pyOpenGL (http://pyopengl.sourceforge.net/)

## Alternative OpenSesame movie player plugins

I dare to say that this is the best implementation of a movie player for OpenSesame yet, but here are some others:

- [media_player_gst](https://github.com/dschreij/media_player_gst) - Based on the GStreamer framework (0.10). Worked quite well, except on OSX where videos suddenly tended to freeze.
- [media_player_vlc](https://github.com/dschreij/media_player_vlc) - Based on the vlc python bindings. It 'hijacks' a window by its handle and renders the video in there, but this all does not work very gracefully.

## License

Like moviepy, this module is licensed under the MIT license:

The MIT License (MIT)
Copyright (c) 2016-2020 Daniel Schreij

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
