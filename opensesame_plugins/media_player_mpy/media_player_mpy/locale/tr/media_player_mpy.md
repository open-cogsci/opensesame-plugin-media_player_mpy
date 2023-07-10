# MoviePy tabanlı Medya Oynatıcı eklentisi

Telif hakkı 2010-2016 Daniel Schreij (<d.schreij@vu.nl>)

media_player_mpy eklentisi, video oynatma özelliklerini [OpenSesame deney oluşturucu][opensesame] programına ekler. Bu eklenti [Moviepy][mpy_home] programını temel alır. En modern video ve ses formatlarını işleyebilir, ancak önemlidir ki akışlar bozuk olmamalıdır. Eğer bir dosya çalışmıyormuş gibi görünüyorsa, daha iyi bir sürümünü bulmaya çalışın veya farklı bir formata dönüştürmeyi deneyin.

En iyi oynatma, donanım hızlandırmalı Psychopy veya Expyriment arka ucu kullanılarak elde edilir. Eski sürüm kullanıldığında ve film yüksek çözünürlükte veya çerçeve hızında olduğunda performans yetersiz olabilir.

## Eklenti ayarları
Eklenti, Kullanıcı Arayüzünden aşağıdaki yapılandırma seçeneklerini sunar:

- *Video dosyası* - Oynatılacak video dosyası. Bu alan, değerini döngü öğelerinde belirleyebileceğiniz [video_dosyası] gibi değişken notasyonlarına izin verir.
- *Ses oynat* - Videonun sesli mi yoksa sessiz mi (susturulmuş) oynatılacağını belirtir.
- *Videoyu ekrana sığdır* - Videonun orijinal boyutunda mı, yoksa pencerenin/ekranın boyutuna sığacak şekilde ölçeklendirilmiş mi oynatılması gerektiğini belirtir. Ölçeklendirme işlemi filmin orijinal en boy oranını korur.
- *Döngü* - Videonun döngü içinde mi oynatılması gerektiğini belirtir, yani film bitince baştan başlar.
- *Süre* - Filmin ne kadar süreyle gösterilmesi gerektiğini belirtir. 'keypress' veya 'mouseclick' değerlerini veya saniye cinsinden bir değeri kabul eder. Son iki değerden birine sahipse, bir tuşa basıldığında veya fare düğmesi tıklanıldığında oynatma durur.

## Tuş basma ve fare tıklama olaylarını işlemek için özel Python kodu
Bu eklenti, her çerçevenin ardından veya bir tuşa basıldığında veya fareye tıkladıktan sonra, özel olay işleme kodunun uygulanması işlevselliğini de sunar (Her çerçeve sonrası kodun çalıştırılması, 'keypress' opsiyonunu süre alanında geçersiz kılar; Ancak Escape tuşuna hala dikkat edilir). Bu, örneğin, bir katılımcının filmin gösterime girdiği süre boyunca bir tuşa (veya başka bir tuşa) kaç kez bastığını saymak isterseniz kullanışlıdır.

Burada girilen script içinde birkaç değişken erişilebilirdir:

- `continue_playback` (True veya False) - Filmin oynatılmaya devam edip etmeyeceğini belirler. Bu değişken, film oynatılırken varsayılan olarak True olarak ayarlanır. Scriptinizden oynatmayı durdurmak isterseniz, bu değişkeni sadece False olarak ayarlayın ve oynatma durur.
- `exp` - self.experiment nesnesine işaret eden kullanışlı bir değişken
- `frame` - Halihazırda gösterilen mevcut çerçevenin numarası
- `mov_width` - Filmin px cinsinden genişliği
- `mov_height` - Filmin px cinsinden yüksekliği
- `paused` - Oynatma şu anda durdurulduğunda *True*, film şu anda oynatılıyorsa *False*
- `event` - Bu değişken biraz özeldir, çünkü içerikleri, son çerçeve sırasında bir tuşun veya fare düğmesinin basılıp basılmadığına bağlıdır. Bu durum söz konusu değilse, event değişkeni basitçe *None* değerine işaret eder. Eğer bir tuşa basıldıysa, event değişkeni öncelikle "key" değerini ve ikincil olarak da basılan tuşun değerini içeren bir çift bilgi içerir, örneğin ("key","space"). Eğer bir fare düğmesine tıklandıysa, event değişkeni öncelikle "mouse" değerini ve ikincil olarak tıklanan fare düğmesinin numarasını içeren bir çift bilgi içerir, örneğin ("mouse", 2). Eğer aynı çerçeve sırasında birden fazla düğmeye veya tuşa basılırsa, event değişkeni bu olayların bir listesini içerir, örneğin [("key","space"),("key", "x"),("mouse",2)]. Bu durumda, kodunuzda bu listeyi gezinmeniz ve size ilgili tüm olayları çıkartmanız gerekecektir.

Bu değişkenlere ek olarak, aşağıdaki fonksiyonlarda kullanımınıza sunulmuştur:

- `pause()` - Film çalışırken oynatmayı durdurur ve aksi halde duraklatmayı iptal eder (bunu duraklatma/devam ettirme anahtarı olarak düşünebilirsiniz)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/