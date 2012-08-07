Array.prototype.removeItem = function(str) {
   	for(i=0; i<this.length ; i++){
     	if(escape(this[i]).match(escape(str.trim()))){
       		this.splice(i, 1);  break;
    	}
	}
	return this;
}

$.fn.animationFrame = function(){
	if (!$(this).requestAnimationFrame) {
		$(this).requestAnimationFrame = (function() 
		{
			return $(this).webkitRequestAnimationFrame 	|| 	
				   $(this).mozRequestAnimationFrame 		|| 	
			       $(this).oRequestAnimationFrame 		|| 	
				   $(this).msRequestAnimationFrame	 	||
				   function(callback,element)
				   { 
				   		$(this).setTimeout(callback,1000/60); 
				   };
	  	})();
	}
}

$.fn.translate2D = function(x,y){
	$(this).css({'-webkit-transform':'translate('+x+'px,'+y+'px)'});
	$(this).css({'-moz-transform':'translate('+x+'px,'+y+'px)'});
	$(this).css({'-o-transform':'translate('+x+'px,'+y+'px)'});
	$(this).css({'transform':'translate('+x+'px,'+y+'px)'});	
	if(navigator.appName == 'Microsoft Internet Explorer') 
		if(navigator.appVersion.indexOf('MSIE 10.0') != -1)
			$(this).css({'-ms-transform':'translate('+x+'px,'+y+'px)'});
		else
			$(this).animate({'margin-top':y});
	else if(navigator.appName == 'Android') 
		$(this).animate({'margin-top':y});
}

$.fn.rotate2D = function(a){
	$(this).css({'-webkit-transform':'rotate('+a+'deg)'});
	$(this).css({'-moz-transform':'rotate('+a+'deg)'});
	$(this).css({'-o-transform':'rotate('+a+'deg)'});
	$(this).css({'transform':'rotate('+a+'deg)'});	
	if(navigator.appName == 'Microsoft Internet Explorer') 
		if(navigator.appVersion.indexOf('MSIE 10.0') != -1)
			$(this).css({'-ms-transform':'rotate('+a+'deg)'});
}

$.fn.scale2D = function(r){
	$(this).css({'-webkit-transform':'scale('+r+')'});
	$(this).css({'-moz-transform':'scale('+r+')'});
	$(this).css({'-o-transform':'scale('+r+')'});
	$(this).css({'transform':'scale('+r+')'});	
	if(navigator.appName == 'Microsoft Internet Explorer') 
		if(navigator.appVersion.indexOf('MSIE 10.0') != -1)
			$(this).css({'-ms-transform':'scale('+r+')'});
}


$.fn.tosubmit = function(event){
	event.preventDefault();
	$(this).submit();
}

$.fn.input = function(event){
	event.preventDefault();
	$('input:file').click(); 
}

$.fn.redirect = function(event){
	event.preventDefault();
	window.location = $(this).attr('href');
}

$.fn.select = function(event){
	event.preventDefault();
	if($.e.selection){
		time = $(this).find('.time').text();
		if($(this).attr('class') == 'mosaic-overlay selected'){
			$.e.objects.removeItem(time);
			$(this).attr('style','background:url(../images/bg-black.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay');
		}else{
			$(this).attr('style','background:url(../images/bg-red.png); display: inline; opacity: 0;')
			$(this).attr('class','mosaic-overlay selected');
			$.e.objects.push(time);
		}
	}
}

$.fn.edit = function(event){
	event.preventDefault();
	if(!$(this).hasClass('erased')){
		$(this).attr('value','');
		$(this).addClass('erased');
	}
}