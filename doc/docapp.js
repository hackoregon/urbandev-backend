/* Might be better to just dynamically add a <style> tag to the head */
document.addEventListener("DOMContentLoaded", function() {
      var i = 0;
      
      // Style all the method titles
      var elts = document.getElementsByTagName('h4');
      for(i=0; i<elts.length; i++) {
         elts[i].style.color = '#b24';
      }
      
      // Style all the method parameters
      var elts2 = document.querySelectorAll("li p strong");
      for(i=0; i<elts2.length; i++) {
         elts2[i].style.color = '#084';
      }
      
      // Style the main title
      document.getElementsByTagName('h1')[0].style.color = '#15d';
});