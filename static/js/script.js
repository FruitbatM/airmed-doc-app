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


// Back to Top Arrow - code with modification taken from: https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
mybutton = document.getElementById('arrow_2top');

// When the user scrolls down 50px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50|| document.documentElement.scrollTop > 50) {
    mybutton.style.display = 'block';
  } else {
    mybutton.style.display = 'none';
  }
}

// When the user clicks on the button, scroll to the top of the page
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

// Tooltip
// Code source: https://getbootstrap.com/docs/4.6/components/tooltips/-->
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});