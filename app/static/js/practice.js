$(document).ready(function() {
$("#definition").html('')

var answer, word1, word2, word3, trueAnswer = null;



$("#practiseChoose").on("click", "input.word", function(){
    answer =  $(this).val();
    word1 = $("#word1").val()
    word2 = $("#word2").val()
    word3 = $("#word3").val()
    trueAnswer = $("#trueAnswer").val()

});


	$('#practiseForm').on('submit', function(event) {



		$.ajax({
			data :{
			      answer: answer,
                  word1: word1,
                  word2: word2,
                  word3: word3,
                  trueAnswer:trueAnswer
                 },
        type: 'POST',
        url: '/practice'
		})
		.done(function(data) {

		      $('#practiseButton').attr('value', 'Skip');

              $("#definition").html('<h5 class="d-flex justify-content-center">Definition:</h5>'
              +'<div  class="alert alert-dark d-flex justify-content-center">'+data.definition+'</div>')


            $("#practiseChoose").html('<div class="d-flex justify-content-center">'+
            '<span class="p-2"><input  type="submit" class="word btn btn-primary" name="answer" id="word1" value='+data.words[0]+'></span>'+
            '<span class="p-2"> <input type="submit" class="word btn btn-primary" name="answer" id="word2" value='+data.words[1]+'></span>'+
            '<span class="p-2"> <input type="submit" class="word btn btn-primary" name="answer" id="word3" value='+data.words[2]+'></span>'+
            '<input type="hidden" id="trueAnswer" value="'+data.trueAnswer+'"/></div>')


if('word' in data.pastData)
{
            if( data.pastData.word == data.pastData.answer)
            {
                 $("#feedback").html('<div class="d-flex justify-content-center" >'+
                  '<p style="color:green">You earned 1 practice point for word <b>'+data.pastData.word+'</b></p></div>')

            }
            else
            {
                $("#feedback").html('<div class="d-flex justify-content-center">'+
                  '<p style="color:red">Wrong answer, true answer: <b>'+data.pastData.word+'</b></div></p>')
            }



}
else{
$("#feedback").html('')
}
		});

		event.preventDefault();

	});


});