  function add_ok(count) {
            var $add_x = $('#add_cart').offset().top;
            var $add_y = $('#add_cart').offset().left;

            var $to_x = $('#show_count').offset().top;
            var $to_y = $('#show_count').offset().left;

            $('.add_jump').css({left: $add_y + 80, top: $add_x + 10, display: 'block'})
                .stop()
                .animate({left: $to_y + 7, top: $to_x + 7}, 'fast', function () {
                    $('.add_jump').fadeOut('fast', function () {
                        $('#show_count').html(count)
                    })
                })
        }

        $(function () {
            $('.add').click(function () {
                var num = parseInt($('.num_show').val());
                num++;
                $('.num_show').val(num).blur();
            });

            $('.minus').click(function () {
                var num = parseInt($('.num_show').val());
                num--;
                $('.num_show').val(num).blur();
            });


            $('.num_show').blur(function () {
                var num = parseInt($(this).val());
                if (isNaN(num) || num <= 1) {
                    num = 1;
                }
                if (num >= {{ g.gkucun }}) {
                    num = '{{ g.gkucun }}';
                }

                $(this).val(num);
                var price = parseFloat($('.show_pirze em').html());
                var total = price * num;
                $('.total em').html(total.toFixed(2) + '元')
            });


            $('#add_cart').click(function () {
                $.get('/cart/add/', {'gid': '{{ g.id }}', 'count': $('.num_show').val()}, function (data) {
                    if (data.isNotLogin == 1) {
                        location.href = '{% url "login" %}'
                    }
                    console.log(data.count);
                    console.log(data);
                    add_ok(data.count);
                })
            })

        })