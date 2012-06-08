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