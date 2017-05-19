/**
 * Code refactored by orkan at 24-09-2016
 */

(function() {
    $(document).ready(function () {

        var $mainmenu = $('#maintop');
        var $overlay = $('#overlay');

        function showModal(name) {
            /*
             * Show modal (popup), name must be tag id ex.: <tag id="name">...</tag>
             */
            $overlay.addClass('display')
                .width('100%')
                .height('100%');
            var $modal = $('#'+name);
            $modal.appendTo($overlay)
                .addClass('display')
                .css('z-index', 9000);
            $mainmenu.css('z-index', 5000)
                .removeClass("opacity");
            setTimeout(function () {
                $overlay.addClass('opacity');
                $modal.addClass("opacity");
            }, 150); // opoznienie
        }

        function hideModal() {
            /*
             * Hide all popups
             */
            $overlay.children().each(function(){
                // this condition skips div#overlay-close element
                if ($(this).hasClass('display')) {
                    $(this).removeClass('display')
                        .removeClass('opacity');
                    // move active modal from div#overlay to div#modals
                    $(this).appendTo($('#modals'));
                }
            });
            $mainmenu.removeClass('display')
                     .removeClass('opacity');
            $('.small-popup').removeClass('display')
                    .removeClass('opacity');
            setTimeout(function () {
                $overlay.removeClass("opacity")
                        .removeClass("display");
            }, 150); // opoznienie
        }

        function showSmallPopup(name){
            $('.small-popup').removeClass('display')
                .removeClass('opacity');
            $mainmenu.css('z-index', 8000);
            $('#' + name).addClass("display");
            $overlay.addClass("display")
                .width('100%')
                .height('100%');
            setTimeout(function () {
                $('#' + name).addClass("opacity");
                $overlay.addClass("opacity");
            }, 100); // opoznienie
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

        //pokaż okno logowania
        $('.show-login').on('click', function () {
            showModal('login');
        });

        // Show dialog with voting
        $('.show-zakoncz-wydarzenie').on('click', function () {
            showModal('outcome-action');
        });

        // Show message about points reset - in authomaticated.html is condition for it
        $('#reset-message').each(function(){
            showModal('reset-message');
        });

        // Add new event proposition
        $('#add-event-button').on('click', function(){
            showModal('add-event');
        });

        //ukryj okno logowania po kliknieciu w X
        $('.login-close').on('click', function () {
            hideModal();
        });

        //ukryj wszystko po klieknieciu w overlay
        $('#overlay-close').on('click', function () {
            hideModal();
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

        //pokaż menu z hamburgera
        $('.burger').on('click', function () {
            showSmallPopup('mainmenu');
        });

        //pokaż menu z avatara
        $('#maintop .graj .image').on('click', function () {
            if (!$('#maintop .graj .avatarmenu ul').hasClass('display')) {
                showSmallPopup('avatarmenu');
            } else {
                $('.overlay').click();
            }
        });

        //pokaż powiadomienia
        $('#maintop .userdata .wallet.notification').on('click', function () {
            if (!$('#maintop .userdata .wallet .arrowup').hasClass("display")) {
                showSmallPopup('arrowup');
                $('#wallet-not').css({'margin-top': '0px'});
                $('#wallet-not').addClass("opacity");
            } else {
                $('.overlay').click();
            }
        });
        //featured - pokazuje wykres
        $(document).on({
            mouseenter: function () {
                $('.details').css({'opacity': '1'});
            },
            mouseleave: function () {
                $('.details').css({'opacity': '0'});
            }
        }, '#featured');

        //featured - hover
        $(document).on({
            mouseenter: function () {
                $(this).find('figcaption').find('h2').animate({marginTop: "196px"}, 100);
            },
            mouseleave: function () {
                $(this).find('figcaption').find('h2').animate({marginTop: "250px"}, 100);
            }
        }, '#betfeed .bet');

        //ukrywa menu z hamburgera po odpaleniu intro
        $(document).on('click', '.intro-start', function () {
            $mainmenu.removeClass("opacity");
            $('.blankoverlay').removeClass("opacity");
            setTimeout(function () {
                $mainmenu.removeClass("display");
                $('.blankoverlay').removeClass("display");
            }, 100); // opoznienie
        });

        // wysyłanie formularza zmiany danych profilu
        $(document).on('click', '#settings-submit #loadmore', function () {
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

        // kupowanie i sprzedawanie zakładów
        function play_bet() {
            $('.a_bet').each(function () {
                if ($(this).data('click') == true) {
                    // to prevent bind multi click action to one existed elements
                    return null;
                }
                $(this).data('click', true);
                $(this).click(function (e) {
                    e.preventDefault();
                    var event_id = $(this).data('event_id');
                    var data = {
                        buy: $(this).data('buy'),
                        outcome: $(this).data('outcome'),
                        for_price: $(this).data('price')
                    };
                    var makebets = $('body').find('#makeabet [data-event_id="' + event_id + '"]').parent();
                    $.ajax({
                        type: 'POST',
                        data: JSON.stringify(data),
                        contentType: 'application/json',
                        url: '/event/' + event_id + '/transaction/create/',
                        success: function (data) {
                            // console.log(JSON.stringify(data));
                            if (data.updates && data.updates.user) {
                                // console.log('RESP: ' + JSON.stringify(data.updates));
                                var event = data.updates.events[0];
                                var bet = data.updates.bets[0];
                                var user = data.updates.user;
                                var bets_type = '';     // YES or NO
                                makebets.each(function () {
                                    // console.log($(this));
                                    // update element with bets number and average bet price
                                    var currentbet = $(this).children('.currentbet');
                                    var p_el = currentbet.children('p');
                                    var first_currentbet = currentbet.children().first();
                                    var a_betYes = $(this).children('.a_betYES');
                                    var a_betNo = $(this).children('.a_betNO');
                                    var betYes = a_betYes.children('.betYES');
                                    var betNo = a_betNo.children('.betNO');

                                    p_el.children('.has_bets').html(bet.has);
                                    p_el.children('.bought_avg_price').html(Math.round(bet.bought_avg_price));

                                    if ($(this).hasClass('collapsible')) {
                                        $(this).children('.change').addClass('hidden');
                                    }
                                    $(this).addClass('morebets');

                                    if (bet.outcome == true) {
                                        // You have YES bets for the event
                                        bets_type = words['youYes'];
                                        a_betYes.data('price', event.buy_for_price);
                                        betYes.children('.value').html(event.buy_for_price);
                                        betYes.children('.txt').html(words['buyYes']);
                                        a_betNo.data('price', event.sell_for_price);
                                        a_betNo.data('outcome', true);
                                        a_betNo.data('buy', false);
                                        betNo.children('.value').html(event.sell_for_price);
                                        betNo.children('.txt').html(words['sellBet']);
                                        first_currentbet.removeClass('change')
                                            .addClass('changeYES')
                                            .html(bets_type);
                                    } else {    // bet.outcome = false
                                        // You have NO bets for the event
                                        bets_type = words['youNo'];
                                        a_betYes.data('price', event.sell_against_price);
                                        a_betYes.data('outcome', false);
                                        a_betYes.data('buy', false);
                                        betYes.children('.value').html(event.sell_against_price);
                                        betYes.children('.txt').html(words['sellBet']);
                                        a_betNo.data('price', event.buy_against_price);
                                        betNo.children('.value').html(event.buy_against_price);
                                        betNo.children('.txt').html(words['buyNo']);
                                        first_currentbet.removeClass('change')
                                            .addClass('changeNO')
                                            .html(bets_type);
                                    }
                                    if (bet.has == 0) {    // bet.has = 0
                                        // You don't have any bets for the event
                                        $(this).removeClass('morebets');
                                        betYes.children('.txt').html(words['yes']);
                                        betNo.children('.txt').html(words['no']);
                                        betYes.children('.value').html(event.buy_for_price);
                                        betNo.children('.value').html(event.buy_against_price);
                                        a_betYes.data('price', event.buy_for_price);
                                        a_betNo.data('price', event.buy_against_price);
                                        a_betYes.data('buy', true);
                                        a_betNo.data('buy', true);
                                        a_betYes.data('outcome', true);
                                        a_betNo.data('outcome', false);
                                        currentbet.hide();
                                        if ($(this).hasClass('collapsible')) {
                                            $(this).children('.change').removeClass('hidden');
                                        }
                                        first_currentbet.removeClass('changeNO')
                                            .removeClass('changeYES')
                                            .addClass('change')
                                            .html(bets_type);
                                    } else {
                                        currentbet.show();
                                    }
                                });

                                $(".walletvalue").fadeOut(200, function () {
                                    $(this).text(user.portfolio_value).fadeIn(200);
                                });
                                $(".freevalue").fadeOut(200, function () {
                                    $(this).text(user.total_cash).fadeIn(200);
                                });
                                $(".reputationvalue").fadeOut(200, function () {
                                    $(this).text(user.reputation).fadeIn(200);
                                });
                            }
                        },
                        error: function (data) {
                            var response = JSON.parse(data.responseText);
                            notify(response.error, 'error');
                        }
                    }); // ajax
                });

            }); // end $(".a_bet").on()
        }

        play_bet();

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

        // powiadomienia
        function notify(text, type) {
            return noty({
                layout: 'topRight',
                text: text,
                type: type
            });
        }

        // handle the custom upload widget
        function setPreviewSrc($wrapper, src) {
            var changeCallback = $wrapper.data('change-callback'),
                $preview = $wrapper.find('.preview'),
                width = $wrapper.data('preview-width') || $preview.width(),
                height = $wrapper.data('preview-height') || $preview.height();
            if (src) {
                $.when(prepareImage(src, width, height)).then(function (src) {
                    $wrapper.find('.preview').css({
                        'background-image': 'url(' + src + ')',
                        'background-size': 'cover',
                        'background-repeat': 'no-repeat',
                        'background-position': 'center center'
                    }).show();
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

        function getExtension(fname) {
            return fname.substr((~-fname.lastIndexOf(".") >>> 0) + 2);
        }

        function preloadImages() {
            // preload images
            $("[data-preload-url]").each(function (i, x) {
                var el = $(x);
                var url = el.attr("data-preload-url");
                var image = new Image();
                el.toggleClass("preloading");
                // console.log("preloading");
                image.onload = function () {
                    // console.log("preloaded", el);
                    el.toggleClass("preloading");
                    window.x = el;
                    el.css({
                        'background-image': 'url(' + url + ')',
                        'background-size': 'cover',
                        'background-repeat': 'no-repeat',
                        'background-position': 'center center',
                    });
                    el.removeAttr('data-preload-url');
                };
                image.src = url;
            });

        }
        // skraca tytuły zakładów
        $('.skroc').dotdotdot();

        preloadImages();

        // GŁÓWNE MENU - SCROLL
        var pos = $mainmenu.position();
        var pagestatus = $("#POLITIKON");
        $(window).scroll(function () {
            var windowpos = $(window).scrollTop();

            if (windowpos >= 30) { // wysokosc, po ktorej zaczyna sie scroll
                $mainmenu.addClass("sticktotop");
                $mainmenu.css({'top': '0px'});
                pagestatus.addClass("body-scrolled");
            } else {
                $mainmenu.removeClass("sticktotop");
                $mainmenu.css({'top': ''});
                pagestatus.removeClass("body-scrolled");
            }
        });

        // It is necessary to not duplicate requests.
        var waypoint_checks = {
            transactions: null,
            notifications: null,
            portfolio: null,
            betfet: null
        };

        function active_waypoint(items_list) {
            var item_list_name = items_list.id.split('-')[0];

            // check if exist and destroy any waypoint on hidden tab
            for (var key in waypoint_checks) {
                if (key != item_list_name) {
                    var waypoint_check = waypoint_checks[key];
                    if (waypoint_check != null) {
                        waypoint_check.destroy();
                        waypoint_checks[key] = null;
                    }
                }
            }
            // create a waypoint only for current tab
            if (waypoint_checks[item_list_name] == null) {
                waypoint_checks[item_list_name] = new Waypoint.Infinite({
                    element: $('#' + item_list_name + '-list')[0],      //  #transactions-list
                    items: '.' + item_list_name + '-item',              //  .transactions-item
                    more: '.' + item_list_name + '-loadmore',          //  .transactions-loadmore
                    onBeforePageLoad: function() {
                        $('.' + item_list_name + '-loadmore .btn').text("Ładowanie...")
                    },
                    onAfterPageLoad: function() {
                        $('.' + item_list_name + '-loadmore .btn').text("wyświetl więcej rekordów");
                        $('.skroc').dotdotdot();
                    }
                });
            }
        }
        // tabs
        $('.zakladki-content article').removeClass('active');
        $('.zakladki-content article:first').addClass('active');
        // Switch to other tab
        $('ul.tabs li').on('click', function () {
            $('ul.tabs li').removeClass('active');
            $(this).addClass('active');
            $('.zakladki-content article').removeClass('active');
            var activeTab = $(this).find('a').attr('href');
            $(activeTab).addClass('active');
            var items_list = $(activeTab + ' > div')[0];
            if (items_list) {
                active_waypoint(items_list);
            }
            return false;
        });

        // Waypoint initialize on active tab after page load
        $('.zakladki-content article').each(function(){
            if ($(this).hasClass('active') && $(this).children('div').length > 0) {
                active_waypoint($(this).children('div')[0]);
            }
        });

        // This will automatically switch to tab specified by anchor
        // ex: /accounts/user_profile/#powiadomieniaowynikach
        var anchor = window.location.hash.split('#');
        if (anchor.length > 1) {
            var tab_choosen = anchor[1];
            var tabswitches = $('#userinfo > ul > li > a');
            for (var tabswitch in tabswitches) {
                if (tabswitch.href == '#' + anchor) {
                    tabswitch.click();
                }
            }
        }

        $('.profile-avatar').parent('a').on('click', function () {
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

        if ($('#betfeed').length > 0) {
            $(function () {
                new Waypoint.Infinite({
                    element: $('#betfeed')[0],
                    items: '.event-item',
                    more: '.event-loadmore',
                    onBeforePageLoad: function () {
                        $(".loadmore .btn").text("Ładowanie...")
                    },
                    onAfterPageLoad: function () {
                        $(".loadmore .btn").text("Wyświetl więcej zakładów");
                        preloadImages();
                        $('.skroc').dotdotdot();
                        renderCharts();
                        play_bet();
                    }
                });
            });
        }
    });
})();
