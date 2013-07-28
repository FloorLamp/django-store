(function() {
    $('.product-display button').on('click', function() {
        var $this = $(this)
          , $added = $('#added-product');
        $.ajax({
            url: '/modify_cart',
            type: 'POST',
            data: {
                id: $this.data('id'),
                action: 'add',
                csrfmiddlewaretoken: csrftoken
            }
        }).then(function(data) {
            $added.find('img').attr('src', $this.data('image'));
            $added.find('p').text($this.data('name'));
            $added.fadeIn(function() {
                setTimeout(function() {
                    $added.fadeOut();
                }, 3000);
            });
        });
    });
    
    $('#cart .delete-product').on('click', function() {
        var $row = $(this).parents('li');
        $.ajax({
            url: '/modify_cart',
            type: 'POST',
            data: {
                id: $(this).data('id'),
                action: 'delete',
                csrfmiddlewaretoken: csrftoken
            }
        }).then(function(data) {
            $row.fadeOut(function() {
                $row.remove();
                updateTotal();
            });
        });
    });
    
    $('#cart .count-input').on('input', function() {
        var $this = $(this)
          , $button = $this.next('button')
          , value = $this.val();
        if (/^[0-9]+$/.test(value) && parseInt(value) > 0) {
            $button.fadeIn();
        } else {
            $button.fadeOut();
        }
    });
    
    $('#cart .update-product').on('click', function() {
        var $this = $(this);
        $.ajax({
            url: '/modify_cart',
            type: 'POST',
            data: {
                id: $(this).data('id'),
                action: 'update',
                count: $this.prev('input').val(),
                csrfmiddlewaretoken: csrftoken
            }
        }).then(function(data) {
            $this.fadeOut();
            updateTotal();
        });
    });
    
    function updateTotal() {
        var $counts = $('.count-input')
          , $price = $('#total-price')
          , price = 0;
        
        if ($counts.length) {
            $counts.each(function() {
                var $this = $(this);
                price += parseInt($this.val()) * parseFloat($this.data('price'));
            })
            $price.text(price.toFixed(2));
        } else {
            $('.list-group').after('Your cart is empty.').remove();
        }
    }
})();