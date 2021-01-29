//link: https://getbootstrap.com/docs/4.0/components/modal/
$('#preview_modal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var link = button.data('link') // Extract info from data-* attributes
  var modal = $(this)
  //link: https://stackoverflow.com/questions/7551912/jquery-force-set-src-attribute-for-iframe
  modal.find('#preview_page').attr('src', link)
})
