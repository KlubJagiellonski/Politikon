//pokaż menu z hamburgera
$(function(){
    $('.burger').on('click',function(){
        $('#maintop .graj .avatarmenu ul').removeClass('display');
        $('#maintop .graj .avatarmenu ul').removeClass('opacity');
        $('#wallet-not').css({'margin-top' : ''});
        $('#wallet-not').removeClass("opacity");
        $('#maintop .userdata .wallet .arrowup').removeClass("display");
        $('#maintop .userdata .wallet .arrowup').removeClass("opacity");
        $('#maintop .mainmenu').addClass("display");
        $('.overlay').addClass("display");
        setTimeout(function (){
            $('#maintop .mainmenu').addClass("opacity");
            $('.overlay').addClass("opacity");
        }, 100); // opoznienie
    });
});
//pokaż menu z avatara
$(function(){
        $('#maintop .graj img').on('click',function(){
            $('#maintop .mainmenu').removeClass('display');
            $('#maintop .mainmenu').removeClass('opacity');
            $('#wallet-not').css({'margin-top' : ''});
            $('#wallet-not').removeClass("opacity");
            $('#maintop .userdata .wallet .arrowup').removeClass("display");
            $('#maintop .userdata .wallet .arrowup').removeClass("opacity");
            $('#maintop .graj .avatarmenu ul').addClass("display");
            $('.overlay').addClass("display");
            setTimeout(function (){
                $('#maintop .graj .avatarmenu ul').addClass("opacity");
                $('.overlay').addClass("opacity");
            }, 100); // opoznienie
    });
});
//pokaż powiadomienia
$(function(){
    $('#maintop .userdata .wallet.notification').on('click',function(){
        if (! $('#maintop .userdata .wallet .arrowup').hasClass("display")) {
            $('#maintop .mainmenu').removeClass('display');
            $('#maintop .mainmenu').removeClass('opacity');
            $('#maintop .graj .avatarmenu ul').removeClass('display');
            $('#maintop .graj .avatarmenu ul').removeClass('opacity');
            $('#wallet-not').css({'margin-top': '0px'});
            $('#maintop .userdata .wallet .arrowup').addClass("display");
            $('.overlay').addClass("display");
            setTimeout(function () {
                $('#wallet-not').addClass("opacity");
                $('#maintop .userdata .wallet .arrowup').addClass("opacity");
                $('.overlay').addClass("opacity");
            }, 100); // opoznienie
        } else {
            $('.overlay').click();
        }
    });
});
//ukryj wszystko po klieknieciu w overlay
$(function(){
        $('.overlay').on('click',function(){
            $('#maintop .mainmenu').removeClass('display');
            $('#maintop .mainmenu').removeClass('opacity');
            $('#maintop .graj .avatarmenu ul').removeClass('display');
            $('#maintop .graj .avatarmenu ul').removeClass('opacity');
            $('#maintop .userdata .wallet .arrowup').removeClass("display");
            $('#maintop .userdata .wallet .arrowup').removeClass("opacity");
            $('#wallet-not').removeClass("opacity");
            $('.overlay').removeClass("opacity");
            setTimeout(function (){
                $('#wallet-not').css({'margin-top' : ''});
                $('.overlay').removeClass("display");
            }, 150); // opoznienie
    });
});

//notifications - scroll setup
$(function() {
    $(document).ready(function() {
        // the element we want to apply the jScrollPane
        var $el = $('#jp-container').jScrollPane({
                verticalGutter: -16
            }),

        // the extension functions and options
            extensionPlugin = {

                extPluginOpts: {
                    // speed for the fadeOut animation
                    mouseLeaveFadeSpeed: 500,
                    // scrollbar fades out after hovertimeout_t milliseconds
                    hovertimeout_t: 1000,
                    // if set to false, the scrollbar will be shown on mouseenter and hidden on mouseleave
                    // if set to true, the same will happen, but the scrollbar will be also hidden on mouseenter after "hovertimeout_t" ms
                    // also, it will be shown when we start to scroll and hidden when stopping
                    useTimeout: false,
                    // the extension only applies for devices with width > deviceWidth
                    deviceWidth: 980
                },
                hovertimeout: null, // timeout to hide the scrollbar
                isScrollbarHover: false,// true if the mouse is over the scrollbar
                elementtimeout: null,	// avoids showing the scrollbar when moving from inside the element to outside, passing over the scrollbar
                isScrolling: false,// true if scrolling
                addHoverFunc: function () {

                    // run only if the window has a width bigger than deviceWidth
                    if ($(window).width() <= this.extPluginOpts.deviceWidth) return false;

                    var instance = this;

                    // functions to show / hide the scrollbar
                    $.fn.jspmouseenter = $.fn.show;
                    $.fn.jspmouseleave = $.fn.fadeOut;

                    // hide the jScrollPane vertical bar
                    var $vBar = this.getContentPane().siblings('.jspVerticalBar').hide();

                    /*
                     * mouseenter / mouseleave events on the main element
                     * also scrollstart / scrollstop - @James Padolsey : http://james.padolsey.com/javascript/special-scroll-events-for-jquery/
                     */
                    $el.bind('mouseenter.jsp', function () {

                        // show the scrollbar
                        $vBar.stop(true, true).jspmouseenter();

                        if (!instance.extPluginOpts.useTimeout) return false;

                        // hide the scrollbar after hovertimeout_t ms
                        clearTimeout(instance.hovertimeout);
                        instance.hovertimeout = setTimeout(function () {
                            // if scrolling at the moment don't hide it
                            if (!instance.isScrolling)
                                $vBar.stop(true, true).jspmouseleave(instance.extPluginOpts.mouseLeaveFadeSpeed || 0);
                        }, instance.extPluginOpts.hovertimeout_t);

                    }).bind('mouseleave.jsp', function () {

                        // hide the scrollbar
                        if (!instance.extPluginOpts.useTimeout)
                            $vBar.stop(true, true).jspmouseleave(instance.extPluginOpts.mouseLeaveFadeSpeed || 0);
                        else {
                            clearTimeout(instance.elementtimeout);
                            if (!instance.isScrolling)
                                $vBar.stop(true, true).jspmouseleave(instance.extPluginOpts.mouseLeaveFadeSpeed || 0);
                        }

                    });

                    if (this.extPluginOpts.useTimeout) {
                        $el.bind('scrollstart.jsp', function () {
                            // when scrolling show the scrollbar
                            clearTimeout(instance.hovertimeout);
                            instance.isScrolling = true;
                            $vBar.stop(true, true).jspmouseenter();
                        }).bind('scrollstop.jsp', function () {

                            // when stop scrolling hide the scrollbar (if not hovering it at the moment)
                            clearTimeout(instance.hovertimeout);
                            instance.isScrolling = false;
                            instance.hovertimeout = setTimeout(function () {
                                if (!instance.isScrollbarHover)
                                    $vBar.stop(true, true).jspmouseleave(instance.extPluginOpts.mouseLeaveFadeSpeed || 0);
                            }, instance.extPluginOpts.hovertimeout_t);
                        });

                        // wrap the scrollbar
                        // we need this to be able to add the mouseenter / mouseleave events to the scrollbar
                        var $vBarWrapper = $('<div/>').css({
                            position: 'absolute',
                            left: $vBar.css('left'),
                            top: $vBar.css('top'),
                            right: $vBar.css('right'),
                            bottom: $vBar.css('bottom'),
                            width: $vBar.width(),
                            height: $vBar.height()
                        }).bind('mouseenter.jsp', function () {

                            clearTimeout(instance.hovertimeout);
                            clearTimeout(instance.elementtimeout);

                            instance.isScrollbarHover = true;

                            // show the scrollbar after 100 ms.
                            // avoids showing the scrollbar when moving from inside the element to outside, passing over the scrollbar
                            instance.elementtimeout = setTimeout(function () {
                                $vBar.stop(true, true).jspmouseenter();
                            }, 100);

                        }).bind('mouseleave.jsp', function () {

                            // hide the scrollbar after hovertimeout_t
                            clearTimeout(instance.hovertimeout);
                            instance.isScrollbarHover = false;
                            instance.hovertimeout = setTimeout(function () {
                                // if scrolling at the moment don't hide it
                                if (!instance.isScrolling)
                                    $vBar.stop(true, true).jspmouseleave(instance.extPluginOpts.mouseLeaveFadeSpeed || 0);
                            }, instance.extPluginOpts.hovertimeout_t);

                        });

                        $vBar.wrap($vBarWrapper);

                    }

                }

            },

        // the jScrollPane instance
            jspapi = $el.data('jsp');

        // extend the jScollPane by merging
        $.extend(true, jspapi, extensionPlugin);
        jspapi.addHoverFunc();

        /**
         * Send request to set bet as viewed by me and remove it from wallet.
         * @param bets_id_list
         */
        function check_bets_viewed(bets_id_list) {
            $.ajax({
                type: 'get',
                data: {bets: bets_id_list},
                contentType: 'application/json;charset=utf-8',
                url: '/bets/viewed/',
                success: function(data) {
                    $('.a-betresult').each(function(){
                        var this_bet_id = $(this).data('bet_id');
                        for (var i = 0; i < data.length; i+=1) {
                            if (data[i] == this_bet_id) {
                                $(this).remove();
                                break;
                            }
                        }
                    });
                    if ($('.a-betresult').length > 0) {
                        $('#wallet_notification_count').html($('.a-betresult').length);
                    } else {
                        $('#wallet_notification_count').remove();
                    }
                    $('.overlay').click();
                },
                error: function(xhr, data) {
                    console.log('Some error when BETs sent: bezradny');
                }
            });
        }

        $('.a-betresult').click(function(){
            // set new finished bet as a read
            var bets = [$(this).data('bet_id')];
            check_bets_viewed(bets);
        });

        $('#all-bets-result').click(function(){
            // set all new finished bets as a read
            var bets = [];
            $('.a-betresult').each(function(){
                bets.push($(this).data('bet_id'));
            });
            check_bets_viewed(bets);
        });

        // It is neccessairy only when using wallet on /accounts/user_profile site.
        $('#go-to-all-results').click(function(){
            $('.overlay').click();
            $('#userinfo > ul > li > a[href=#powiadomieniaowynikach]').click();
        });
    });
});
