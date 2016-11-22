$(function () {
    $("#id_date_from, #id_date_until").datepicker({format: 'yyyy-mm-dd', language: 'uk', autoclose: true});
    $('#id_timestamp').datetimepicker('update', {format: 'yyyy-mm-dd hh:ii:ss', language: 'uk', autoclose: true})
});