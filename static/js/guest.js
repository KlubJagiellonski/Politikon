(function() {
    $(document).ready(function () {

        var $mainmenu = $('#maintop .mainmenu');

        function hide_popups() {
            /*
            Hide all popups
             */
            $mainmenu.removeClass('display')
                     .removeClass('opacity');
            $('.overlay').removeClass("opacity");
            $('#login').removeClass("opacity")
                       .removeClass("display");
            $('.blankoverlay').removeClass("display");
            setTimeout(function () {
                $('.overlay').removeClass("display");
            }, 150); // opoznienie
        }

        //pokaż menu z hamburgera
        $('.burger').on('click', function () {
            $mainmenu.addClass("display");
            $('.blankoverlay').addClass("display");
            setTimeout(function () {
                $mainmenu.addClass("opacity");
                $('.blankoverlay').addClass("opacity");
            }, 100); // opoznienie
        });

        //ukryj wszystko po klieknieciu w overlay
        $('.blankoverlay').on('click', function () {
            hide_popups();
        });

        //ukryj okno logowania po kliknieciu w X
        $('.login-close').on('click', function () {
            hide_popups();
        });

        //pokaż okno logowania
        $('.show-login').on('click', function () {
            $('.overlay').addClass('display');
            $('#login').addClass("display");
            $mainmenu.removeClass("opacity");
            setTimeout(function () {
                $('.overlay').addClass('opacity');
                $('#login').addClass("opacity");
                $mainmenu.removeClass("display");
                $('.blankoverlay').addClass("display");
            }, 150); // opoznienie
        });

        //zamykanie okien logowania
        $('.overlay-close').on('click', function () {
            hide_popups();
        });

        //pokaż rejestrację przez e-mail
        $('.show-rejestracjaemail').on('click', function () {
            $('.rejestracja').removeClass('opacity');
            $('.logowanie').removeClass('opacity');
            $('.przypomnienie').removeClass('opacity');

            setTimeout(function () {
                $('.rejestracja').removeClass('asblock');
                $('.logowanie').removeClass('asblock');
                $('.przypomnienie').removeClass('asblock');

                $('.rejestracjaemail').addClass('asblock');
            }, 150); // opoznienie

            setTimeout(function () {
                $('.rejestracjaemail').addClass('opacity');
            }, 200); // opoznienie
        });

        //pokaż rejestrację
        $('.show-rejestracja').on('click', function () {
            $('.rejestracjaemail').removeClass('opacity');
            $('.logowanie').removeClass('opacity');
            $('.przypomnienie').removeClass('opacity');

            setTimeout(function () {
                $('.rejestracjaemail').removeClass('asblock');
                $('.logowanie').removeClass('asblock');
                $('.przypomnienie').removeClass('asblock');

                $('.rejestracja').addClass('asblock');
            }, 150); // opoznienie

            setTimeout(function () {
                $('.rejestracja').addClass('opacity');
            }, 200); // opoznienie
        });

        //pokaż logowanie
        $('.show-logowanie').on('click', function () {
            $('.rejestracjaemail').removeClass('opacity');
            $('.rejestracja').removeClass('opacity');
            $('.przypomnienie').removeClass('opacity');

            setTimeout(function () {
                $('.rejestracjaemail').removeClass('asblock');
                $('.rejestracja').removeClass('asblock');
                $('.przypomnienie').removeClass('asblock');

                $('.logowanie').addClass('asblock');
            }, 150); // opoznienie

            setTimeout(function () {
                $('.logowanie').addClass('opacity');
            }, 200); // opoznienie
        });

        //pokaż reset hasła
        $('.show-przypomnienie').on('click', function () {
            $('.rejestracjaemail').removeClass('opacity');
            $('.rejestracja').removeClass('opacity');
            $('.logowanie').removeClass('opacity');

            setTimeout(function () {
                $('.rejestracjaemail').removeClass('asblock');
                $('.rejestracja').removeClass('asblock');
                $('.logowanie').removeClass('asblock');

                $('.przypomnienie').addClass('asblock');
            }, 150); // opoznienie

            setTimeout(function () {
                $('.przypomnienie').addClass('opacity');
            }, 200); // opoznienie
        });

    });
})();
