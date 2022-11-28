$(document).ready(function () {
  $('#supplier_scf_datatable').DataTable({
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

  $("#confirmationSupplierModal").on("show.bs.modal", function (event) {
    // Get the button that triggered the modal
    var button = $(event.relatedTarget);

    // Extract value from the custom data-* attribute
    var url = button.data("url");
    $(this).find("#agree").attr("href", url);
  });
  $("#confirmationSupplierModal .modal-footer #agree").on(
    "click",
    function (event) {
      $("#confirmationSupplierModal .modal-footer #agree").text("")
      var $loading = $('<div class="spinner-border text-white" role="status"></div>')
      $("#confirmationSupplierModal .modal-footer #agree").append($loading)
      $.ajax({
        method: "GET",
        url: $(this).attr("href"),
      })
        .done(function (data) {
          $("#confirmationSupplierModal").modal("hide");
          // resetValue()
          location.reload();
          // $('#scf_datatable').DataTable().ajax.reload();
        })
        .fail(function (e) {
          console.log("error add order", e);
        });
    }
  );
});

$("#apply-loan-submit").on("click",function(){
  $("#apply-loan-submit").text("")
  var $loading = $('<div class="spinner-border text-white" role="status"></div>')
  $("#apply-loan-submit").append($loading)
})


$(".btn-view-get-voucher").on("click", function () {
  let v = $(this).data("voucher");
  $("#do_voucher").attr('src', `/static/UPLOAD_FOLDER/${v}`);
  $("#dataVoucherModal").modal("show");
})

// function saveAdditionalData(id) {
//   $.ajax({
//     method: "POST",
//     url: `/api/order/${id}`,
//   }).done(function (data) {
//     // let data = d;
//     // console.log("data", data);
//     // $(".modal-title").text(`Additional Data for order id #${data.id}`);
//     $("#do_nama_pt_enterprise").text(data.nama_pt_enterprise);
//     $("#do_nama_pemesan").text(data.nama_pemesan);
//     $("#do_no_hp_pemesan").text(data.no_hp_pemesan);
//     $("#do_nama_barang").text(data.nama_barang);
//     $("#do_jumlah_barang").text(`${formatNumer(data.jumlah_barang)} Buah`);
//     $("#do_jenis_bayar").text(data.jenis_bayar);
//     $("#do_total_discount").text(`Rp ${formatNumer(data.total_diskon ? data.total_diskon : 0)}`);
//     $("#do_total_harga").text(`Rp ${formatNumer(data.total_harga ? data.total_harga : 0)}`);
//     $("#do_sign_e").text(data.sign_enterprise ? data.sign_enterprise : '-');
//     $("#do_sign_s").text(data.sign_supplier ? data.sign_supplier : '-');
//     $("#do_voucher").attr('src', `${data.voucher}`);
//     $("#do_created_at").text(data.created_at);
//     $("#dataAdditionalModal").modal("show");
//   });
// }

$(".btn-add-extra-data-supplier").on("click", function () {
  const idOrder = $(this).data("order-id");
  $('.additional_order_id').val(idOrder)
  $('#dataAdditionalModal').modal('show')
  // getDetailOrder(idOrder);
  // getAdditionalData(idOrder);
});

$(".btn-view-status").on(
  "click",
  function () {
    let idOrder = $(this).data("order-id");
    getDetailApply(idOrder);
  }
);

function getFixedNumber(num1, num2) {
  let x = num1 / num2;
  return x.toFixed(2);
}

function getDetailApply(id) {
  $.ajax({
    method: "GET",
    url: `/api/order/${id}`,
  }).done(function (data) {
    console.log('data', data)
    var divider = 0
    if (data.action == 1 || data.action == 2 || data.action == 3) {
      divider = 1 / 3;
    }
    if (data.action == 4) {
      divider = 1 / 3;
    }
    if (data.action == 5) {
      divider = 3 / 3;
    }
    $("#progress").css("width", `${divider * 100}%`);
    const fixed = divider.toFixed(2);
    if (fixed == getFixedNumber(1,3)) {
      $("#apply_loan_to_finance").attr("class", "step step-active");
      $("#loan_confirm_by_finance").attr("class", "step");
      $("#funds_disbursed").attr("class", "step");
    // } 
    // else if (fixed == getFixedNumber(2,3)) {
    //   $("#apply_loan").attr("class", "step step-complete");
    //   $("#loan_confirm_by_finance").attr("class", "step step-complete");
    //   $("#funds_disbursed").attr("class", "step-step");
    } else {
      $("#apply_loan_to_finance").attr("class", "step step-active");
      $("#loan_confirm_by_finance").attr("class", "step step-active");
      $("#funds_disbursed").attr("class", "step step-active");
    }
    $("#detailApplyModal").modal("show");
  });
}