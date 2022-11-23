const btnDelete = document.querySelectorAll('.btn-delete');
if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete it?')) {
                e.preventDefault();
            }
        });
    })
}

$(document).ready(function () {
    $('#scf_datatable').DataTable({
        "scrollX": true,
        "scrollCollapse": true,
        "fixedColumns":   {
            "right": 1,
            "left": 0 
        },
        "columnDefs": [
            { "width": "20%", "targets": 6 }
          ],
        "autoWidth": true
        
    });
});
