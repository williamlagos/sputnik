$.fn.clearEvents = function(){
	$(window).off('resize');
	//$('a').off("click");
	
	$('#Canvas').off('mousedown');
	$('#Canvas').off('mouseup');
	$('#Canvas').off('mousemove');
	
	$('.causablespread').off("click");
	$('#selectupload').off("click");
	$('#causeupload').off("submit");
	$('.causable').off("click");
	$('.message').off("click");
	$('.movement,.schedule').off("click");

	$('.spreadablespread').off("click");
	$('.eventspread').off("click");
	$('#spreadpost').off("click");
	$('#eventpost').off("click");
	$('.spreadable,.event').off("click");
	$('.spread').off('click');

	$('#content').off("click");
	$('.playable').off("click");
	$('.video').off("click");
	$('.videoupload').off("click");
	$('#Message').off('click');
	$('.pcontrols').on('click',play.play);
	$('.mute').off('click');
	$('.unmute').off('click');
	$('.fan').off('click');
	$('.deletable').off('click');

	$('.purchase').off("click");
	$('.product').off("click");
	$('.buyable').off("click");
	$('.creation').off("click");
	$('.products').off("click");
	$('.calculate').off("click");
	
	$('.place').off("click");
	$('.new').off("click");
	$('#Direita').off("click");
	$('.social').off("click");
	$('#upload').off("click");
	$('.register').off("click");
	$('.eraseable').off("click");
	$('.select').off("change");
	$('.selection').off("click");
	$('.return').off("click");
	$('#causeupload').off("click");
	
	$('#id_username,#id_email,#id_last_name,#id_first_name,#datepicker').off("keyup");
	$('#datepicker').off("keydown");
	$('#password').off("click");
	$('.mosaic-overlay').off("click");
	$('.loadable').off("click");
	$('.profile').off("click");
	$('.mosaic-block').off("click");
	$('.login').off("click");
	$('.register').off("click");
	$('.who').off("click");
	$('.what').off("click");
	$('.how').off("click");
	$('.filter').off("click");
	$('#explore').off("submit");
	$('.mosaic-overlay').off("click");
	$('.return').off("click");
	$('#play').off("click");
	$('#create').off("click");
	$('#spread').off("click");
	$('.favorites').off("click");
	$('.config').off("click");
	$('.cart').off("click");
	$('.cancel,.close').off("click");
}

$.fn.eventLoop = function(){
	$.fn.clearEvents();
	$('a').on("click",function(){ this.blur(); });
	$(window).on('resize',spin.resizeHelix);

	$('#Canvas').on('mousedown',spin.holdHelix);
	$('#Canvas').on('mouseup',spin.releaseHelix);
	$('#Canvas').on('mousemove',spin.moveHelix);
	
	$('.causablespread').on("click",create.openCausableSpread);
	$('#selectupload').on("click",create.selectVideo);
	$('#causeupload').on("submit",create.submitCause);
	$('.causable').on("click",create.openCausable);
	$('.message').on("click",create.loadListContext);
	$('.movement,.schedule').on("click",create.loadListMosaic);

	$('.spreadablespread').on("click",spread.openSpreadableSpread);
	$('.eventspread').on("click",spread.openEventSpread);
	$('#spreadpost').on("click",spread.submitSpread);
	$('#eventpost').on("click",spread.submitEvent);
	$('.spreadable,.event').on("click",spread.loadTextObject);
	$('.spread').on('click',function(event){
		event.preventDefault();
		related = "<div class=\"time\" style=\"display:none;\">"+$('#Espaco').find('.time').text()+"</div>"
		$.ajax({
			url:'spread',
			beforeSend:function(){ $('#Espaco').Progress() },
			success:function(data){
				$.fn.showDataContext('',data+related);
				$('#Espaco').css({'background':'#222','border-radius':'50px'});
				$('#spreadpost').click(function(event){
					event.preventDefault();
					$.post('spread',{'spread':$('#id_content').val(),'time':$('#Espaco').find('.time').text()},function(data){
						alert(data);
						$('#Espaco').dialog('close');
					});
				});
			}
		});
	});

	$('#content').on("click",play.submitPlay);
	$('.playable').on("click",play.loadPlayObject);
	$('.video').on("click",play.getVideoInformation);
	$('.videoupload').on("click",play.submitContent);
	$('#Message').on('click',play.replay);
	$('.replay').on('click',play.replay);
	$('.mute').on('click',play.mute);
	$('.unmute').on('click',play.unmute);
	$('.play').on('click',play.play);
	$('.pause').on('click',play.pause);
	$('.fan').on('click',function(event){
		event.preventDefault();
		$.get('fan',{'text':$('#Espaco').find('.time').text()},function(data){
			$('#Grade').loadMosaic(data);
			$('#Espaco').dialog('close');
		});
	});
	$('.playlist').on('click',play.playlistObject);
	
	$('.deletable').on('click',$.fn.deleteObject);

	$('.purchase').on("click",store.openDeliverable);
	$('.product').on("click",store.openProduct);
	$('.buyable').on("click",store.buyMoreCredits);
	$('.creation').on("click",store.createNewProduct);
	$('.products').on("click",store.showProducts);
	$('.calculate').on("click",store.calculatePrice);
	
	$('.place').on("click",$.fn.registerPlace);
	$('.new').on("click",$.fn.newItem);
	$('#Direita').on("click",$.fn.showMessage);
	$('.social').on("click",$.fn.gotoSocial);
	$('#upload').on("click",$.fn.input);
	$('.register').on("click",$.fn.loadNewDialog);
	$('.eraseable').on("click",$(this).edit);
	$('.select').on("change",$.fn.changeSelection);
	$('.selection').on("click",$(this).createSelection);
	$('.return').on("click",$.fn.showMenus);
	$('#causeupload').on("click",$(this).tosubmit);
	
	$('#id_username,#id_email,#id_last_name,#id_first_name,#datepicker').on("keyup",$.fn.sendNewField);
	$('#datepicker').on("keydown",$.fn.sendNewField);
	$('#password').on("click",$.fn.submitPasswordChange);
	$('.mosaic-overlay').on("click",$(this).select);
	$('.loadable').on("click",$.fn.loadMoreMosaic);
	$('.profile').on("click",$.fn.loadProfileObject);
	$('.mosaic-block').on("click",function(){ $.e.value = false; });
	$('.login').on("click",$.fn.showLoginView);
	$('.register').on("click",$.fn.showRegisterView);
	$('.who').on("click",$.fn.slideWhoPage);
	$('.what').on("click",$.fn.slideWhatPage);
	$('.how').on("click",$.fn.slideHowPage);
	$('.filter').on("click",explore.selectFilter);
	$('#explore').on("submit",explore.submitSearch);
	$('.mosaic-overlay').on("click",$(this).clickContent);
	$('.return').on("click",function(event){ $.fn.showMenus(); });
	$('#play').on("click",$(this).showContext);
	$('#create').on("click",$(this).showContext);
	$('#spread').on("click",$(this).showContext);
	$('.favorites').on("click",$(this).showMosaic);
	$('.config').on("click",$(this).showContext);
	$('.cart').on("click",store.showProductCart);
	$('.cancel,.close').on("click",$.fn.closeDialog);
}
