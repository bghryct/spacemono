$('#slider-ital').on('input', function(){
	$('#slider-ITA2').val($('#slider-ital').val())
	$('#slider-ITA2').trigger("input");
	$('#slider-ITA3').val($('#slider-ital').val())
	$('#slider-ITA3').trigger("input");
})