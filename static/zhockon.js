Array.prototype.removeItem = function(str) {
   	for(i=0; i<this.length ; i++){
     	if(escape(this[i]).match(escape(str.trim()))){
       		this.splice(i, 1);  break;
    	}
	}
	return this;
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