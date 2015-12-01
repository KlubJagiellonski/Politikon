function startIntro(){
        var intro = introJs();
          intro.setOptions({
        showBullets: false,
            showStepNumbers: false,
            steps: [
              {
                intro: "<b>Witamy w POLITIKONIE - pierwszych w Polsce zakładach politycznych!</b><br/><br/>W tym samouczku zaprezentujemy podstawowe elementy gry, dostępne dla niezalogowanego gracza."
              },
              {
                element: '.graj',
                intro: "<b>By grać w POLITIKON, musisz się zalogować.</b> <br/><br/> Jeśli chcesz poznać grę przed rejestracją, kliknij w OK.",
                position: 'left'
              },
              {
                element: '#featured',
                intro: '<b>Oto wyróżnione wydarzenie.</b> <br/><br/>Przyjrzyjmy mu się dokładnie.',
                position: 'bottom'
              },
              {
                element: '#featured h1',
                intro: "<b>Tytuł wydarzenia</b> <br/><br/>Zawsze ma formę pytania zamkniętego. Trafna odpowiedź na to pytanie jest kluczem do sukcesu w POLITIKONIE!",
                position: 'bottom'
              },
              {
                element: '#featured #makeabet',
                intro: '<b>Wybierz swoją odpowiedź</b> <br/><br/>Na pytanie z tytułu odpowiadasz tutaj. Możesz kupić zakłady na TAK lub na NIE.<br/><br/> Za zakłady płacisz w REPUTACH - walucie POLITIKONU.',
        position: 'bottom'
              },
              {
                element: '#featured #makeabet .betYES .value',
                intro: 'Cena za zakład na TAK widoczna jest tutaj.',
        position: 'right'
              },
              {
                element: '#featured #makeabet .betNO .value',
                intro: 'Cena za zakład na NIE jest natomiast tutaj.',
        position: 'left'
              },
          {
                element: '#featured #makeabet',
                intro: 'Za każdy wygrany zakład otrzymasz 100 reputów.<br/><br/>Jeśli kupiłeś zakład za 60 reputów, na wygranej zyskasz dodatkowe 40 reputów.<br/><br/><span style="font-style: italic; font-size: .7em;">(wygrana 100rp - cena za zakład 60rp = zysk 40rp)</span>',
        position: 'bottom'
              },
          {
                element: '#featured #makeabet .change',
                intro: '<b>Wskaźnik zmiany kursu</b> <br/><br/>Kurs zakładów zależy od zainteresowania społeczności POLITIKONU.',
        position: 'bottom'
              },
          {
                element: '#featured #makeabet .change',
                intro: 'Kurs rośnie, gdy gracze wykupują zakłady na TAK i spada, gdy kupują zakłady na NIE.',
        position: 'bottom'
              },
          {
                element: '#featured #makeabet .change',
                intro: 'To ważne, bo w każdej chwili możesz sprzedać kupione wcześniej zakłady. Staraj się kupować taniej i sprzedawać drożej.',
        position: 'bottom'
              },
              {
                element: '#betfeed',
                intro: 'W przypadku innych wydarzeń, wszystko działa tak samo! :).',
        position: 'top'
              },
              {
                intro: "<b>Dołącz do gry!</b><br/><br/>Jesteś już gotowy do gry. Zarejestruj się i zacznij stawiać na politkę!"
              }
            ]
          });

          intro.start();
      }
