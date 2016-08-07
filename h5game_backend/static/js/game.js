function init_answer(answer_id){
	$("#input_answer").val(answer_id);
	$("#next_play").prop('disabled', false);
	$("#next_play").removeClass("disabled");
	$("#img_next_play_disabled").hide();
	$("#img_next_play_enabled").show();
}

$("#answer_sub_1").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:1
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_1").attr("answer-value");
	  	init_answer(answer_value);
	  });
	$("#answer_sub_2").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_3").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_4").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
});

$("#answer_sub_2").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_2").animate({
		opacity: 1
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_2").attr("answer-value");
	  	init_answer(answer_value);
	  });
	$("#answer_sub_3").animate({
		opacity: 0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_4").animate({
		opacity: 0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
});

$("#answer_sub_3").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_2").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_3").animate({
		opacity: 1
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_3").attr("answer-value");
	  	init_answer(answer_value);
	  });
	$("#answer_sub_4").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
});

$("#answer_sub_4").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_2").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_3").animate({
		opacity:0.3
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_4").animate({
		opacity: 1
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_4").attr("answer-value");
	  	init_answer(answer_value);
	  });
});
