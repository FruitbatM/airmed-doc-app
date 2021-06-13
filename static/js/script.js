// jQuery for MaterializeCSS initialization

$(document).ready(function(){
  $('select').formSelect();
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
});
