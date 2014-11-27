//pokaż menu z hamburgera
$(function(){
    $('.burger').on('click',function(){
        $('#maintop .mainmenu').addClass("display");
        $('.blankoverlay').addClass("display");
        setTimeout(function (){
            $('#maintop .mainmenu').addClass("opacity");
            $('.blankoverlay').addClass("opacity");
        }, 100); // opoznienie
    });
})

//ukryj wszystko po klieknieciu w overlay
$(function(){
        $('.blankoverlay').on('click',function(){
            $('#maintop .mainmenu').removeClass('display');
            $('#maintop .mainmenu').removeClass('opacity');
            $('.overlay').removeClass("opacity");
            $('.blankoverlay').removeClass("display");
            setTimeout(function (){
                $('.overlay').removeClass("display");
            }, 150); // opoznienie
    });
})

//ukryj okno logowania po kliknieciu w X
$(function(){
        $('.login-close').on('click',function(){
            $('#maintop .mainmenu').removeClass('display');
            $('#maintop .mainmenu').removeClass('opacity');
            $('.overlay').removeClass("opacity");
            $('.blankoverlay').removeClass("display");
            setTimeout(function (){
                $('.overlay').removeClass("display");
            }, 150); // opoznienie
    });
})

//pokaż okno logowania
$(function(){
        $('.show-login').on('click',function(){
            $('.overlay').addClass('display');
            $('#maintop .mainmenu').removeClass("opacity");
            setTimeout(function (){
                $('.overlay').addClass('opacity');
                $('#maintop .mainmenu').removeClass("display");
                $('.blankoverlay').addClass("display");
            }, 150); // opoznienie
    });
})

//zamykanie okien logowania
$(function(){
        $('.overlay-close').on('click',function(){
            $('.overlay').removeClass('opacity');
            setTimeout(function (){
                $('.overlay').removeClass('display');
            }, 150); // opoznienie
    });
})

//pokaż rejestrację przez e-mail
$(function(){
        $('.show-rejestracjaemail').on('click',function(){
            $('.rejestracja').removeClass('opacity');
            $('.logowanie').removeClass('opacity');
            $('.przypomnienie').removeClass('opacity');
            
            setTimeout(function (){
                $('.rejestracja').removeClass('asblock');
                $('.logowanie').removeClass('asblock');
                $('.przypomnienie').removeClass('asblock');
                
                $('.rejestracjaemail').addClass('asblock');
            }, 150); // opoznienie
            
            setTimeout(function (){
                $('.rejestracjaemail').addClass('opacity');
            }, 200); // opoznienie
    });
})

//pokaż rejestrację
$(function(){
        $('.show-rejestracja').on('click',function(){
            $('.rejestracjaemail').removeClass('opacity');
            $('.logowanie').removeClass('opacity');
            $('.przypomnienie').removeClass('opacity');
            
            setTimeout(function (){
                $('.rejestracjaemail').removeClass('asblock');
                $('.logowanie').removeClass('asblock');
                $('.przypomnienie').removeClass('asblock');
                
                $('.rejestracja').addClass('asblock');
            }, 150); // opoznienie
            
            setTimeout(function (){
                $('.rejestracja').addClass('opacity');
            }, 200); // opoznienie
    });
})

//pokaż logowanie
$(function(){
        $('.show-logowanie').on('click',function(){
            $('.rejestracjaemail').removeClass('opacity');
            $('.rejestracja').removeClass('opacity');
            $('.przypomnienie').removeClass('opacity');
            
            setTimeout(function (){
                $('.rejestracjaemail').removeClass('asblock');
                $('.rejestracja').removeClass('asblock');
                $('.przypomnienie').removeClass('asblock');
                
                $('.logowanie').addClass('asblock');
            }, 150); // opoznienie
            
            setTimeout(function (){
                $('.logowanie').addClass('opacity');
            }, 200); // opoznienie
    });
})

//pokaż reset hasła
$(function(){
        $('.show-przypomnienie').on('click',function(){
            $('.rejestracjaemail').removeClass('opacity');
            $('.rejestracja').removeClass('opacity');
            $('.logowanie').removeClass('opacity');
            
            setTimeout(function (){
                $('.rejestracjaemail').removeClass('asblock');
                $('.rejestracja').removeClass('asblock');
                $('.logowanie').removeClass('asblock');
                
                $('.przypomnienie').addClass('asblock');
            }, 150); // opoznienie
            
            setTimeout(function (){
                $('.przypomnienie').addClass('opacity');
            }, 200); // opoznienie
    });
})