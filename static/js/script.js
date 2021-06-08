// jQuery for MaterializeCSS initialization

$(document).ready(function(){
  $('.sidenav').sidenav({edge: "right"});
  $('.slider').slider(
    {
      indicators: true,
      interval: 6000,
      duration: 800,
      height: 450
    }
  );
});