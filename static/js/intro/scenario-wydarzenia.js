function startIntro() {
    var intro = introJs();
    intro.setOptions({
        scrollToElement: false,
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy na stronie <span class="orange">Wydarzeń.</span></h2><p>W tym samouczku pokażemy,<br/>jak <span class="green">przeglądać</span> i <span class="green">sortować</span> <span class="orange">wydarzenia.</span></p><p class="comment">Jeśli chcesz <span class="green">dowiedzieć</span> się więcej o samej <span class="orange">grze,</span><br/>przedź na stronę główną i <span class="green">wybierz</span> opcję <span class="orange">„JAK GRAĆ“.</span></p>',
            },
            {
                element: '#betfeed',
                intro: '<h2>Wydarzenia</h2><p>Tutaj znajdziesz wszystkie <span class="green">aktywne wydarzenia</span> na <span class="orange">POLITIKONIE.</span></p>',
                position: 'top',
            },
            {
                element: '#betfeed .bet',
                intro: '<p>Przez <span class="green">aktywne</span> rozumiemy takie, na których rozstrzygnięcie <span class="orange">możesz postawić.</span></p><p>Wystarczy, że skorzystasz z przycisków <span class="orange">TAK</span> / <span class="green">NIE,</span> bądź <span class="orange">[+]</span> / <span class="green">[-].</span></p>',
                position: 'top'
            },
            {
                element: '#header .tabs',
                intro: '<h2>Sortuj wydarzenia.</h2><p><span class="green">Skorzystaj</span> z dostępnych opcji <span class="orange">sortowania,</span> by <span class="green">wyświetlić</span> najbardziej <span class="orange">interesujące</span> Cię wydarzenia.</p>',
                position: 'bottom',
            },
            {
                intro: '<h2>Stawiaj na politykę!</h2><p><span class="green">Wybierz</span> <span class="orange">interesujące</span> Cię wydarzenia i <span class="green">stawiaj</span> na ich <span class="orange">rozstrzygnięcie!</span></p>'
            },
            {
                intro: '<p>Za każdy <span class="green">wygrany</span> zakład, otrzymasz <span class="orange">100</span> reputów.</p><p>Jeśli kupiłeś zakład za <span class="orange">60</span> reputów, na wygranej zyskasz dodatkowe <span class="green">40</span> reputów.</p><p class="comment">Zysk <span class="green">40rp</span> = wygrana <span class="orange">100rp</span> - cena za zakład <span class="orange">60rp</span></p>'
            },
            {
                intro: '<h2>Powodzenia!</h2><p><span class="green">Uzupełnij</span> swój <span class="orange">portfel zakładów.</span> <span class="green">Sprzedaj</span> je po <span class="orange">korzystnej cenie,</span> lub <span class="green">czekaj</span> na <span class="orange">pozytywne rozstrzygnięcie.</span></p>'
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
