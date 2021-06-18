// jQuery for MaterializeCSS initialization

$(document).ready(function(){
  $('select').formSelect();

  $('.parallax').parallax();

  $('.dropdown-trigger').dropdown({
      coverTrigger: false
  });
  
  $('.sidenav').sidenav(
    {
      edge: "right",
      draggable: true,
    });

  $('.slider').slider(
    {
      indicators: true,
      interval: 6000,
      duration: 800,
      height: 450
    }
  );

  $('.datepicker').datepicker(
    {
      autoClose: true
    });

    // Carousel Slider autoplay
    $('.carousel.carousel-slider').carousel({
      fullWidth: true,
      padding: 200,
      height: 450
    }, 
    setTimeout(autoplay, 5000));
   
    function autoplay() {
      $('.carousel').carousel('next');
      setTimeout(autoplay, 5000);
    }
});
