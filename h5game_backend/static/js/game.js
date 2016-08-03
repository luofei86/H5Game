function init_answer(answer_id){
	$("#input_answer").val(answer_id);
	$("#next_play").prop('disabled', false);
	$("#next_play").removeClass("btn-disabled");
}

$("#answer_sub_1").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:1,
	    width: "60%",
	    height: "60%"
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_1").attr("answer-value");
	  	init_answer(answer_value);
	  });
	$("#answer_sub_2").animate({
		opacity:0.3,
	    width: "40%",
	    height: "60%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_3").animate({
		opacity:0.3,
	    width: "60%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_4").animate({
		opacity:0.3,
	    width: "40%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
});

$("#answer_sub_2").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:0.3,
	    width: "40%",
	    height: "60%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_2").animate({
		opacity: 1,
	    width: "60%",
	    height: "60%"
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_2").attr("answer-value");
	  	init_answer(answer_value);
	  });
	$("#answer_sub_3").animate({
		opacity: 0.3,
	    width: "40%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_4").animate({
		opacity: 0.3,
	    width: "60%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
});

$("#answer_sub_3").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:0.3,
	    width: "60%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_2").animate({
		opacity:0.3,
	    width: "40%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_3").animate({
		opacity: 1,
	    width: "60%",
	    height: "60%"
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_3").attr("answer-value");
	  	init_answer(answer_value);
	  });
	$("#answer_sub_4").animate({
		opacity:0.3,
	    width: "40%",
	    height: "60%"
	  }, 1000, function() {
	    // Animation complete.
	  });
});

$("#answer_sub_4").on('touchstart', function(){
	$("#next_play").addClass("btn-disabled");
	$("#answer_sub_1").animate({
		opacity:0.3,
	    width: "40%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_2").animate({
		opacity:0.3,
	    width: "60%",
	    height: "40%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_3").animate({
		opacity:0.3,
	    width: "40%",
	    height: "60%"
	  }, 1000, function() {
	    // Animation complete.
	  });
	$("#answer_sub_4").animate({
		opacity: 1,
	    width: "60%",
	    height: "60%"
	  }, 1000, function() {
	  	var answer_value = $("#answer_sub_4").attr("answer-value");
	  	init_answer(answer_value);
	  });
});
