// # Twitter Bootstrap modal responsive fix by @niftylettuce
//  * resolves #407, #1017, #1339, #2130, #3361, #3362, #4283
//   <https://github.com/twitter/bootstrap/issues/2130>
//  * built-in support for fullscreen Bootstrap Image Gallery
//    <https://github.com/blueimp/Bootstrap-Image-Gallery>

// **NOTE:** If you are using .modal-fullscreen, you will need
//  to add the following CSS to `bootstrap-image-gallery.css`:
//
//  @media (max-width: 480px) {
//    .modal-fullscreen {
//      left: 0 !important;
//      right: 0 !important;
//      margin-top: 0 !important;
//      margin-left: 0 !important;
//    }
//  }
//

var adjustModal = function($modal) {
  var top;
  if ($(window).width() <= 480) {
    if ($modal.hasClass('modal-fullscreen')) {
      if ($modal.height() >= $(window).height()) {
        top = $(window).scrollTop();
      } else {
        top = $(window).scrollTop() + ($(window).height() - $modal.height()) / 2;
      }
    } else if ($modal.height() >= $(window).height() - 10) {
      top = $(window).scrollTop() + 10;
    } else {
      top = $(window).scrollTop() + ($(window).height() - $modal.height()) / 2;
    }
  } else {
    top = '50%';
    if ($modal.hasClass('modal-fullscreen')) {
      $modal.stop().animate({
          marginTop  : -($modal.outerHeight() / 2)
        , marginLeft : -($modal.outerWidth() / 2)
        , top        : top
      }, "fast");
      return;
    }
  }
  $modal.stop().animate({ 'top': top }, "fast");
};

var show = function() {
  var $modal = $(this);
  adjustModal($modal);
};

var checkShow = function() {
  $('.modal').each(function() {
    var $modal = $(this);
    if ($modal.css('display') !== 'block') return;
    adjustModal($modal);
  });
};

var modalWindowResize = function() {
  $('.modal').not('.modal-gallery').on('show', show);
  $('.modal-gallery').on('displayed', show);
  checkShow();
};

$(modalWindowResize);
$(window).resize(modalWindowResize);
$(window).scroll(checkShow);

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