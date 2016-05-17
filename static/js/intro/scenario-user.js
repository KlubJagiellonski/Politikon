function startIntro() {
    var intro = introJs();
    intro.setOptions({
        showBullets: true,
        showStepNumbers: false,
        steps: [
            {
                intro: '<h2>Witamy w <span class="orange">POLITIKONIE</span><br/>pierwszych w Polsce zakładach politycznych!</h2><p>W tym samouczku <span class="green">poznasz</span> podstawowe <span class="orange">elementy gry.</span></p>'
            },
            {
                intro: '<span>Jesteś <span class="green">zalogowany,</span> więc na początek przyjrzymy się Twojemu <span class="orange">panelowi użytkownika.</span></p>'
            },
            {
                element: '.userdata',
                intro: '<h2>Panel użytkownika.</h2><p>Tutaj <span class="green">sprawdzisz</span> swoje <span class="orange">wyniki.</span> <span class="green">Poznasz</span> wartość swojego <span class="orange">portfela</span>, <span class="orange">stan posiadania</span> i <span class="orange">reputację</span> w grze.</p>',
                position: 'left'
            },
            {
                element: '.userdata .wallet',
                intro: '<h2>Powiadomienia o wynikach.</h2><p>Gdy <span class="orange">wydarzenia,</span> które <span class="green">obstawiłeś</span> zostają <span class="orange">rozstrzygnięte,</span> <span class="green">informacja</span> o tym pojawi się <span class="orange">w tym miejscu.</span></p><p class="comment">Wystarczy <span class="green">kliknąć,</span> by przejrzeć <span class="orange">szczegóły.</span></p>',
                position: 'left'
            },
            {
                element: '.graj',
                intro: '<h2>Twoje konto.</h2><p>Po <span class="green">kliknięciu</span> w <span class="orange">avatar</span>, możesz <span class="green">zarządzać</span> swoim <span class="orange">profilem.</span> <span class="green">Zmienić</span> swoje <span class="orange">zdjęcie,</span> <span class="green">dodać</span> <span class="orange">konta społecznościowe</span> i <span class="green">uzupełnić</span> informacje <span class="orange">o sobie.</span>',
                position: 'left'
            },
            {
                intro: '<p>W porządku, ale pewnie zastanawiasz się, jak właściwie grać w <span class="orange">POLITIKON?</span> Rzućmy okiem na <span class="green">wydarzenia!</span></p>'
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
                position: 'right'
            },
            {
                element: '#featured #makeabet .betNO .value',
                intro: '<p>Cena za zakład na <span class="orange">NIE</span> jest natomiast tutaj.</p>',
                position: 'left'
            },
            {
                element: '#featured #makeabet',
                intro: '<p>Za każdy <span class="green">wygrany</span> zakład otrzymasz <span class="orange">100</span> reputów.</p><p>Jeśli kupiłeś zakład za <span class="orange">60</span> reputów, na wygranej zyskasz dodatkowe <span class="green">40</span> reputów.</p><p class="comment">Zysk <span class="green">40rp</span> = wygrana <span class="orange">100rp</span> - cena za zakład <span class="orange">60rp</span></p>',
                position: 'bottom'
            },
            {
                element: '#featured #makeabet',
                intro: '<h2>Możesz kupić więcej, niż jeden zakład.</h2><p>By <span class="green">dodać kolejne,</span> posłuż się przyciskiem <span class="orange">[+].</span> Jeśli chcesz <span class="green">sprzedać zakłady,</span> skorzystaj z przycisku <span class="orange">[-].</span></p>',
                position: 'bottom'
            },
            {
                element: '#betfeed',
                intro: '<p>W przypadku innych wydarzeń, <span class="orange">wszystko działa tak samo!</span></p>',
                position: 'top'
            },
            {
                intro: '<h2>Powodzenia!</h2><p>Jesteś już gotowy do gry! <span class="green">Obstaw</span> swoje pierwsze <span class="orange">wydarzenia</span> i <span class="green">udowodnij,</span> że jesteś <span class="orange">czarnym koniem</span> tej politycznej rozgrywki!</p>'
            }
        ]
    });

    intro.start();
}
