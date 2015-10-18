function startIntro(){
        var intro = introJs();
          intro.setOptions({
            showBullets: false,
            showStepNumbers: false,
            steps: [
              {
                intro: '<b>Witamy na stronie szczegółów wydarzenia.</b><br/><br/>W tym samouczku pokażemy Ci, jak zapoznać się ze szczegółami wydarzenia.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
              },
              {
                element: '#header h1',
                intro: '<b>Tytuł wydarzenia</b><br/><br/>Zawsze w formie pytania zamkniętego. Możesz odpowiedzieć na nie, wykupując zakłady na TAK lub NIE.',
        position: 'BOTTOM',
              },
              {
                element: '#bet-details',
                intro: '<b>Szczegóły wydarzenia.</b><br/><br/>Sprawdź, jak głosowali inni, jaki jest aktualny kurs, oraz ile kosztują poszczególne zakłady.',
        position: 'top'
              },
              {
                element: '#makeabet',
                intro: 'Zakłady kupujesz za pomocą przycisków TAK / NIE, bądź - jeśli kupiłeś już zakład - zmieniasz ich liczbę przyciskami [+] / [-]. ',
        position: 'top',
              },
              {
                element: '#bet-desc .lewa',
                intro: '<b>Opis wydarzenia</b><br/><br/>Tutaj znajdziesz szczegółowy opis wydarzenia i warunki rozstrzygnięcia zakładów.<br/><br/>Po zakończeniu wydarzenia, pojawi się tutaj także pełne uzasadnienie podjętego rozstrzygnięcia.',
        position: 'right',
              },
              {
                element: '#bet-desc .rss-related',
                intro: '<b>Informacje w mediach</b><br/><br/>Przed obstawieniem wydarzenia, warto zasięgnąć informacji z nim związanych. W tym miejscu dowiesz się, co na jego temat piszą w mediach.',
        position: 'left',
              },
              {
                element: '#comments',
                intro: 'Możesz również poznać opinie innych graczy o wydarzeniu, a nawet zapytać ich, dlaczego kupili zakłady na TAK bądź na NIE.',
        position: 'top',
              },
              {
                element: '#betfeed',
                intro: '<b>Obstawiaj podobne wydarzenia!</b><br/><br/>Jeśli zainteresowało Cię to wydarzenie, sprawdź związane z nim zakłady. Jeśli jesteś pewny swojej decyzji, warto obstawić podobne wydarzenia i wygrać więcej za jednym razem!',
        position: 'bottom',
              },
              {
                intro: "<b>Stawiaj na politykę!</b><br/><br/>Wiesz już, jaką opcję obstawisz? Nie zwlekaj i kup zakłady teraz, zanim podrożeją!"
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
