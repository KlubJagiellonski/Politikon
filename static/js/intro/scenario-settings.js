function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy w <span class="orange">Ustawieniach</span></h2><p>W tym <span class="green">samouczku</span> pokażemy Ci, <span class="green">modyfikować</span> <span class="orange">Twój profil.</span></p><p class="comment">Jeśli chcesz <span class="green">dowiedzieć</span> się więcej o samej <span class="orange">grze,</span><br/>przedź na stronę główną i <span class="green">wybierz</span> opcję <span class="orange">„JAK GRAĆ“.</span></p>',
            },
            {
                element: '#settings-profile',
                intro: '<h2>Obecne ustawienia</h2><p>Tutaj znajdziesz informacje o <span class="orange">Twoim profilu:</span><br /> Twoją <span class="green">nazwę</span> w <span class="orange">POLITIKONIE,</span> <span class="green">avatar, login, datę</span> dołączenia do gry i <span class="green">dane kontaktowe.</span>',
                position: 'bottom',
            },
            {
                element: '#settings-profile .profile-avatar',
                intro: '<p>By <span class="green">zmienić</span> swoje <span class="orange">zdjęcie,</span> po prostu <span class="green">kliknij</span> na aktualny <span class="orange">avatar</span> i <span class="green">wybierz</span> nową <span class="orange">fotografię.</span></p>',
                position: 'right'
            },
            {
                element: '#userinfo .tabs',
                intro: '<p>Ustawienia zostały podzielone na <span class="green">dwie sekcje.</span></p><p><span class="green">Pierwsza</span> zawiera ustawienia związane z <span class="orange">Twoim profilem</span> w grze. <span class="green">Druga</span> - ustawienia pozwalające uzyskać dostęp do <span class="orange">Twojego konta.</span></p>',
                position: 'right'
            },
            {
                element: '#loadmore .btn',
                intro: '<p>Po wprowadzeniu zmian, <span class="green">zapisz</span> je klikając w ten <span class="orange">przycisk.</span></p>',
                position: 'top'
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
