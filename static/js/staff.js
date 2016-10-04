// Show dialog with voting
$(document).on('click', '.show-zakoncz-wydarzenie', function () {
    $('#login').addClass("display");
    $('.overlay').addClass("display");

    setTimeout(function () {
        $('#login').addClass("opacity");
        $('.overlay').addClass("opacity");
    }, 150); // opoznienie
});

// Vote for solution
$(document).on('click', '#resolveabet .a_bet', function (e) {
    var event_id = $(this).data('event_id');
    var outcome = $(this).data('outcome');
    var data = {outcome: outcome};
    var resolveabet = $('body').find('#resolveabet [data-event_id="' + event_id + '"]').parent();
    $.ajax({
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        url: '/event/' + event_id + '/resolve/',
        success: function (data) {
            // console.log(JSON.stringify(data));
            if (data.updates) {
                // console.log('RESP: ' + JSON.stringify(data.updates));
                var count_YES = data.updates.YES;
                var count_NO = data.updates.NO;
                var count_CANCEL = data.updates.CANCEL;
                var text_YES = 'TAK';
                var text_NO = 'NIE';
                var text_CANCEL = 'ANULUJ';
                resolveabet.each(function (idx) {
                    $(this).children('.a_betYES').children('.betYES').children('.value').html(count_YES);
                    $(this).children('.a_betNO').children('.betNO').children('.value').html(count_NO);
                    $(this).children('.a_betCANCEL').children('.betCANCEL').children('.value').html(count_CANCEL);
                    $(this).prev().removeClass('hidden');
                    var newText;
                    if (outcome === 'YES') {
                        newText = text_YES;
                    }
                    else if (outcome === 'NO') {
                        newText = text_NO;
                    }
                    else {
                        newText = text_CANCEL;
                    }
                    $(this).prev().find('span#decision').html(newText);
                });
            }
        },
        error: function (data) {
            var response = JSON.parse(data.responseText);
            notify(response.error, 'error');
            // console.log(data);
        }
    });
});

//ukryj okno logowania po kliknieciu w X
$(function () {
    $('.login-close').on('click', function () {
        $('#maintop .mainmenu').removeClass('display');
        $('#maintop .mainmenu').removeClass('opacity');
        $('.overlay').removeClass("opacity");
        $('.blankoverlay').removeClass("display");
        $('#login').removeClass("display");
        setTimeout(function () {
            $('.overlay').removeClass("display");
        }, 150); // opoznienie
    });
});