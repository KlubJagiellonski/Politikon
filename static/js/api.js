/**
 * Created by ppeczek on 5/23/17.
 */
(function() {
  $(document).ready(function () {

    function saveForm(url, data, method) {
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
          location.reload();
        },
        error: function (cb) {
          console.log(cb);
        }
      });
    }

    $('form#add-event-form').submit(function (e) {
      e.preventDefault();
      if ($(this).valid()) {
        saveForm($(this).attr('action'), new FormData($(this)[0]), $(this).attr('method'));
      }
    });
  });
})();
