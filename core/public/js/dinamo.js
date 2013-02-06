Array.prototype.removeItem = function(str) {
   	for(i=0; i<this.length ; i++){
     	if(escape(this[i]).match(escape(str.trim()))){
       		this.splice(i, 1);  break;
    	}
	}
	return this;
}

$.fn.drawSVG = function(url,width,height){
	element = $(this).attr('id');
	$.ajax({
		url:url,
		dataType:'xml',
		success:function(xml){
			document.getElementById(element).width = width;
			document.getElementById(element).height = height;
			ctx = document.getElementById(element).getContext('2d');
			ctx.save();
			ctx.drawSvg(url,0,0,width,height);
			ctx.restore();
		}
	});
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
		if($(this).attr('class') == 'overlay selected'){
			$.e.objects.removeItem(time);
			$(this).attr('style','background:black; display: inline;')
			$(this).attr('class','overlay');
		}else{
			$(this).attr('style','background:red; display: inline;')
			$(this).attr('class','overlay selected');
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