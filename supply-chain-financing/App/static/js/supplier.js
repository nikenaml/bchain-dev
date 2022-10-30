$(document).ready(function () {
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
