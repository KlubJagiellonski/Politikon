function startIntro(){
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy w <span class="orange">POLITIKONIE</span><br/>pierwszych w Polsce zakładach politycznych!</h2><p class="green">W tym samouczku zaprezentujemy podstawowe elementy gry, dostępne dla niezalogowanego gracza.</p>'
            },
            {
                element: '.graj',
                intro: '<h2>By grać w <span class="orange">POLITIKON</span>, musisz się zalogować.</h2> <p class="green">Jeśli chcesz poznać grę przed rejestracją, kliknij w OK.</p>',
                position: 'left'
            },
            {
                element: '#featured',
                intro: '<h2>Oto <span class="orange">wyróżnione</span> wydarzenie.</h2><p class="green">Przyjrzyjmy mu się dokładnie.</p>',
                position: 'bottom'
            },
            {
                element: '#featured h1',
                intro: '<h2>Tytuł wydarzenia</h2><p class="green">Zawsze ma formę pytania zamkniętego. Trafna odpowiedź na to pytanie jest kluczem do sukcesu w <span class="orange">POLITIKONIE!</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet',
                intro: '<h2>Wybierz swoją odpowiedź</h2><p class="green">Na pytanie z tytułu odpowiadasz tutaj. Możesz kupić zakłady na <span class="orange">TAK</span> lub na <span class="orange">NIE.</span> Za zakłady płacisz w REPUTACH - walucie <span class="orange">POLITIKONU.</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet .betYES .value',
                intro: '<p>Cena za zakład na <span class="orange">TAK</span> widoczna jest tutaj.</p>',
                position: 'right'
            },
            {
                element: '#featured #makeabet .betNO .value',
                intro: '<p>Cena za zakład na <span class="orange">NIE</span> jest natomiast tutaj.</p>',
                position: 'left'
            },
            {
                element: '#featured #makeabet',
                intro: '<p>Za każdy wygrany zakład otrzymasz <span class="orange">100</span> reputów.</p><p>Jeśli kupiłeś zakład za <span class="orange">60</span> reputów, na wygranej zyskasz dodatkowe <span class="green">40</span> reputów.</p><p style="font-style: italic; font-size: .7em;">Zysk <span class="green">40rp</span> = wygrana <span class="orange">100rp</span> - cena za zakład <span class="orange">60rp</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet .change',
                intro: '<h2>Wskaźnik zmiany kursu</h2><p class="green">Kurs zakładów zależy od zainteresowania społeczności <span class="orange">POLITIKONU.</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet .change',
                intro: '<p>Kurs <span class="green">rośnie</span>, gdy gracze wykupują zakłady na <span class="orange">TAK</p><p><span class="green">spada</span>, gdy kupują zakłady na <span class="orange">NIE</span>.</p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet .change',
                intro: '<p>To ważne, bo w każdej chwili możesz sprzedać kupione wcześniej zakłady. Staraj się <span class="green">kupować</span> <span class="orange">taniej</span> i <span class="green">sprzedawać</span> <span class="orange">drożej.</span></p>',
                position: 'bottom'
            },
            {
                element: '#betfeed',
                intro: '<p>W przypadku innych wydarzeń, <span class="orange">wszystko</span> działa tak samo!</p>',
                position: 'top'
            },
            {
                intro: '<h2>DOŁĄCZ DO GRY!</h2><p class="green">Jesteś gotowy? Zarejestruj się i zacznij stawiać na <span class="orange">politkę!</span></p>'
            }
        ]
    });

    intro.start();
}
