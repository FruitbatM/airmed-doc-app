// jQuery for MaterializeCSS initialization

$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.carousel').carousel(
      {
        dist: 0,
        padding: 0,
        fullWidth: true,
        indicators: true,
        duration: 200,
      }
      );
  });

  // auto-play functionality with delay of 5 seconds
  function autoplay() {
    $('.carousel').carousel('next');
    setTimeout(autoplay, 5000);
   }    
   setTimeout(autoplay, 5000);