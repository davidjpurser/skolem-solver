$(document).ready(function(){
       $('#treearea').on('click','button',function(event){
               event.stopPropagation();
               $(this).parent().find('ul').first().toggle();
            });
            $('#treearea').on('click','ul',function(event){
               event.stopPropagation();
            });
            $('#treearea').on('click','li',function(event){
               event.stopPropagation();
               $('#treearea li').css('background-color','');
               $(this).css('background-color','orange');

               var object = $(this).data('object');
               var level = $(this).data('level');
               var val  = "";
               if (object['type'] == 'modm') {
                  val = val + "================\n";
                  val = val + "LRS: " +object['lrs'] +   "\n";
                   val = val + "================\n";
                  if (level != 0){
                     val = val + "Linear subset of root LRS: " +object['linearOfFullSet'] +   "\n";
                     if (level!= 1){
                        val = val + "Linear subset of parent LRS: " +object['linearOfParent'] +   "\n";
                     }
                  } else {
                     val = val + "This is the root LRS\n";
                  }
                  val = val + "================\n";
                  val = val + "LRS used: " +object['actualLrs'] +   "\n";
                  val = val + "================\n";
                  val = val + "LRS used is non-zero modulo: " +object['modm'] +   "\n";
                  val = val + "Periodic sequence modulo " + object['modm'] +": " +object['repmodm'] +   "\n";
                  val = val + "Period length: " + object['repmodmlen'] +   "\n";
                  
               } else if (object['type'] == 'split') {
                  val = val + "================\n";
                  val = val + "LRS: " +object['lrs'] +   "\n";
                     val = val + "================\n";
                  if (level != 0){
                  
                     val = val + "Linear subset of root LRS: " +object['linearOfFullSet'] +   "\n";
                     if (level!= 1){
                        val = val + "Linear subset of parent LRS: " +object['linearOfParent'] +   "\n";
                     }
                  } else {
                     val = val + "This is the root LRS\n";
                  }
                  val = val + "================\n";
                  val = val + "LRS used: " +object['actualLrs'] +   "\n";
                  val = val + "================\n";
                  val = val + "There is a zero at: " +object['zero'] +   "\n";
                  val = val + "Sufficient jump: " +object['jump'] +   "\n";
                  val = val + "Prime used is: " +object['prime'] +   "\n";
                  if (level != 0){
                     val = val + "In root LRS corresponds to zero at: " +object['realzero'] +   "\n";
                  }
                  val = val + "================\n";
                  val = val + "We consider the following "  + object['jump'] + " subsequences of LRS\n";
                  val = val + "of the form (i+ " + object['jump'] +  "ℤ) for i = 0, ..., " + (parseInt(object['jump'])-1) + "\n"

                  val = val +  (parseInt(object['zero'])) + "+" + object['jump'] + "ℤ splits as " + (parseInt(object['zero'])) + " (which is zero) and "  + object['zero'] + "+" + object['jump'] + "ℤ<sub>≠0</sub> (which has no zeros)\n"
                  val = val + "================\n";

                  val = val +  object["reasoning"] + "\n";

                  val = val + "================\n";
                  
                  val = val + "We test the remainder:\n"
                  object['children'].forEach(function($child) {
                     if ($child['type'] != 'padic-non-zero'){
                        val = val + $child['linearOfParent'] + " must be tested\n";
                     }
                  });

               }  else if (object['type'] == 'padic-non-zero') {
                  val = val + "================\n";
                  val = val + "LRS: not computed (no computations required)\n";
                  val = val + "================\n";
                  if (level != 0){
                     val = val + "Linear subset of root LRS: " +object['linearOfFullSet'] +   "\n";
                     if (level!= 1){
                        val = val + "Linear subset of parent LRS: " +object['linearOfParent'] +   "\n";
                     }
                  } else {
                     val = val + "This is the root LRS\n";
                  }
                  val = val + "================\n";
                  val = val + "There is no zero due to padic argument: \n"
                  val = val + "Because there is a zero at " + object['zero'] +  " and jump "  + object['jump'] + " in parent \n"
                  val = val + "See parent (click Zero at ...) above for further details\n";
                 
               }


              $('#output').html(val); 


            })

});


function leapFrogging(errorArea,globalData,data) {

   if(errorHandler(errorArea, data)) {
         return 
   }

   resultTree = data['resultTree']

   $('#treearea').html($('<ul>').html(getListItem(resultTree,0)));

   if (globalData.hasOwnProperty('minimized') && globalData['minimized'] == 'True') {
      $('#treearea').prepend("<br> Note: The LRS was minimised.");
   }

   if (data['zeros'].length > 0){
      $('#treearea').prepend("Zeros: " + data['zeros'].join(", "));
   } else {
      $('#treearea').prepend("Zeros: None ");
   }
   $('#output').html('👈 click on each subsequence on left for more information.');
}

getListItem = function(object, level){

   var item = $('<li>');
   

   item.data('object',object)
   item.data('level',level)

   
   if (object['type'] == 'split') { 

      var stuff = "Zero at " + object['realzero'] + " in "
      stuff = stuff +  object['linearOfFullSet'];
      if (object['linearOfFullSet'] != object['linearOfParent']) {
         stuff = stuff +  " (" + object['linearOfParent'] + " of parent)";
      }
      item.append(stuff);

      item.append($('<button>').html('hide/show').addClass('btn btn-primary btn-sm'));


      var ul = $('<ul>');
      object['children'].forEach(function(child){
         ul.append(getListItem(child, level+1))
      });
      item.append(ul)
   }

   if (object['type'] == 'padic-non-zero') {

      var stuff = "p-adic non-zero in " 
      stuff = stuff + object['linearOfFullSet'];
      if (object['linearOfFullSet'] != object['linearOfParent']) {
         stuff = stuff +  " (" + object['linearOfParent'] + " of parent)";
      }
      item.append(stuff);

   }

   if (object['type'] == 'modm') {
      var stuff = "Non-zero mod " + object['modm'];
      if (!object['isSame']) {
         stuff = stuff +  "·GCD";
      }
      if (level != 0) {
         stuff = stuff +  " in " 
         stuff = stuff + object['linearOfFullSet'];
         if (level != 1) {
            stuff = stuff +  " (" + object['linearOfParent'] + " of parent)";
         }
      }
      item.append(stuff);

   }
   return item;
}