function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy w <span class="orange">profilu gracza.</span></h2><p>W tym samouczku pokażemy Ci, na które elementy warto zwrócić <span class="green">szczególną uwagę</span>.</p><p class="comment">Jeśli chcesz <span class="green">dowiedzieć</span> się więcej o samej <span class="orange">grze,</span><br/>przedź na stronę główną i <span class="green">wybierz</span> opcję <span class="orange">„JAK GRAĆ“.</span></p>',
            },
            {
                element: '#profileuser',
                intro: '<h2>Podstawowe dane.</h2><p>Stąd możesz dowiedzieć się, do kogo należy <span class="orange">profil,</span> który właśnie oglądasz.</p><p>Na <span class="orange">zdjęciu</span> wygląda całkiem przyzwoicie, prawda? A jak radzi sobie <span class="orange">w grze?</span></p>',
                position: 'bottom',
            },
            {
                element: '#profile',
                intro: '<p>Wystarczy rzucić okiem na <span class="orange">wykres</span>, by ocenić w jakiej jest formie.',
                position: 'bottom',
            },
            {
                element: '#userstats .profile-stats',
                intro: '<p>Jeśli potrzebujesz bardziej <span class="orange">szczegółowych danych,</span> spójrz tutaj.</p>',
                position: 'top',
            },
            {
                element: '#bet-desc',
                intro: '<p>Jeśli chcesz poznać gracza od bardziej <span class="orange">osobistej strony,</span> sprawdź tę sekcję.</p>',
                position: 'bottom',
            },
            {
                element: '#bet-desc .lewa',
                intro: '<p>Przeczytaj <span class="orange">opis,</span> który sam dodał do swojego konta.</p>',
                position: 'bottom',
            },
            {
                element: '#bet-desc .prawa',
                intro: '<p>Sprawdź, czy można go znaleźć na <span class="green">portalach społecznościowych</span>.</p>',
                position: 'left',
            },
            {
                element: '#userinfo .tabs',
                intro: '<p>Możesz także <span class="green">przejrzeć</span> <span class="orange">profil gracza</span> oraz <span class="green">zapoznać się</span> z <span class="orange">historią transakcji,</span> których dokonał w ostatnim czasie.</p>',
                position: 'top',
            },
            {
                intro: '<h2>Poznajcie się!</h2><p>Jeśli chcesz <span class="green">porozmawiać</span> z tym graczem, <span class="green">skorzystaj</span> z danych kontaktowych, które udostępnił!</p><p>Polecamy Twittera! <a href="#" style="color: #ea6a2a; font-weight: 700;">@POLITIKON</a></p>',
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
