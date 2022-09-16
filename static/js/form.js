$(document).ready(function() {

	$('form').on('submit', function(event) {
                $('#formcontainer').hide();
		$.ajax({
			data : {
				text : $('#textInput').val(),
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#formcontainer').show();
                                $('#textInput').val('');

			}
			else {
			}

		});

		event.preventDefault();

	});

});
