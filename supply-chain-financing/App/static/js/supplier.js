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



$(".btn-view-get-voucher").on("click", function () {
  let v = $(this).data("voucher");
  $("#do_voucher").attr('src', `${v}`);
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
  console.log('idOrder', idOrder)
  // getDetailOrder(idOrder);
  // getAdditionalData(idOrder);
});