function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy w <span class="orange">POLITIKONIE</span><br/>pierwszych w Polsce zakładach politycznych!</h2><p>W tym samouczku zaprezentujemy <span class="orange">podstawowe elementy</span> gry, dostępne dla <span class="orange">niezalogowanego gracza.</span></p>'
            },
            {
                element: '.graj',
                intro: '<h2>By grać w <span class="orange">POLITIKON</span>, musisz się zalogować.</h2><p>Jeśli chcesz poznać grę <span class="green">przed rejestracją,</span> kliknij w <span class="orange">OK.</span></p>',
                position: 'left'
            },
            {
                element: '#featured',
                intro: '<h2>Oto <span class="orange">wyróżnione</span> wydarzenie.</h2><p>Przyjrzyjmy mu się dokładnie.</p>',
                position: 'bottom'
            },
            {
                element: '#featured h1',
                intro: '<h2>Tytuł wydarzenia</h2><p>Zawsze ma formę <span class="orange">pytania zamkniętego.</span> <span class="green">Trafna odpowiedź</span> na to pytanie jest kluczem do <span class="green">sukcesu</span> w <span class="orange">POLITIKONIE!</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet',
                intro: '<h2>Wybierz swoją odpowiedź</h2><p>Na pytanie z tytułu odpowiadasz tutaj. Możesz <span class="green">kupić zakłady</span> na <span class="orange">TAK</span> lub na <span class="orange">NIE.</span></p><p>Za zakłady <span class="green">płacisz</span> w <span class="orange">REPUTACH</span> - walucie <span class="orange">POLITIKONU.</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet .betYES .value',
                intro: '<p>Cena za zakład na <span class="orange">TAK</span> widoczna jest tutaj.</p>',
                position: 'top'
            },
            {
                element: '#featured #makeabet .betNO .value',
                intro: '<p>Cena za zakład na <span class="orange">NIE</span> jest natomiast tutaj.</p>',
                position: 'left'
            },
            {
                element: '#featured #makeabet',
                intro: '<p>Za każdy wygrany zakład otrzymasz <span class="orange">100</span> reputów.</p><p>Jeśli kupiłeś zakład za <span class="orange">60</span> reputów, na wygranej zyskasz dodatkowe <span class="green">40</span> reputów.</p><p class="comment">Zysk <span class="green">40rp</span> = wygrana <span class="orange">100rp</span> - cena za zakład <span class="orange">60rp</span></p>',
                position: 'bottom'
            },
            {
                element: '#betfeed',
                intro: '<p>W przypadku innych wydarzeń, <span class="orange">wszystko</span> działa tak samo!</p>',
                position: 'top'
            },
            {
                intro: '<h2>DOŁĄCZ DO GRY!</h2><p>Jesteś gotowy? <span class="green">Zarejestruj się</span> i zacznij <span class="green">stawiać na</span> <span class="orange">politkę!</span></p>'
            }
        ]
    });

    intro.start();
}
