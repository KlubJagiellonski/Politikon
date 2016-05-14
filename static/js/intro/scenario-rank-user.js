function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<b>Witamy na stronie Rankingu.</b><br/><br/>W tym samouczku pokażemy Ci, jak zapoznać się z wynikami rywalizacji na POLITIKONIE. Dowiesz się m.in. kto najlepiej zna się na politce.<br/><br/> <span style="font-style: italic; font-size: .7em;">Jeśli chcesz dowiedzieć się więcej o samej grze, przedź na stronę główną i wybierz opcję "JAK GRAĆ".</span>',
            },
            {
                element: '#userstats',
                intro: '<b>Twoje wyniki.</b><br/><br/>Tutaj możesz poznać swoje aktualne wyniki - wartość portfela, liczbę wolnych reputów i reputację w POLITIKONIE. Możesz użyć tych danych, by porównać się z innymi graczami.',
                position: 'bottom'
            },
            {
                element: '#userstats .position',
                intro: '<b>Twoja pozycja w rankingu.</b><br/><br/>Sprawdź, które miejsca w rankingu zajmujesz. Jak poszło Ci w tym tygodniu, a jak w całym miesiącu? Które miejsce zajmujesz w rankingu ogólnym?',
                position: 'right'
            },
            {
                element: '#ranking',
                intro: 'Swoją pozycję możesz dosłownie <b>zobaczyć!</b> Wystarczy rzut oka na ten wykres. ',
                position: 'bottom',
            },
            {
                element: '#userinfo .zakladki-content',
                intro: '<b>Pełne zestawienie.</b><br/><br/>Miejsca poszczególnych graczy możesz sprawdzić tutaj. Jeśli chcesz dowiedzieć się o nich więcej - po prostu kliknij w wybranego gracza, by wyświetlić jego profil.',
                position: 'top',
            },
            {
                element: '#userinfo .tabs',
                intro: 'Możesz zmieniać wyświetlane rankingi za pomocą tych przycisków.<br/><br/><b>Przełącz widok na ranking 7-dniowy</b> zanim przejdziemy dalej!',
                position: 'top',
            },
            {
                element: '.ranking-event',
                intro: '<b>Ten gracz radzi sobie wyśmienicie!</b> Jest na pierwszej pozycji!<br/><br/><b>Chcesz go pokonać?</b> Nie ma sprawy! Twoje miejsce w rankingu zależy od trzech wskaźników:<br/>- wartości portfela,<br/>- liczbie wolnych reputów<br/>- reputacji w POLITIKONIE<br/><br/>Dbaj o nie, a niedługo będziesz czarnym koniem tych rozgrywek!',
                position: 'top',
            },
            {
                element: '.rank-wallet',
                intro: '<b>Wartość portfela</b><br/><br/>To wskaźnik wyrażający łączną wartość nabytych (i ciągle nierozstrzygniętych) zakładów oraz wolnych reputów posiadanych przez gracza.',
                position: 'bottom',
            },
            {
                element: '.rank-freereputy',
                intro: '<b>Wolne reputy</b><br/><br/>To reputy, krórych nie zainwestowałeś jeszcze w żadne zakłady. Możesz przeznaczyć je na obstawianie wydarzeń.',
                position: 'bottom',
            },
            {
                element: '.rank-reputation',
                intro: '<b>Reputacja</b><br/><br/>To wskaźnik samodzielność gracza. Im więcej reputów wygrałeś na zakładach, a mniej otrzymałeś od systemu - tym wskaźnik reputacji będzie większy.',
                position: 'bottom',
            },
            {
                intro: '<b>Zadowolony ze swojego miejsca w rankingu?</b><br/><br/>Jeśli tak - gratulujemy! Jeśli nie - zajrzyj na profile najlepszych graczy i sprawdź jak osiągnęli sukces. Może zainspirują Cię do obstawienia kilku wydarzeń ;-)'
            }
        ]
    });

    intro.start();
}


//poprawia pozycje tooltipow na podstronach
$(document).ready(function () {
    var s = $("#maintop");
    var pagestatus = $("#POLITIKON");
    var pos = s.position();
    $(window).scroll(function () {
        var windowpos = $(window).scrollTop();
        if (windowpos >= 30) { // wysokosc, po ktorej zaczyna sie scroll
            pagestatus.addClass("body-scrolled-subpage");
        } else {
            pagestatus.removeClass("body-scrolled-subpage");
        }
    });
});
