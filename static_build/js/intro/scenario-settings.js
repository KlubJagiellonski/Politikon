function startIntro(){
        var intro = introJs();
          intro.setOptions({
            showBullets: false,
            showStepNumbers: false,
            steps: [
              {
                intro: '<b>Witamy w Ustawieniach</b><br/><br/>W tym samouczku pokażemy Ci, modyfikować Twój profil.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
              },
              {
                element: '#settings-profile',
                intro: '<b>Obecne ustawienia</b><br/><br/>Tutaj znajdziesz informacje o Twoim profilu: Twoją nazwę w POLITIKONIE, avatar, login, datę dołącznie do gry i dane kontaktowe.',
		position: 'top',
              },
              {
                element: '#settings-profile .profile-avatar',
                intro: 'By zmienić swoje zdjęcie, po prostu kliknij na aktualny avatar i wybierz nową fotografię.',
		position: 'right'
              },
              {
                element: '#userinfo .tabs',
                intro: 'Ustawienia zostały podzielone na dwie sekcje.<br/><br/>Pierwsza zawiera ustawienia związane z Twoim profilem w grze, druga - ustawienia pozwalające uzyskać dostęp do Twojego konta.',
		position: 'right'
              },
              {
                element: '#loadmore .btn',
                intro: 'Po wprowadzeniu zmian, zapisz je klikając w ten przycisk.',
		position: 'top'
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