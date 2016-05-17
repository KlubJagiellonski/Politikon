function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy na stronie <span class="orange">Rankingu.</span></h2><p>W tym samouczku pokażemy Ci, jak <span class="green">zapoznać się</span> z <span class="orange">wynikami rywalizacji</span> na <span class="orange">POLITIKONIE.</span> Dowiesz się m.in. kto najlepiej zna się na politce.</p><p class="comment">Jeśli chcesz <span class="green">dowiedzieć</span> się więcej o samej <span class="orange">grze,</span><br/>przedź na stronę główną i <span class="green">wybierz</span> opcję <span class="orange">„JAK GRAĆ“.</span></p>',
            },
            {
                element: '#userinfo .zakladki-content',
                intro: '<h2>Pełne zestawienie.</h2><p><span class="orange">Miejsca</span> poszczególnych graczy możesz <span class="green">sprawdzić</span> tutaj. Jeśli chcesz <span class="green">dowiedzieć się</span> o nich <span class="orange">więcej</span> - po prostu <span class="green">kliknij</span> w wybranego <span class="orange">gracza,</span> by wyświetlić jego <span class="orange">profil.</span></p>',
                position: 'top',
            },
            {
                element: '#userinfo .tabs',
                intro: '<p>Możesz zmieniać <span class="green">wyświetlane rankingi</span> za pomocą tych przycisków.</p><p><span class="orange">Przełącz widok na ranking 7-dniowy</span> zanim przejdziemy dalej!</p>',
                position: 'bottom',
            },
            {
                element: '.ranking-event',
                intro: '<p>Ten gracz radzi <span class="green">sobie wyśmienicie!</span> Jest na pierwszej pozycji!</p><p><span class="orange">Chcesz go pokonać?</span> Nie ma sprawy!<br/>Ale zanim zdradzimy Ci, jak to zrobić...</p>',
                position: 'bottom',
            },
            {
                element: '.graj',
                intro: '<h2>Dołącz do gry!</h2><p><span class="green">Zaloguj się,</span> lub <span class="green">utwórz nowe konto</span> w <span class="orange">POLITIKONIE.</span> Zajmie Ci to zaledwie parę sekund!.',
                position: 'left',
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
