$(document).ready(function () {
    function PostAjax(){
        var property_type_selected = ""
        $('.property_type_checkbox:checked').each(function () {
            property_type_selected += $(this).val() + ","
        });
        $('#property_type_check').val(property_type_selected)

        var property_for_selected = ""
        $('.property_for_checkbox:checked').each(function () {
            property_for_selected += $(this).val() + ","
        });
        $('#property_for_check').val(property_for_selected)
        
        var property_category_selected = ""
        $('.property_category_checkbox:checked').each(function () {
            property_category_selected += $(this).val() + ","
        });
        $('#property_category_check').val(property_category_selected)

        var amenities_selected = ""
        $('.amenities_checkbox:checked').each(function () {
            amenities_selected += $(this).val() + ","
        });
        $('#amenities_check').val(amenities_selected)

        var side_search_selected = ""
        $(".side_search").click(function () {
            side_search_selected = $(this).val()
        });
        $('#side_search_id').val(side_search_selected)

        var ddl_selected = ""
        $(".class-price").each(function () {
            ddl_selected = $(this).val()
        });
        $('#ddl_textbox_id').val(ddl_selected)

        $.post('/check/',
            {
                p_type_check: $('#property_type_check').val(),
                p_for_check: $('#property_for_check').val(),
                p_category_check : $('#property_category_check').val(),
                amenity_check: $('#amenities_check').val(),
                search_area: $('#search_area_id').val(),
                fetch_search_text: $('#search_text_id').val(),
                availlabel: $('#availlabel_id').val(),
                price: $('#amount_two').val(),
                ddl_selected_data: $('#ddl_textbox_id').val(),

                // min_price_box : $('#min_price').val(),
                // max_price_box : $('#max_price').val(),

                type: 'premium',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }, function (response) {
                $('#room').html(response)
                //document.documentElement.innerHTML = response;
                console.log(response)
            });

    }


    $('.property_type_checkbox, .property_for_checkbox, .property_category_checkbox, .amenities_checkbox, .search_field, .clear_all, .price-range, .side_search').click(function (event) {
        PostAjax();
    });
    $('.custom-select').change(function(event) {
        PostAjax();
      });
     

});