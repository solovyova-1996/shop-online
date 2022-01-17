window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity,
        delta_cost;
    let quantity_array = []
    let price_arr = []
//    сколько строк в заказе
    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    console.log(total_forms)
//   ($('.order_total_quantity') обращение к классу( если нет строк(NAN) то заменим его на 0)
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0
//    забираем цену с формы и точку меняем на запятую если NAN то 0
    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0

    for (let i = 0; i < total_forms; i++) {
//    строим строку, которая будет выглядеть определенным образом
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseInt($('input[name=orderitems-' + i + '-price').val());
//        складываем значение количества товара в массив
        quantity_array[i] = _quantity
//        если есть какая-то цена то кладем ее в массив
        if (_price) {
            price_arr[i] = _price
        } else {
            price_arr[i] = 0
        }

    }
//
// обработка клика на чекбокс
    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target
//        находим номер строки
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quontity', ''))
        if (price_arr[orderitem_num]) {
//если в списке цен есть цена товар, получаем количество товара по номеру строки
            orderitem_quantity = parseInt(target.value)
            //отнимаем от полученного количества исходное количество которое было перед изменением заказа
            delta_quantity = orderitem_quantity - quantity_array[orderitem_num]
            quantity_array[orderitem_num] = orderitem_quantity;
            // в функцию передаем новое количество товара и разницу между исходным количеством и текущим
            orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
        }

    })
    // при клике на checkbox
    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target
//        находим номер строки
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''))
        // если нажали и поставили галочку
        if (target.checked) {
            // отнимаем количество в этой строке
            delta_quantity = -quantity_array[orderitem_num]
            //    если галочку убрали то возвращаем это количество
        } else {
            delta_quantity = quantity_array[orderitem_num]
        }
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    })


    function orderSummerUpdate(orderitem_price, delta_quantity) {
        // считаем на сколько нужно прибавить цену, умножаем разницу количеств на цену за товар
        delta_cost = orderitem_price * delta_quantity
        // прибавляем цену прибавленных товаров к итоговой цене
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        // прибавляем к итоговому количество прибавленных товаров
        order_total_quantity = order_total_quantity + delta_quantity;
        // загружаем показатели в html
        $('.order_total_quantity').html(order_total_quantity.toString())
        $('.order_total_cost').html(order_total_price.toString() + ',00')
    }
    // upgrade form
    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });
    // удаление строки с заказом
    function deleteOrderItem(row){
        // обращаемся к первой строке в заказах
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quontity', ''))
        delta_quantity =  - quantity_array[orderitem_num]
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    }
}
// задание сделать так чтоб при добавлении товара цена притягивалась сразу