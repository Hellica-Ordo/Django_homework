function recalculate_total_values () {
    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    let quantity_arr = [];
    let price_arr = [];

    for (var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    order_total_quantity = 0;
    order_total_cost = 0;

    for (let i = 0; i < TOTAL_FORMS; i++) {
        order_total_quantity += quantity_arr[i];
        order_total_cost += quantity_arr[i] * price_arr[i];
    }


    $('.order_total_cost').text(order_total_cost);
    $('.order_total_quantity').text(order_total_quantity);
}

window.onload = function () {
    $('.order_form input[type="number"]').on('click', recalculate_total_values)
    recalculate_total_values()
}

function deleteOrderItem(row) {
   let target_name= row[0].querySelector('input[type="number"]').name;
   orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
   delta_quantity = -quantity_arr[orderitem_num];
   orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
}
