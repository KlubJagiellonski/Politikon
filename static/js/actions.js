// skraca tytuły zakładów 
$(function() {
    $('.skroc').dotdotdot();
});

//featured - pokazuje wykres
$(function() {                      
 $('#featured').hover(function () { 
    $('.details').css({'opacity': '1'});
}, function () { //mouseout
     $('.details').css({'opacity': '0'});
});});

//ukrywa menu z hamburgera po odpaleniu intro
$(function(){
    $('.intro-start').on('click',function(){
        $('#maintop .mainmenu').removeClass("opacity");
        $('.blankoverlay').removeClass("opacity");
        setTimeout(function (){
            $('#maintop .mainmenu').removeClass("display");
            $('.blankoverlay').removeClass("display");
        }, 100); // opoznienie
    });
})

// GŁÓWNE MENU - SCROLL
$(document).ready(function() {
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
});
 
//zakładki    
$(function(){
    //TODO: remove if unused
/*  $('ul.tabs li:first').addClass('active');
  $('.zakladki-content article').hide();
  $('.zakladki-content article:first').show();
  $('ul.tabs li').on('click',function(){
    $('ul.tabs li').removeClass('active');
    $(this).addClass('active')
    $('.zakladki-content article').hide();
    var activeTab = $(this).find('a').attr('href');
    $(activeTab).show();
    return false;
  });
  */
})
    