$(document).ready(function() {

    // navigation hide and Show
    $(window).scroll(function(){
      var scroll = $(window).scrollTop();
      if (scroll>48 && scroll<600){
        $('#nav-wrap').fadeOut("fast");
      }
      else{
        $('#nav-wrap').fadeIn("fast");
          if(scroll>600){
            $('#nav-wrap').css('background','#022f46');
          }
          else{
            $('#nav-wrap').css('background','#022f46');
          }
        }
    })

})