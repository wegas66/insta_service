//РјРµРЅСЋ
$('document').ready(function(){
    var removed = false;

    $(window).scroll(function () {
        if ($(this).scrollTop() > 20){
            if (!removed) {
                $('.navbar').removeClass("navbar1").addClass("navbar2");
            }
            removed = true;
        }
        else{
            if (removed) {
                $('.navbar').removeClass("navbar2").addClass("navbar1");
            }
            removed = false;
        }
    });

    $('#signupModal').on('show.bs.modal', function (event) {
	    var priceId = $(event.relatedTarget).data('price');

	    var $pricaInput = $(this).find('input[name="price"]');

	    $pricaInput.val(priceId ? priceId : '');
    });
});

