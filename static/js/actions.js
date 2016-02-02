$(function() {
    $(document).ready(function() {
        // skraca tytuły zakładów
        $('.skroc').dotdotdot();

        //featured - pokazuje wykres
        $('#featured').hover(function () {
            $('.details').css({'opacity': '1'});
        }, function () { //mouseout
            $('.details').css({'opacity': '0'});
        });

        //ukrywa menu z hamburgera po odpaleniu intro
        $('.intro-start').on('click',function(){
            $('#maintop .mainmenu').removeClass("opacity");
            $('.blankoverlay').removeClass("opacity");
            setTimeout(function (){
                $('#maintop .mainmenu').removeClass("display");
                $('.blankoverlay').removeClass("display");
            }, 100); // opoznienie
        });

        // GŁÓWNE MENU - SCROLL
        var s = $("#maintop");
        var pos = s.position();
        var pagestatus = $("#POLITIKON");
        $(window).scroll(function() {
            var windowpos = $(window).scrollTop();

            if (windowpos >= 30) { // wysokosc, po ktorej zaczyna sie scroll
                s.addClass("sticktotop");
                s.css({'top': '0px'});
                pagestatus.addClass("body-scrolled");
            } else {
                s.removeClass("sticktotop");
                s.css({'top': ''});
                pagestatus.removeClass("body-scrolled");
            }
        });

        //zakładki
        $('.zakladki-content article').hide();
        $('.zakladki-content article:first').show();
        $('ul.tabs li').on('click',function(){
            $('ul.tabs li').removeClass('active');
            $(this).addClass('active');
            $('.zakladki-content article').hide();
            var activeTab = $(this).find('a').attr('href');
            $(activeTab).show();
            return false;
        });

        // wysyłanie formularza zmiany danych profilu
        $('#settings-submit #loadmore').click(function(){
            if ($('.active [href=#profil]').length > 0) {
                $('#profil form').submit();
            } else if ($('.active [href=#haslo]').length > 0) {
                $('#haslo form').submit();
            }
        });

        // kupowanie i sprzedawanie zakładów
        $(".a_bet").on('click', function(e) {
            e.preventDefault();
            var event_id = $(this).data('event_id');
            var data = { buy: $(this).data('buy'), outcome: $(this).data('outcome'), for_price : $(this).data('price') };
            var makebet = $(this).parent();
            var word_yes = 'TAK';    // TODO: resolve multi-language problem
            var word_no = 'NIE';    // TODO: resolve multi-language problem
            var word_eng_yes = 'YES';    // TODO: resolve multi-language problem
            var word_eng_no = 'NO';    // TODO: resolve multi-language problem
            var word_true = 'True';
            var word_false = 'False';

            // console.log('sent: ' + JSON.stringify(data));
            $.ajax({
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json',
                url: '/event/'+event_id+'/transaction/create/',
                success: function(data) {
                    // console.log(JSON.stringify(data));
                    if(data.updates && data.updates.user){
                        // console.log('RESP: ' + JSON.stringify(data.updates));
                        var event = data.updates.events[0];
                        var bet = data.updates.bets[0];
                        var user = data.updates.user;
                        var bets_type = '';     // YES or NO
                        makebet.children('.currentbet').children('p').children('.has_bets').html(bet.has);
                        makebet.children('.currentbet').children('p').children('.bought_avg_price').html(Math.round(bet.bought_avg_price * 100) / 100);
                        if (makebet.attr('class') == 'prawa') {
                            makebet.children('.change').addClass('hidden');
                        }

                        if (bet.outcome == true) {
                            // You have YES bets for the event
                            bets_type = word_yes;
                            makebet.addClass('morebets');
                            makebet.children('.a_betYES').data('price', event.buy_for_price);
                            makebet.children('.a_betYES').children('.betYES').children('.value').html(event.buy_for_price);
                            makebet.children('.a_betYES').children('.betYES').children('.txt').html('+');
                            makebet.children('.a_betNO').data('price', event.sell_for_price);
                            makebet.children('.a_betNO').data('outcome', word_eng_yes);
                            makebet.children('.a_betNO').data('buy', word_false);
                            makebet.children('.a_betNO').children('.betNO').children('.value').html(event.sell_for_price);
                            makebet.children('.a_betNO').children('.betNO').children('.txt').html('-');
                            makebet.children('.currentbet').children().first()
                            .removeClass('change')
                            .addClass('changeYES')
                            .html(bets_type);
                        } else {    // bet.outcome = false
                            // You have NO bets for the event
                            bets_type = word_no;
                            makebet.addClass('morebets');
                            makebet.children('.a_betYES').data('price', event.sell_against_price);
                            makebet.children('.a_betYES').data('outcome', word_eng_no);
                            makebet.children('.a_betYES').data('buy', word_false);
                            makebet.children('.a_betYES').children('.betYES').children('.value').html(event.sell_against_price);
                            makebet.children('.a_betYES').children('.betYES').children('.txt').html('-');
                            makebet.children('.a_betNO').data('price', event.buy_against_price);
                            makebet.children('.a_betNO').children('.betNO').children('.value').html(event.buy_against_price);
                            makebet.children('.a_betNO').children('.betNO').children('.txt').html('+');
                            makebet.children('.currentbet').children().first()
                            .removeClass('change')
                            .addClass('changeNO')
                            .html(bets_type);
                        }
                        if (bet.has == 0) {    // bet.has = 0
                            // You don't have any bets for the event
                            makebet.removeClass('morebets');
                            makebet.children('.a_betYES').children('.betYES').children('.txt').html(word_yes);
                            makebet.children('.a_betNO').children('.betNO').children('.txt').html(word_no);
                            makebet.children('.a_betYES').children('.betYES').children('.value').html(event.buy_for_price);
                            makebet.children('.a_betNO').children('.betNO').children('.value').html(event.buy_against_price);
                            makebet.children('.a_betYES').data('price', event.buy_for_price);
                            makebet.children('.a_betNO').data('price', event.buy_against_price);
                            makebet.children('.a_betYES').data('buy', word_true);
                            makebet.children('.a_betNO').data('buy', word_true);
                            makebet.children('.a_betYES').data('outcome', word_eng_yes);
                            makebet.children('.a_betNO').data('outcome', word_eng_no);
                            makebet.children('.currentbet').hide();
                            if (makebet.attr('class') == 'prawa') {
                                makebet.children('.change').removeClass('hidden');
                            }
                            makebet.children('.currentbet').children().first()
                            .removeClass('changeNO')
                            .removeClass('changeYES')
                            .addClass('change')
                            .html(bets_type);
                        } else {
                            makebet.children('.currentbet').show();
                        }

                        $(".walletvalue").fadeOut(200,function(){$(this).text(user.portfolio_value).fadeIn(200);});
                        $(".freevalue").fadeOut(200,function(){$(this).text(user.total_cash).fadeIn(200);});
                        $(".reputationvalue").fadeOut(200,function(){$(this).text(user.reputation+"%").fadeIn(200);});
                    }
                }
            });
        }); // end $(".a_bet").on()


    });
});
