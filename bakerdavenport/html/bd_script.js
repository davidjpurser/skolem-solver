
function bakerDavenport(errorArea,globalData,data){
      
      if(errorHandler(errorArea,data)) {
         return 
      }

      var text = "";

      text += 'LRS: ' + data['lrs'] + "\n";

      if (globalData.hasOwnProperty('minimized') && globalData['minimized'] == 'True') {
         text += 'Note: The LRS was minimised.' + "\n";
      }

      text += '================'+ "\n";
      text += 'bound: ' + data['bound'] + "\n";
      if ('boundPos' in data) {
         text += 'boundPos: ' + data['boundPos'] + "\n";
      }
      if ('boundNeg' in data) {
         text += 'boundNeg: ' + data['boundNeg'] + "\n";
      }
      if ('zeros' in data) {
         text += 'zeros: ' + data['zeros'] + "\n";
      }
      if ('listn' in data){
         text += 'listn: ' + data['listn'] + "\n";
      }


      $('#bdoutput').html(text);
}

$(document).ready(function(){
   $('input[name=bidirectional]').on('change',function(){
      if($(this).is(":checked")) {
         $('input[name=reverseLRS]').prop('checked', false);
         $('input[name=reverseLRS]').prop('disabled', true);
      } else {
         $('input[name=reverseLRS]').prop('checked', false);
         $('input[name=reverseLRS]').prop('disabled', false);
      }
   });
   //initially checked
   if($('input[name=bidirectional]').is(":checked")) {
      $('input[name=reverseLRS]').prop('checked', false);
      $('input[name=reverseLRS]').prop('disabled', true);
   } else {
      $('input[name=reverseLRS]').prop('checked', false);
      $('input[name=reverseLRS]').prop('disabled', false);
   }


   $('input[name=boundonly]').on('change',function(){
      if($(this).is(":checked")) {
         $('input[name=listn]').prop('checked', false)
      }
   });

   $('input[name=listn]').on('change',function(){
      if($(this).is(":checked")) {
         $('input[name=boundonly]').prop('checked', false)
      }
   });
});