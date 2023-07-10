# Plugin de Reprodutor de Mídia baseado em MoviePy

Direitos autorais 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

O plugin media_player_mpy acrescenta capacidades de reprodução de vídeo ao [construtor de experimento OpenSesame][opensesame]. Este plugin utiliza [Moviepy][mpy_home] como sua base. Ele deve ser capaz de lidar com a maioria dos formatos de vídeo e áudio modernos, embora seja importante que suas transmissões não estejam corrompidas. Se um arquivo não parecer funcionar, veja se você consegue encontrar uma versão melhor, ou tente reencodá-lo em um formato diferente.

A melhor reprodução será alcançada ao usar o backend acelerado por hardware Psychopy ou Expyriment. A performance pode ser insuficiente ao usar o backend legado e o filme tiver alta resolução ou taxa de quadros.

## Configurações do plugin
O plugin oferece as seguintes opções de configuração a partir da GUI:

- *Arquivo de vídeo* - o arquivo de vídeo a ser reproduzido. Este campo permite notações de variáveis, como [video_file], das quais você pode especificar o valor em itens de laço.
- *Reproduzir áudio* - especifica se o vídeo deve ser reproduzido com áudio ou em silêncio (mudo).
- *Fit video to screen* - especifica se o vídeo deve ser reproduzido em seu tamanho original, ou se deve ser dimensionado para caber no tamanho da janela/tela. O procedimento de redimensionamento mantém a proporção original do filme.
- *Loop* - especifica se o vídeo deve ser repetido, ou seja, se começará de novo do começo uma vez que o final do filme é atingido.
- *Duração* - Especifica quanto tempo o filme deve ser exibido. Espera um valor em segundos, 'keypress' ou 'mouseclick'. Se tiver um dos últimos valores, a reprodução será interrompida quando uma tecla for pressionada ou o botão do mouse for clicado.

## Código Python personalizado para lidar com eventos de pressionamento de teclas e cliques do mouse
Este plugin também oferece funcionalidade para executar código personalizado de tratamento de eventos após cada quadro, ou após um pressionamento de tecla ou clique do mouse (Note que a execução de código após cada quadro anula a opção 'keypress' no campo de duração; Entretanto, ainda se escuta pressionamentos de Escape). Isso é por exemplo útil, se alguém quer contar quantas vezes um participante pressiona espaço (ou qualquer outro botão) durante o tempo de show do filme.

Há algumas variáveis acessíveis no script que você insere aqui:

- `continue_playback` (Verdadeiro ou Falso) - Determina se o filme deve continuar a ser reproduzido. Esta variável está definida como Verdadeira por padrão enquanto o filme está sendo reproduzido. Se você quiser parar a reprodução a partir do seu script, simplesmente defina esta variável como Falsa e a reprodução será interrompida.
- `exp` - Uma variável de conveniência que aponta para o objeto self.experiment
- `frame` - O número do quadro atual que está sendo exibido
- `mov_width` - A largura do filme em px
- `mov_height` - A altura do filme em px
- `paused` - *Verdadeiro* quando a reprodução está atualmente pausada, *Falso* se o filme está atualmente em execução
- `event` - Esta variável é meio especial, pois seu conteúdo depende se uma tecla ou botão do mouse foi pressionado durante o último quadro. Se este não for o caso, a variável do evento simplesmente apontará para *Nenhum*. Se uma tecla foi pressionada, o evento conterá uma tupla com na primeira posição o valor "key" e na segunda posição o valor da tecla que foi pressionada, por exemplo ("key","space"). Se um botão do mouse foi clicado, a variável do evento conterá uma tupla com na primeira posição o valor "mouse" e na segunda posição o número do botão do mouse que foi clicado, por exemplo ("mouse", 2). Na rara ocasião em que múltiplos botões ou teclas foram pressionados ao mesmo tempo durante um quadro, a variável do evento conterá uma lista desses eventos, por exemplo [("key","space"),("key", "x"),("mouse",2)]. Neste caso, você precisará percorrer esta lista em seu código e retirar todos os eventos relevantes para você.

Além dessas variáveis, você também tem as seguintes funções à sua disposição:

- `pause()` - Pausa a reprodução quando o filme está em execução, e despausa caso contrário (você poderia considerá-lo como um alternador de pausa/despausa)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/