# תוסף נגן מדיה מבוסס MoviePy

זכויות יוצרים 2010-2016 לדניאל שריי (<d.schreij@vu.nl>)

תוסף media_player_mpy מוסיף אפשרויות ניגון וידאו ל-[בניית הניסוי של OpenSesame][opensesame]. תוסף זה משתמש ב[Moviepy][mpy_home] כבסיס שלו. הוא אמור להיות מסוגל להכיל מרבית הפורמטים המודרניים של וידאו ושמע, למרות שחשוב שהתזרים שלהם לא יהיו מושחתים. אם קובץ לא מנוגן כראוי, ראו אם אתם מוצאים גרסה טובה יותר, או מנסים לקדוד מחדש אותו לפורמט שונה.

הניגון הטוב ביותר ניתן להשגתו על ידי שימוש במנגנים שמנועים באמצעות Psychopy או Expyriment. יתכן שהביצועים לא מרשימים כאשר משתמשים במנגנים ישנים והווידאו מתנגן ברזולוציה או במהירות תמונות גבוהה.

## הגדרות התוסף
התוסף מציע את אפשרויות התצורה הבאות מהממשק הגרפי:

- *קובץ וידאו* - קובץ הווידאו שימוגן. שדה זה מאפשר שימוש בתחבירים משתנים כמו [video_file], שתוכלו להגדיר את ערכם בלולאות.
- *נגן אודיו* - מציין אם לנגן את הווידאו עם קול או בשקט (משתק).
- *התאמה של הווידאו למסך* - מציין האם לנגן את הוידאו בגודל המקורי שלו, או אם יש לסדר אותו לגודל החלון/המסך. תהליך התוקף משמר את יחס ההתאמה של הווידאו.
- *לולאה* - מציין אם לחזור על הניגון של הווידאו, כלומר שהניגון יתחיל שוב מההתחלה ברגע שנגמרת ההקרנה של הווידאו.
- *משך* - קובע כמה זמן הוידאו צריך להיות מוצג. מצפה לערך בשניות, 'keypress' או 'mouseclick'. אם יש לו אחד מערכים אלו, הניגון יפסיק כאשר נלחץ מקש או נלחצת כפתור העכבר.

## קוד Python מותאם אישית לטיפול באירועים של לחיצת מקשים ולחיצת עכבר
התוסף מציע גם פונקציונליות המאפשרת להריץ קוד טיפול באירועים מותאם אישית אחרי כל תמונה, או אחרי לחיצה של מקש או העכבר (שים לב שהרצת קוד אחרי כל תמונה מבטלה את אופציית 'keypress' בשדה המשך; על לחיצת Escape אבל עדיין מאזינים). זה שימושי, לדוגמה, אם מישהו רוצה לספור כמה פעמים מתמ Teilnehmer drückt die Leertaste (oder eine andere Taste) während der Vorstellungszeit des Films.

Es gibt ein paar Variablen, auf die Sie in dem Skript, das Sie hier eingeben, zugreifen können:

- `המשך_ניגון` (אמת או שקר) - קובע אם הווידאו צריך להמשיך להנוגן. משתנה זה מוגדר לאמת כברירת מחדל כאשר הווידאו מנוגן. אם אתם רוצים לעצור את הניגון מהתסריט שלכם, פשוט שפעלו למשתנה לשקר והניגון ייפסק.
- `exp` - משתנה שתופקד כ-link לקוביית הניסוי.
- `frame` - מספר התמונה הנוכחית שמוצגת
- `mov_width` - רוחב הווידאו בפיקסלים
- `mov_height` - גובה הווידאו בפיקסלים
- `מושהה` - *אמת* כאשר הניגון כעת בהשהיה, *שקר* אם הווידאו מוצג כעת
- `event` - משתנה זה הוא מיוחד מינה שהתוכן שלו תלוי אם מקש או כפתור העכבר לחצו בתמונה האחרונה. אם זה לא המקרה, משתנה event פשוט יצביע ל-*None*. אם מקש נלחץ, האירוע יכלול tuple עם "מקש" כערך הראשון והערך של המקש שנלחץ, למשל ("מקש","space"). אם כפתור העכבר לחצו, משתנה event יכלול tuple עם "עכבר" כערך הראשון ואת מספר כפתור העכבר שנלחץ, לדוגמה ("עכבר", 2). ברגעים נדירים שבהם הוקשו מספר מקשים או כפתורים בו זמנית במהלך תמונה, משתנה event יכלול רשימה של אירועים אלו, לדוגמה [("מקש","רווח"), ("מקש", "x"), ("עכבר",2)]. במקרה זה, תצטרך לחצות רשימה זו בתסריט שלך ולשלוף את כל האירועים הרלוונטיים לך.

תגיד למשתנים אלה יש לכם גם את הפונקציות הבאות ברשותכם:

- `pause()` - משהה את הניגון כאשר הווידאו מוצג, ומשחרר אותו אחרת (אתה יכול לראות אותו כסוויץ' של השהיה/חילוף)

[opensesame]: http://www.cogsci.nl/opensesame
[mpy_home]: http://zulko.github.io/moviepy/