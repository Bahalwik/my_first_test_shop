$(document).ready(function (){
    var form = $('#form_buying_product')
    console.log(form)
        form.on('submit', function (e){
            e.preventDefault();
            console.log('111222')
            nmb = $('#number').val();
            console.log(nmb);
            submit_btn = $('#submit_btn');
            product_id  = submit_btn.data("product_id")
            product_name  = submit_btn.data("product_name")
            product_price = submit_btn.data("product_price")

            console.log(product_id);
            console.log(product_name);
            console.log(product_price);

                var data = {};
                data.product_id = product_id;
                data.nmb = nmb;
                var csrf_token = $('#form_buying_product [name=csrfmiddlewaretoken]').val();
                data["csrfmiddlewaretoken"] = csrf_token

                var url = form.attr("action");
                $.ajax({
                    url:url,
                    type: 'POST',
                    data: data,
                    cache: true,
                    success: function (data){
                        console.log('OK');
                        console.log((data.products_total_nmb))
                        if (data.products_total_nmb){
                            $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                        }

                    },
                    error: function (data){
                        console.log('error')
                    }
                })

            $('.basket-items ul').append('<li>'+product_name+', ' + nmb + 'шт. ' + 'по ' + product_price + 'рублей   ' +
            '<a class="delete-item" href="">Удалить</a>'+ '</li>');
        });

    $('.basket-container').mouseover(function(){
         $('.basket-items').removeClass('hidden');
     });

    $('.basket-container').mouseout(function(){
         $('.basket-items').toggleClass('hidden');
     });


    $(document).on('click', 'delete-item', function (e){
        e.preventDefault();
        $(this).closest('li').remove();
    })
});
