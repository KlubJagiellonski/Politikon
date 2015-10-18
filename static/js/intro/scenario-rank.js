function startIntro(){
        var intro = introJs();
          intro.setOptions({
            showBullets: false,
            showStepNumbers: false,
            steps: [
              {
                intro: '<b>Witamy na stronie Rankingu.</b><br/><br/>W tym samouczku pokażemy Ci, jak zapoznać się z wynikami rywalizacji na POLITIKONIE. Dowiesz się m.in. kto najlepiej zna się na politce.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
              },
              {
                element: '#userinfo .zakladki-content',
                intro: '<b>Pełne zestawienie.</b><br/><br/>Miejsca poszczególnych graczy możesz sprawdzić tutaj. Jeśli chcesz dowiedzieć się o nich więcej - po prostu kliknij w wybranego gracza, by wyświetlić jego profil.',
        position: 'left',
              },
              {
                element: '#userinfo .tabs',
                intro: 'Możesz zmieniać wyświetlane rankingi za pomocą tych przycisków.<br/><br/><b>Przełącz widok na ranking 7-dniowy</b> zanim przejdziemy dalej!',
        position: 'bottom',
              },
              {
                element: '.ranking-event',
                intro: '<b>Ten gracz radzi sobie wyśmienicie!</b> Jest na pierwszej pozycji!<br/><br/><b>Chcesz go pokonać?</b> Nie ma sprawy! Ale zanim zdradzimy Ci, jak to zrobić...',
        position: 'bottom',
              },
              {
                element: '.graj',
                intro: '<b>Dołącz do gry!</b><br/><br/>Zaloguj się, lub utwórz nowe konto w POLITIKONIE. Zajmie Ci to zaledwie parę sekund!.',
        position: 'bottom',
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
