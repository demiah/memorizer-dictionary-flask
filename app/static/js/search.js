var word = ''
$(document).ready(function() {

	$('#searchForm').on('submit', function(event) {
	word = $("#wordInput").val()
    {
        $("#box").html("");
    }
		$.ajax({
			data : {
        word: $('#wordInput').val()
        },
        type: 'POST',
        url: '/search'
		})
		.done(function(data) {
		    if(data.error){

		     $("#wordForm").html('<p class="d-flex justify-content-center" style="color:red"><b>Error, try again</b></p>');
		    }

		    else {

		    if(data.isWordAdded){
               $("#wordForm").html('<p class="d-flex justify-content-center"><button class="btn btn-danger" type="submit">Delete Word</button></p>');
		    }
		    else{
		       $("#wordForm").html('<p class="d-flex justify-content-center"><button class="btn btn-success" type="submit">Save Word</button></p>');
		    }

			$("#box").append('<p class="d-flex justify-content-center"><b>'+data.word+'</b></p>');
			$("#box").append('<p class="d-flex justify-content-center">Total&nbsp;<b class="d-flex justify-content-center">'+data.definition.length+'</b>&nbsp;definition</p>');
			$("#wordForm").append('<input type="hidden" id="#wordBox" value='+data.word+'/>');

        for(let i=0; i<data.definition.length; i++)
            $("#box").append('<p class="d-flex justify-content-center">'+data.definition[i]+'</p>');}
		});

		event.preventDefault();

	});


});





$(document).ready(function() {

	$('#wordForm').on('submit', function(event) {

		$.ajax({
			data : {
        word: word
        },
        type: 'POST',
        url: '/process'
		})
		.done(function(data) {


        if(data.isWordAdded){
               $("#wordForm").html('<p class="d-flex justify-content-center"><button class="btn btn-danger" type="submit">Delete Word</button></p>');
		    }
		    else{
		       $("#wordForm").html('<p class="d-flex justify-content-center"><button class="btn btn-success" type="submit">Save Word</button></p>');
		    }
		});

		event.preventDefault();

	});

});