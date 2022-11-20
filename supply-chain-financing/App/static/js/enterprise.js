$(document).ready(function () {
  $('#enterprise_scf_datatable').DataTable({
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
        "width": "100px"
      },
      {
        "width": "20px"
      }
    ],
  });

  var price =
    (jumlahBarang =
      discount =
      totalPrice =
      totalDisc =
      totalAmountDiscount =
      0);
  let namaPemesan =
    (noHpPemesan =
      idBarang =
      idJenisPembayaran =
      idSupplier =
      "");

  function alertBootstrap(message, type) {
    let alert = $(
      `<div class="alert alert-${type} alert-dismissible" role="alert"><div>${message}</div><button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`
    );
    $("#alert_message").html(alert);
  }

  function formatNumer(nStr) {
    nStr += "";
    x = nStr.split(".");
    x1 = x[0];
    x2 = x.length > 1 ? "." + x[1] : "";
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
      x1 = x1.replace(rgx, "$1" + "," + "$2");
    }
    return x1 + x2;
  }
  $("#nama_barang").on("change", function () {
    const opt = $(this).find("option").filter(":selected");
    price = opt.data("price");
    idBarang = $(this).val();
    calculate();
    checkValue();
  });
  $("#id_supplier").on("change", function () {
    idSupplier = $(this).val();
    $(".item-dropdown").show()
    calculate();
    checkValue();
  });
  $("#jenis_pembayaran").on("change", function () {
    const opt = $(this).find("option").filter(":selected");
    discount = opt.data("discount");
    idJenisPembayaran = $(this).val();
    calculate();
    checkValue();
  });
  $("#jumlah_barang").on("input", function () {
    jumlahBarang = $(this).val();
    calculate();
    checkValue();
  });
  $("#reset").on("click", function () {
    resetValue();
  });
  $("#nama_pemesan").on("input", function () {
    namaPemesan = $(this).val();
    checkValue();
  });
  $("#no_hp_pemesan").on("input", function () {
    noHpPemesan = $(this).val();
    checkValue();
  });
  $("#submit").on("click", function () {
    calculate();
  });
  $("#confirmationModal .modal-footer #agree").on("click", function (event) {
    calculate();
    let payload = {
      supplier_id: parseInt(idSupplier),
      enterprise_id: 1,
      item_id: parseInt(idBarang),
      payment_type_id: parseInt(idJenisPembayaran),
      item_count: parseInt(jumlahBarang),
      total_price: totalPrice,
      total_discount: totalAmountDiscount,
    };
    addOrder(payload);
  });
  $(".btn-view-detail-data").on("click", function () {
    let idOrder = $(this).data("order-id");
    // $('#detailOrderModal').modal('show')
    getDetailOrder(idOrder);
  });

  function getDetailOrder(id) {
    $.ajax({
      method: "GET",
      url: `/api/order/${id}`,
    }).done(function (data) {
      // let data = d;
      // console.log("data", data);
      $(".modal-title").text(`Detail Order #${data.id}`);
      $("#do_nama_pt_enterprise").text(data.nama_pt_enterprise);
      $("#do_nama_pemesan").text(data.nama_pemesan);
      $("#do_no_hp_pemesan").text(data.no_hp_pemesan);
      $("#do_nama_barang").text(data.nama_barang);
      $("#do_jumlah_barang").text(`${formatNumer(data.jumlah_barang)} Buah`);
      $("#do_jenis_bayar").text(data.jenis_bayar);
      $("#do_total_discount").text(`Rp ${formatNumer(data.total_diskon ? data.total_diskon : 0)}`);
      $("#do_total_harga").text(`Rp ${formatNumer(data.total_harga ? data.total_harga : 0)}`);
      $("#do_sign_e").text(data.sign_enterprise ? data.sign_enterprise : '-');
      $("#do_sign_s").text(data.sign_supplier ? data.sign_supplier : '-');
      $("#do_voucher").attr('src', `${data.voucher}`);
      $("#do_created_at").text(data.created_at);
      $("#detailOrderModal").modal("show");
    });
  }

  function resetValue() {
    $("#id_enterprise").prop("selectedIndex", 0);
    $("#nama_pemesan").val("");
    $("#no_hp_pemesan").val("");
    $("#nama_barang").prop("selectedIndex", 0);
    $("#jumlah_barang").val("");
    $("#jenis_pembayaran").prop("selectedIndex", 0);
  }

  function addOrder(payload) {
    $.ajax({
        method: "POST",
        url: "/api/order",
        data: JSON.stringify(payload),
        contentType: "application/json",
      })
      .done(function (data) {
        $("#confirmationModal").modal("hide");
        alertBootstrap(data.message, "success");
        // resetValue()
        location.reload();
        // $('#scf_datatable').DataTable().ajax.reload();
      })
      .fail(function (e) {
        console.log("error add order", e);
        alertBootstrap("Gagal menambahkan order", "danger");
      });
  }

  function calculate() {
    discJumlahBarang = getExtraDiscount(jumlahBarang, "item.count");
    discId = getExtraDiscount(idBarang, "item.specificId");
    const totalEdiscount = parseFloat(discJumlahBarang) + parseFloat(discId);
    totalDisc = parseFloat(totalEdiscount) + parseFloat(discount);

    const tempTotalPrice = jumlahBarang * price;
    totalAmountDiscount = tempTotalPrice * totalDisc;

    totalPrice = tempTotalPrice - totalAmountDiscount;
    $("#jumlah_discount").text(formatNumer(totalAmountDiscount));
    $("#discount").text(`${discount}%`);
    $("#extra_discount").text(`${totalEdiscount}%`);
    $("#total_discount").text(`${totalDisc}%`);
    $("#total_harga").text(formatNumer(totalPrice));
  }

  // let = deklarasi variable untuk local only (hanya bisa di akses di function itu saja)
  // var = deklarasi variable untuk global (bisa diakses difunction apapun)
  // const = deklarasi variable untuk value yg tidak pernah berubah
  function getExtraDiscount(value, type) {
    let discount = 0;
    if (type == "item.count") {
      if (value > 5) {
        discount = 0.05;
      }
    }
    if (type == "item.specificId") {
      if (value == 3) {
        discount = 0.03;
      }
    }
    return discount;
  }

  function checkValue() {
    let disable = true;
    if (
      idSupplier !== "" &&
      // namaPemesan !== "" &&
      // noHpPemesan !== "" &&
      idBarang !== "" &&
      idJenisPembayaran !== "" &&
      jumlahBarang !== 0
    ) {
      disable = false;
    }
    if (disable) {
      $("#submit").prop("disabled", true);
    } else {
      $("#submit").prop("disabled", false);
    }
  }
});