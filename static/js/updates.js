
/* AJAX UPDATE HAS NOT BEEN IMPLENTED 
If we want to reload values without reloading page
This is an example found online...*/

$(function(){

	$('button').click(function(){
		var user = $('#inputUsername').val();
        var pass = $('#inputPassword').val();
        
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
            type: 'POST',
            
			success: function(response){
				console.log(response);
            },
            
			error: function(error){
				console.log(error);
			}
		});
	});
});