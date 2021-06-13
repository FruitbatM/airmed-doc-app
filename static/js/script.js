// jQuery for MaterializeCSS initialization

$(document).ready(function(){
  $(".dropdown-trigger").dropdown();

  $('select').formSelect();
  
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
});
