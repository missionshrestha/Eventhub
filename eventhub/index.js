
$(".navbar-brand").hover(function() {
  $(".navbar-logo-img").css("transform","scale(1.1)");
  $(".navbar-logo-img").css("opacity","1");

}, function(){
  $(".navbar-logo-img").css("transform","");
  $(".navbar-logo-img").css("opacity","");

}
);


$(".foot-icon").hover(function() {

  $(this).css("opacity","1");
$(this).css("transform","scale(1.2)");

}, function(){
  $(".foot-icon").css("opacity","");
$(this).css("transform","");
}
);
