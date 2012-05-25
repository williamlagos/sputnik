$.fn.translate2D = function(x,y){
	$(this).css({'-webkit-transform':'translate('+x+'px,'+y+'px)'});
	$(this).css({'-moz-transform':'translate('+x+'px,'+y+'px)'});
	$(this).css({'-o-transform':'translate('+x+'px,'+y+'px)'});
	$(this).css({'transform':'translate('+x+'px,'+y+'px)'});	
	if(navigator.appName == 'Microsoft Internet Explorer') 
		$(this).animate({'margin-top':y});
		//$(this).css({'-ms-transform':'translate('+x+'px,'+y+'px)'});
}