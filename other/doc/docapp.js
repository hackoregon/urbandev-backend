document.addEventListener("DOMContentLoaded", function() {
   /* Dynamically add a <style> tag to the head */
   var ss = document.createElement("link");
   ss.type = "text/css";
   ss.rel = "stylesheet";
   ss.href = "/css/more_doc_styles.css";
   document.getElementsByTagName("head")[0].appendChild(ss);
});
