$(function () {
    $("#id_date_from, #id_date_until").datepicker(
        {
            format: 'yyyy-mm-dd',
            language: 'uk',
            autoclose: true
        }
    );
    $('#id_timestamp').datetimepicker(
        'hide', {
            format: 'yyyy-mm-dd hh:ii:ss',
            language: 'uk',
            autoclose: true,
            todayBtn: true,
            pickerPosition: "top-right"
    })
});