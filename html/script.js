   
   xhrreq = {}

 function generateEquation() {
   const input = document.getElementById('input').value.trim();

   const lines = $('#input').val().split('\n');
   const firstLine = (lines[0] || '').trim();
   const secondLine = (lines[1] || '').trim();

   const coeffs = firstLine.split(/\s+/).map(Number);
   const k = coeffs.length;

   let equation = 'u_{n+' + k + '} = ';
   let terms = coeffs.map((a, i) => {
     const sub = k - 1 - i;
     const absCoeff = Math.abs(a);
     const uTerm = `\\ u_{n${sub > 0 ? '+' + sub : ''}}`;

     return (a < 0 ? `- ${absCoeff}${uTerm}` : `${absCoeff}${uTerm}`);
   });

   equation += terms.join(' + ').replace(/\+\s-\s/g, '- ');

   equation = `\\[${equation}\\]`

   if (secondLine) {
     const commasep = secondLine.replaceAll(" ", ", ")
     equation += `\\[(\\dots,${commasep},\\dots)\\]`;  // Inline style for second line
   }

   // Render using MathJax
   document.getElementById('formattedinput').innerHTML = equation;
   MathJax.typeset(); // Trigger MathJax to render
 }




function errorHandler(errorArea, data) {
   if ('status' in data && data['status'] == 'success') {
      return false
   }
   var error;
   error = 'Something went wrong, but no status message was sent. If the problem persists, please email: skolem@davidpurser.net.';
   if ('error' in data) {
      error = data['error']
   }

   $(errorArea).removeClass('alert-info').addClass('alert-danger').show();
   $(errorArea).html(error);
   return true;
}
           

var urlParams = new URLSearchParams(window.location.search);
if(urlParams.has('bd')) {
   $('input[name=BakerDavenport]').prop('checked', true);
   $('input[name=Leapfrogging]').prop('checked', false);
}
if(urlParams.has('padic')) {
   $('input[name=pAdic]').prop('checked', true);
   $('input[name=Leapfrogging]').prop('checked', false);
}
if(urlParams.has('debug')) {
   $('.debug').removeClass('dnone')
}

  function highlightRef(hash) {
    const $refElem = $(hash);
    if ($refElem.length) {
      $refElem.addClass('highlighted-ref');
      setTimeout(() => {
        $refElem.removeClass('highlighted-ref');
      }, 2000);
    }
  }


$(document).ready(function(){

    // Highlight if the page loads with a hash
    if (window.location.hash) {
      highlightRef(window.location.hash);
    }

    // Highlight if the hash changes after page load
    $(window).on('hashchange', function () {
      highlightRef(window.location.hash);
    });


   $('#input').on('input', generateEquation);
   generateEquation();

   $('button.example').on('click',function(){
      data = $(this).attr('data');
      $('#input').val(data);
      dataObject = $(this).data();
      Object.keys(dataObject).forEach(function(item){
         if (item.startsWith('toggle')){
            value = dataObject[item];
            item = item.replace(/^toggle+/g, "");
            $('input[name=' +  item +']').prop('checked', value);
         }
      });
      generateEquation()

      $('#go').click();
   });

   $('button.toggleExplanation').on('click',function(){
      $('.explanation').toggle();
   });

   function enableSuitableOptions() {
         $('.LeapfroggingOptions').toggle( $('input[name=Leapfrogging]').is(":checked"));
         $('.BakerDavenportOptions').toggle($('input[name=BakerDavenport]').is(":checked"));
         $('.pAdicOptions').toggle( $('input[name=pAdic]').is(":checked"));
   }

   $('input[name=Leapfrogging]').on('change',enableSuitableOptions);
   $('input[name=BakerDavenport]').on('change',enableSuitableOptions);
   $('input[name=pAdic]').on('change',enableSuitableOptions);
   enableSuitableOptions()


   function clean() {
      $('#bdoutput').html("");
      $('#output').html(""); 
      $('#treearea').html("");
      $('#padicoutput').html("");
           
   }

   function startComputation(){
      clean();
      $('.warnings').removeClass('alert-info').addClass('alert-danger').html("").hide()

      $('#info').html("Computing").show();
      $('button:not(.dontdisable)').prop('disabled', true);
      $('.form-switch input').prop('disabled', true);

   }
   function endComputation(){

         var done =  Object.keys(xhrreq).every(x => {
            return xhrreq[x] == null;
         });

         if (done) {
           $('#info').html("").hide();
           $('button').prop('disabled', false);
           $('.form-switch input').prop('disabled', false);
           enableSuitableOptions();
         };
   }

   $('#go').on('click',function(){
      startComputation();

      algorithms = ['BakerDavenport','Leapfrogging','pAdic']

      algorithms.forEach(function(algname) {

         var errorArea = '#' + algname +'Errors';
         if(!$('input[name=' + algname + ']').is(":checked")) {

            $(errorArea).removeClass('alert-danger').addClass('alert-info').html("Not requested").show();
            return
         }

         algdata = {
            val: $('#input').val(),
            options: {}
         }

         $('.globaloptions').each(function(){
            algdata['options'][$(this).attr('name')] = $(this).is(":checked");
         });  


         $('.option' + algname ).each(function(){
            if ($(this).attr('type') == "checkbox"){
               algdata['options'][$(this).attr('name')] = $(this).is(":checked");   
            } else {
               algdata['options'][$(this).attr('name')] = $(this).val();
            }
            
         });  


         algdata['options'][algname] = true;

         xhrreq[algname] = $.ajax({
            url: '/skolem',
            contentType: "application/json",
              dataType: "json",
            type: 'post',
            data: JSON.stringify(algdata),
            success:function(data){
               xhrreq[algname] = null;
               endComputation();


               if ('Leapfrogging' in data) {
                  leapFrogging(errorArea,data, data['Leapfrogging'])
               }
               
               if ('BakerDavenport' in data) {
                  bakerDavenportData = data['BakerDavenport']
                  bakerDavenport(errorArea,data,bakerDavenportData)
               }

               if ('pAdic' in data) {
                  pAdicData = data['pAdic']
                  pAdic(errorArea,data,pAdicData)
               }

            },
            error: function(xhr){
               try {
                     var data = JSON.parse(xhr.responseText);
                     errorHandler(errorArea, data);
                 } catch (error) {
                     errorHandler(errorArea, {'status':'fail'});
                 }
               xhrreq[algname] = null;
               endComputation();
            }
         });
      });
      endComputation();
   });
   

   function stop() {
      Object.keys(xhrreq).forEach(x => {
         if(xhrreq[x] != null) {
            xhrreq[x].abort();
            xhrreq[x] = null;
         }
      });
      endComputation();
   }

   $('#clear').on('click', function(){
      stop();
      $('#input').val('');
   });

   $('#stop').on('click', stop);

});


