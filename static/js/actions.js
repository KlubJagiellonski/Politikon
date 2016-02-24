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

        // możliwość url do strony i zakładki np: /accounts/user_profile/#powiadomieniaowynikach
        var anchor = window.location.hash.split('#');
        if (anchor.length > 1) {
            var tab_choosen = anchor[1];
            $('#userinfo > ul > li > a[href=#' + tab_choosen + ']').click();
        }

        // wysyłanie formularza zmiany danych profilu
        $('#settings-submit #loadmore').click(function(){
            var action;
            var form;
            if ($('.active').find('a').attr('href') == '#profil') {
                action = 'main';
                form = '#profil form';
            } else if ($('.active').find('a').attr('href') == '#haslo') {
                action = 'email';
                form = '#haslo form';
            }
            $('form#avatar').find('.hidden').appendTo(form);
            $('<input />').attr('type', 'hidden')
            .attr('name', 'action')
            .attr('value', action)
            .appendTo(form);
            $(form).submit();
        });

        // handle the custom upload widget
        function setPreviewSrc($wrapper, src) {
            var changeCallback = $wrapper.data('change-callback'),
            $preview = $wrapper.find('.preview'),
            width = $wrapper.data('preview-width') || $preview.width(),
            height = $wrapper.data('preview-height') || $preview.height();
            if (src) {
                $.when(prepareImage(src, width, height)).then(function (src) {
                    $wrapper.find('.preview').attr('src', src).show();
                    if (changeCallback) {
                        changeCallback(src);
                    }
                });
            } else {
                $wrapper.find('.preview').hide();
                if (changeCallback) {
                    changeCallback('');
                }
            }
        }
        function prepareImage(src, width, height) {
            var image = new Image(),
            dfd = $.Deferred();
            image.src = src;
            image.onload = function () {
                var cropped = document.createElement('canvas'),
                ctx = cropped.getContext('2d'),
                sourceRatio = image.width / image.height,
                destinationRatio = width / height,
                srcWidth, srcHeight;
                if (sourceRatio > destinationRatio) {
                    srcHeight = image.height;
                    srcWidth = image.height * destinationRatio;
                } else {
                    srcWidth = image.width;
                    srcHeight = image.width / destinationRatio;
                }
                cropped.width = width;
                cropped.height = height;
                ctx.drawImage(image, (image.width - srcWidth) / 2.0, (image.height - srcHeight) / 2.0, srcWidth, srcHeight, 0, 0, width, height);
                dfd.resolve(cropped.toDataURL());
            };
            return dfd;

        }
        $('.profile-avatar').parent('a').click(function () {
            var $input = $('input[type=file]', $(this).parent()),
                $wrapper = $(this);
            if ($input.val() || $wrapper.data('current')) {
                $wrapper.data('current', '');
                $wrapper.data('current-url', '');
                $input.val('').change();
            } else {
                $input.click();
            }
        });
        function getExtension(fname) {
            return fname.substr((~-fname.lastIndexOf(".") >>> 0) + 2);
        }
        $('.upload-wrapper').on('change', 'input[type=file]', function (event) {
            var $wrapper = $(this).closest('.upload-wrapper');
            if (event.target.files && event.target.files[0]) {
                var ext = getExtension(event.target.files[0].name),
                FR = new FileReader();
                if (ext !== 'jpeg' && ext !== 'jpg' && ext !== 'png') {
                    $(this).val('').change();
                    alert('This file type is not supported');
                    return;
                }
                FR.onload = function (e) {
                    setPreviewSrc($wrapper, e.target.result);
                    $wrapper.data('current-url', 'fixed');
                };
                FR.readAsDataURL(event.target.files[0]);
            } else {
                $wrapper.data('current-url', '');
            }
            // $(this).closest('.upload-wrapper').each(updateUploadWidget);
        });
        // $('.upload-wrapper').each(updateUploadWidget)
        // .data('updater', updateUploadWidget);

        // kupowanie i sprzedawanie zakładów
        $(".a_bet").on('click', function(e) {
            e.preventDefault();
            var event_id = $(this).data('event_id');
            var data = { buy: $(this).data('buy'), outcome: $(this).data('outcome'), for_price : $(this).data('price') };
            var makebets = $('body').find('[data-event_id="'+event_id+'"]').parent();
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
                        makebets.each(function(idx) {
                            // console.log($(this));
                            $(this).children('.currentbet').children('p').children('.has_bets').html(bet.has);
                            $(this).children('.currentbet').children('p').children('.bought_avg_price').html(Math.round(bet.bought_avg_price * 100) / 100);
                            if ($(this).hasClass('collapsible')) {
                                $(this).children('.change').addClass('hidden');
                            }

                            if (bet.outcome == true) {
                                // You have YES bets for the event
                                bets_type = word_yes;
                                $(this).addClass('morebets');
                                $(this).children('.a_betYES').data('price', event.buy_for_price);
                                $(this).children('.a_betYES').children('.betYES').children('.value').html(event.buy_for_price);
                                $(this).children('.a_betYES').children('.betYES').children('.txt').html('+');
                                $(this).children('.a_betNO').data('price', event.sell_for_price);
                                $(this).children('.a_betNO').data('outcome', word_eng_yes);
                                $(this).children('.a_betNO').data('buy', word_false);
                                $(this).children('.a_betNO').children('.betNO').children('.value').html(event.sell_for_price);
                                $(this).children('.a_betNO').children('.betNO').children('.txt').html('-');
                                $(this).children('.currentbet').children().first()
                                .removeClass('change')
                                .addClass('changeYES')
                                .html(bets_type);
                            } else {    // bet.outcome = false
                                // You have NO bets for the event
                                bets_type = word_no;
                                $(this).addClass('morebets');
                                $(this).children('.a_betYES').data('price', event.sell_against_price);
                                $(this).children('.a_betYES').data('outcome', word_eng_no);
                                $(this).children('.a_betYES').data('buy', word_false);
                                $(this).children('.a_betYES').children('.betYES').children('.value').html(event.sell_against_price);
                                $(this).children('.a_betYES').children('.betYES').children('.txt').html('-');
                                $(this).children('.a_betNO').data('price', event.buy_against_price);
                                $(this).children('.a_betNO').children('.betNO').children('.value').html(event.buy_against_price);
                                $(this).children('.a_betNO').children('.betNO').children('.txt').html('+');
                                $(this).children('.currentbet').children().first()
                                .removeClass('change')
                                .addClass('changeNO')
                                .html(bets_type);
                            }
                            if (bet.has == 0) {    // bet.has = 0
                                // You don't have any bets for the event
                                $(this).removeClass('morebets');
                                $(this).children('.a_betYES').children('.betYES').children('.txt').html(word_yes);
                                $(this).children('.a_betNO').children('.betNO').children('.txt').html(word_no);
                                $(this).children('.a_betYES').children('.betYES').children('.value').html(event.buy_for_price);
                                $(this).children('.a_betNO').children('.betNO').children('.value').html(event.buy_against_price);
                                $(this).children('.a_betYES').data('price', event.buy_for_price);
                                $(this).children('.a_betNO').data('price', event.buy_against_price);
                                $(this).children('.a_betYES').data('buy', word_true);
                                $(this).children('.a_betNO').data('buy', word_true);
                                $(this).children('.a_betYES').data('outcome', word_eng_yes);
                                $(this).children('.a_betNO').data('outcome', word_eng_no);
                                $(this).children('.currentbet').hide();
                                if ($(this).hasClass('collapsible')) {
                                    $(this).children('.change').removeClass('hidden');
                                }
                                $(this).children('.currentbet').children().first()
                                .removeClass('changeNO')
                                .removeClass('changeYES')
                                .addClass('change')
                                .html(bets_type);
                            } else {
                                $(this).children('.currentbet').show();
                            }
                        });

                        $(".walletvalue").fadeOut(200,function(){$(this).text(user.portfolio_value).fadeIn(200);});
                        $(".freevalue").fadeOut(200,function(){$(this).text(user.total_cash).fadeIn(200);});
                        $(".reputationvalue").fadeOut(200,function(){$(this).text(user.reputation).fadeIn(200);});
                    }
                },
                error: function (data) {
                    var response = JSON.parse(data.responseText);
                    notify(response.error, 'error');
                }
            });
        }); // end $(".a_bet").on()

        // powiadomienia
        function notify(text, type) {
            return noty({
                layout: 'topRight',
                text: text,
                type: type,
            });
        };


    });
});
