$(document).ready(function () {
  $('#finance_scf_datatable').DataTable({
    "scrollX": true,
    "scrollCollapse": true,
    "fixedColumns": {
      "right": 1,
      "left": 0
    },
    // "autoWidth": false,
    "columns": [{
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      },
      {
        "width": "20px"
      }
    ],
  });
});
var url = ''
$("#confirmationSignFinanceModal").on("show.bs.modal", function (event) {
  // Get the button that triggered the modal
  var button = $(event.relatedTarget);

  // Extract value from the custom data-* attribute
  url = button.data("url");
});
$("#agree").on("click",function(){
  $("#agree").text("")
  var $loading = $('<div class="spinner-border text-white" role="status"></div>')
  $("#agree").append($loading)
})
$("#confirmationSignFinanceModal .modal-footer #agree").on(
  "click",
  function (event) {
    $.ajax({
        method: "GET",
        url,
      })
      .done(function (data) {
        $("#confirmationSignFinanceModal").modal("hide");
        // resetValue()
        location.reload();
        // $('#scf_datatable').DataTable().ajax.reload();
      })
      .fail(function (e) {
        console.log("error sign finance", e);
      });
  }
);