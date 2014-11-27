function startIntro(){
        var intro = introJs();
          intro.setOptions({
            showBullets: false,
            showStepNumbers: false,
            steps: [
              {
                intro: '<b>Witamy w profilu gracza.</b><br/><br/>W tym samouczku pokażemy Ci, na które elementy warto zwrócić szczególną uwagę.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
              },
              {
                element: '#profileuser',
                intro: '<b>Podstawowe dane.</b><br/><br/>Stąd możesz dowiedzieć się, do kogo należy profil, który właśnie oglądasz.<br/><br/>Na zdjęciu wygląda całkiem przyzwoicie, prawda? A jak radzi sobie w grze?',
		position: 'top',
              },
              {
                element: '#profile',
                intro: 'Wystarczy rzucić okiem na wykres, by ocenić w jakiej jest formie.',
		position: 'bottom',
              },
              {
                element: '#userstats .profile-stats',
                intro: 'Jeśli potrzebujesz bardziej szczegółowych danych, spójrz tutaj.',
		position: 'top',
              },
              {
                element: '#bet-desc',
                intro: 'Jeśli chcesz poznać gracza od bardziej osobistej strony, sprawdź tę sekcję.',
		position: 'bottom',
              },
              {
                element: '#bet-desc .lewa',
                intro: 'Przeczytaj opis, który sam dodał do swojego konta.',
		position: 'right',
              },
              {
                element: '#bet-desc .prawa',
                intro: 'Sprawdź, czy można go znaleźć na portalach społecznościowych.',
		position: 'left',
              },
              {
                element: '#userinfo .tabs',
                intro: 'Możesz także przejrzeć profil gracza oraz zapoznać się z historią transakcji, których dokonał w ostatnim czasie.<br/><br/>Informacje w tej sekcji aktualizują się z 24-godzoinnym opóźnieniem.<br/><br/><span style="font-style: italic; font-size: .7em;">...a to oznacza, że nie można oszukiwać ;-)</span>',
		position: 'top',
              },
              {
                intro: '<b>Poznajcie się!</b><br/><br/>Jeśli chcesz porozmawiać z tym graczem, skorzystaj z danych kontaktowych, które udostępnił!<br/><br/>P.S. Polecamy Twittera!<br/><a href="#" style="color: #ea6a2a; font-weight: 700;">@POLITIKON</a> :-)',
              }
            ]
          });

          intro.start();
      }
      
      
//poprawia pozycje tooltipow na podstronach
$(document).ready(function() {
    var s = $("#maintop");
    var pagestatus = $("#POLITIKON");
    var pos = s.position();                    
    $(window).scroll(function() {
        var windowpos = $(window).scrollTop();
        if (windowpos >= 30) { // wysokosc, po ktorej zaczyna sie scroll
                pagestatus.addClass("body-scrolled-subpage");
        } else {
                pagestatus.removeClass("body-scrolled-subpage");
        }
    });
});