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
$("#agree").on("click", function () {
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

$(".btn-view-status-finance").on("click", function (e) {
  const t = $(this);
  urlStatus = t.data("order-id");
  url = t.data("url");
  $.ajax({
      method: "GET",
      url: url, // TODO: urlStatus harus diisi dengan url untuk get API status di page finance 
    })
    .done(function (data) {
      console.log('hasil response API get status => ', data) // TODO: hasil dari API get status akan muncul di console log ini
      let divider = data.action / 4;
      console.log('divider', divider)
      $("#progress").css("width", `${divider * 100}%`);
      if (divider == 1 / 4) {
        $("#funds_disbursed").attr("class", "step step-active");
        $("#shipment").attr("class", "step");
        $("#receive").attr("class", "step");
        $("#payment_by_enterprise").attr("class", "step");
      } else if (divider == 2 / 4) {
        $("#funds_disbursed").attr("class", "step step-active");
        $("#shipment").attr("class", "step step-active");
        $("#receive").attr("class", "step");
        $("#payment_by_enterprise").attr("class", "step");
      } else if (divider == 3 / 4) {
        $("#funds_disbursed").attr("class", "step step-active");
        $("#shipment").attr("class", "step step-active");
        $("#receive").attr("class", "step step-active");
        $("#payment_by_enterprise").attr("class", "step");
      } else if (divider == 4 / 4) {
        $("#funds_disbursed").attr("class", "step step-active");
        $("#shipment").attr("class", "step step-active");
        $("#receive").attr("class", "step step-active");
        $("#payment_by_enterprise").attr("class", "step step-active");
      }
      $('#detailFundsDisbursed').modal('show')
    })
    .fail(function (e) {
      console.log("error sign finance", e);
    });
});