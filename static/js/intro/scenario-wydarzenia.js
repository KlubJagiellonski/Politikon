function startIntro(){
        var intro = introJs();
          intro.setOptions({
            scrollToElement: false,
            showBullets: true,
            showStepNumbers: false,
            steps: [
              {
                intro: '<b>Witamy na stronie Wydarzeń.</b><br/><br/>W tym samouczku pokażemy Ci, jak przeglądać i sortować wydarzenia.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
              },
              {
                element: '#betfeed',
                intro: '<b>Wydarzenia</b><br/><br/>Tutaj znajdziesz wszystkie aktywne wydarzenia na POLITIKONIE.',
                position: 'top',
              },
              {
                element: '#betfeed .bet',
                intro: 'Przez "aktywne" rozumiemy takie, na których rozstrzygnięcie możesz postawić.<br/><br/>Wystarczy, że skorzystasz z przycisków TAK / NIE, bądź [+] / [-].',
                position: 'top'
              },
              {
                element: '#header .tabs',
                intro: '<b>Sortuj wydarzenia.</b><br/><br/>Skorzystaj z dostępnych opcji sortowania, by wyświetlić najbardziej interesujące Cię wydarzenia.',
                position: 'top',
              },
              {
                intro: "<b>Stawiaj na politykę!</b><br/><br/>Wybierz interesujące Cię wydarzenia i stawiaj na ich rozstrzygnięcie!"
              },
              {
                intro: 'Za każdy wygrany zakład, otrzymasz 100 reputów.<br/><br/>Jeśli kupiłeś zakład za 60 reputów, na wygranej zyskasz dodatkowe 40 reputów.<br/><br/><span style="font-style: italic; font-size: .7em;">(wygrana 100rp - cena za zakład 60rp = zysk 40rp)</span>'
              },
              {
                intro: "<b>Powodzenia!</b><br/><br/>Uzupełnij swój portfel zakładów. Sprzedaj je po korzystnej cenie, lub czekaj na pozytywne rozstrzygnięcie."
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
