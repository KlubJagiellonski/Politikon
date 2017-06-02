/**
 * Created by ppeczek on 5/23/17.
 */
(function() {
  $(document).ready(function () {

    function saveForm(url, data, method, onSuccess) {
      console.log(data);
      $.ajax({
        type: method,
        url: url,

        cache: false,
        contentType: false,
        processData: false,

        dataType: 'JSON',
        data: data,
        success: function (result) {
          onSuccess();
        },
        error: function (cb) {
          console.log(cb);
        }
      });
    }

    $('form#add-event-form').submit(function (e) {
      e.preventDefault();
      var onSuccess = function () {
        location.reload()
      };
      if ($(this).valid()) {
        saveForm($(this).attr('action'), new FormData($(this)[0]), $(this).attr('method'), onSuccess);
      }
    });

    $('form#contact-form').submit(function (e) {
      e.preventDefault();
      var onSuccess = function () {
        $('#contact-us').hide();
        $('#contact-done').show();
      };
      if ($(this).valid()) {
        saveForm($(this).attr('action'), new FormData($(this)[0]), $(this).attr('method'), onSuccess);
      }
    });

  });
})();
