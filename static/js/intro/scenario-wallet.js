function startIntro(){
        var intro = introJs();
          intro.setOptions({
            showBullets: true,
            showStepNumbers: false,
            steps: [
              {
                intro: '<b>Witamy w Twoim Portfelu!</b><br/><br/>W tym samouczku pokażemy Ci, jak zarządzać zawartością Twojego portfela.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
              },
              {
                element: '#userstats',
                intro: '<b>Twoje wyniki.</b><br/><br/>Tutaj znajdziesz informacje nt. zawartości Twojego portfela, posiadanych reputów i pozycji w rankingu.',
        position: 'bottom',
              },
              {
                element: '#userstats .wallet',
                intro: 'Zwróć szczególną uwagę na statystyki portfela. Ile zakładów zgromadziłeś? Czy ich wartość rośnie? Czy może spada i najwyższy czas sprzedać źle obstawione wydarzenia?',
        position: 'right',
              },
              {
                element: '#userinfo .tabs',
                intro: 'Wydarzenia, które obstawiłeś, tworzą zawartość Twojego portfela. Przyjrzyjmy się jej uważnie. <br/><br/><b>Przejdź na zakładkę ZAWARTOŚĆ PORTFELA</b> przed przejściem dalej.',
        position: 'bottom',
              },
              {
                element: '#zawartoscportfela .betinwallet',
                intro: 'W portfelu widzisz wszystkie zakupione i nierozstrzygnięte jeszcze zakłady.',
        position: 'right',
              },
              {
                element: '#zawartoscportfela .betinwallet .status p',
                intro: 'Pod tytułem wydarzenia, znajdziesz informację o zakupionych zakładach - ich rodzaju (TAK / NIE), liczbie, oraz średniej cenie, jaką zapłaciłeś za zakład.',
        position: 'right',
              },
              {
                element: '#zawartoscportfela .betinwallet .status p .why',
                intro: 'Pomocna może również okazać się informacja o aktualnej cenie. Dzięki temu wiesz, czy nie zapłaciłeś za dużo i czy opłaca się dokupić dodatkowe zakłady.',
        position: 'right',
              },
              {
                element: '#zawartoscportfela .betinwallet',
                intro: 'Gdy wskażesz zakład kursorem, zobaczysz trzy dodatkowe informacje. Od lewej:<br/>- łączny koszt zakładów,<br/>- możliwą wygraną<br/>- potencjalny zysk',
        position: 'right',
              },
              {
                element: '#zawartoscportfela .betinwallet',
                intro: 'By kupić lub sprzedać zakłady z portfela, wybierz interesujące Cię wydarzenie i kliknij w nie. Na stronie wydarzenia będziesz mógł zmodyfikować swoje zakłady.',
        position: 'right',
              },
              {
                element: '#userinfo .tabs',
                intro: 'Sprawdźmy teraz powiadomienia o Twoich wynikach.<br/><br/><b>Przejdź na zakładkę POWIADOMIENIA O WYNIKACH</b> przed przejściem dalej.',
        position: 'bottom',
              },
              {
                element: '#powiadomieniaowynikach .notinwallet',
                intro: 'Tak wygląda przykładowa informacja o rozstrzygniętym zakładzie.<br/><br/>Jej lewa część wygląda analogicznie jak w zakładów w portfelu. Skupmy się zatem na elementach z prawej strony.',
        position: 'top',
              },
              {
                element: '#powiadomieniaowynikach .status-change',
                intro: 'W tym miejscu dowiesz się, jak zmienił się Twój stan posiadania po rozstrzygnięciu wydarzenia. Czy zakłady przyniosły Ci zysk, czy stratę?',
        position: 'top',
              },
              {
                element: '#powiadomieniaowynikach .status-change p',
                intro: 'Zwróć uwagę na dodatkowe informacje pod wynikiem.',
        position: 'bottom',
              },
              {
                element: '#powiadomieniaowynikach .status-change p .invested',
                intro: 'Ta pole informuje o liczbie reputów, które wydałeś na kupno zakładów',
        position: 'bottom',
              },
              {
                element: '#powiadomieniaowynikach .status-change p .won',
                intro: 'Natomiast to pole wskazuje wysokość Twojej wygranej.',
        position: 'bottom',
              },
              {
                element: '#powiadomieniaowynikach .status-change div',
                intro: 'Zmiana portfela to różnica pomiędzy dwiema poprzednimi wartościami.',
        position: 'bottom',
              },
              {
                element: '#powiadomieniaowynikach .status-explanation',
                intro: 'Tutaj znajdziesz skrócone uzasadnienie rozstrzygnięcia wydarzenia na TAK bądź na NIE. By poznać pełne uzasadnienie, po prostu kliknij w to powiadomienie.',
        position: 'left',
              },
              {
                element: '#userinfo .tabs',
                intro: 'Spójrzmy teraz na transakcje zrealizowane na Twoim koncie.<br/><br/><b>Przejdź na zakładkę HISTORIA TRANSAKCJI</b> przed przejściem dalej.',
        position: 'bottom',
              },
              {
                element: '#historiatransakcji',
                intro: 'Historia transakcji jest trochę jak wyciąg z banku. Znajdziesz tutaj wszyskie operacje, które wpłynęły na stan Twojego konta.',
        position: 'top',
              },
              {
                element: '#historiatransakcji .history-event .lewa',
                intro: 'Jest tutaj nazwa transakcji.',
        position: 'bottom',
              },
              {
                element: '#historiatransakcji .history-event .history-action',
                intro: 'Jest rodzaj transakcji.',
        position: 'bottom',
              },
              {
                element: '#historiatransakcji .history-event .reputy-change',
                intro: 'Jej wpływ na stan konta.',
        position: 'bottom',
              },
              {
                element: '#historiatransakcji .history-event .event-date',
                intro: 'Oraz data realizacji.',
        position: 'bottom',
              },
              {
                element: '#historiatransakcji .history-event',
                intro: 'Wszystkie transakcje zawarte w tej sekcji składają się na obecny stan Twojego konta.<br/><br/>Jeśli chcesz sprawdzić, co przyniosło Ci zysk, a co stratę - przejrzyj poniższe wpisy.',
        position: 'bottom',
              },
              {
                intro: '<b>To wszystko!</b><br/><br/>Teraz już wiesz, jak zarządzać swoim portfelem. Dzięki temu możesz optymalizować swoje zakłady tak, by maksymalizować zysk i minimalozować ryzyko straty. Powodzenia! :-)',
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
