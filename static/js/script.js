// jQuery for MaterializeCSS initialization

$(document).ready(function(){
  $('select').formSelect();

  $('.collapsible').collapsible();

  $('.parallax').parallax();

  // Modal cannot be closed by clicking anywhere outside the modal itself
  $('.modal').modal(
    {
      dismissible: false,
    }
  );

  // Datepicker for contact form
  $('.datepicker').datepicker(
    {
      autoClose: true,
      yearRange: [2021,2023],
      disableWeekends: true,
      closeOnSelect: true,
      setDefaultDate: true
    }
  );

  $('.dropdown-trigger').dropdown(
    {
      coverTrigger: false
    }
  );
  
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

