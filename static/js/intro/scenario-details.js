function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy na stronie <span class="orange">szczegółów</span> wydarzenia.</h2><p>W tym samouczku <span class="green">pokażemy</span> Ci, jak zapoznać się ze <span class="orange">szczegółami wydarzenia.</span></p><p class="comment">Jeśli chcesz <span class="green">dowiedzieć</span> się więcej o samej <span class="orange">grze,</span><br/>przedź na stronę główną i <span class="green">wybierz</span> opcję <span class="orange">„JAK GRAĆ“.</span></p>',
            },
            {
                element: '#header h1',
                intro: '<h2>Tytuł wydarzenia</h2><p><span class="green">Zawsze</span> w formie <span class="orange">pytania zamkniętego.</span> Możesz <span class="green">odpowiedzieć</span> na nie, wykupując zakłady na <span class="orange">TAK</span> lub <span class="orange">NIE.</span></p>',
                position: 'BOTTOM',
            },
            {
                element: '#bet-details',
                intro: '<h2>Szczegóły wyzdarzenia</h2><p>Sprawdź, <span class="green">jak</span> <span class="orange">głosowali inni,</span> <span class="green">jaki</span> jest <span class="orange">aktualny kurs</span>, oraz <span class="green">ile kosztują</span> poszczególne <span class="orange">zakłady.</span></p>',
                position: 'top'
            },
            {
                element: '#makeabet',
                intro: '<p>Zakłady kupujesz za pomocą przycisków <span class="orange">TAK</span> / <span class="green">NIE,</span> bądź - jeśli kupiłeś już zakład - zmieniasz ich liczbę przyciskami <span class="orange">[+]</span> / <span class="green">[-].</span></p>',
                position: 'top',
            },
            {
                element: '#bet-desc .lewa',
                intro: '<h2>Opis wydarzenia</h2><p>Tutaj znajdziesz szczegółowy <span class="green">opis</span> <span class="orange">wydarzenia</span> i <span class="green">warunki rozstrzygnięcia</span> <span class="orange">zakładów.</span><br/><br/>Po zakończeniu wydarzenia, pojawi się tutaj także <span class="green">pełne uzasadnienie</span> podjętego <span class="orange">rozstrzygnięcia.</span></p>',
                position: 'top',
            },
            {
                element: '#bet-desc .rss-related',
                intro: '<h2>Informacje w mediach</h2><a>Przed obstawieniem wydarzenia, <span class="green">warto</span> <span class="orange">zasięgnąć informacji</span> z nim związanych. W tym miejscu dowiesz się, <span class="green">co</span> na jego temat <span class="orange">piszą w mediach.</span></p>',
                position: 'left',
            },
            {
                element: '#comments',
                intro: '<p>Możesz również <span class="green">poznać</span> <span class="orange">opinie innych graczy</span> o wydarzeniu, a nawet zapytać ich, <span class="green">dlaczego</span> kupili zakłady na <span class="orange">TAK</span> bądź na <span class="orange">NIE.</span></p>',
                position: 'top',
            },
            {
                element: '#betfeed',
                intro: '<h2>Obstawiaj <span class="orange">podobne</span> wydarzenia!</h2><p>Jeśli zainteresowało Cię to wydarzenie, <span class="green">sprawdź</span> <span class="orange">związane z nim zakłady.</span> Jeśli jesteś pewny swojej decyzji, warto obstawić <span class="orange">podobne wydarzenia</span> i wygrać więcej za jednym razem!</p>',
                position: 'bottom',
            },
            {
                intro: '<h2>Stawiaj na politykę!</h2><p>Wiesz już, jaką opcję obstawisz? Nie zwlekaj i <span class="green">kup zakłady</span> teraz, <span class="orange">zanim podrożeją!</span></p>'
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
