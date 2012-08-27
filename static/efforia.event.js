$.fn.clearEvents = function(){
	$(window).off('resize');
	
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
	$('.moreproducts').off("click");
	$('.cancelpurchase').off("click");
	$('.deliver').off("click");
	$('.payment').off("click");
	
	$('.place').off("click");
	$('.new').off("click");
	$('#Direita').off("click");
	$('.social').off("click");
	$('#upload').off("click");
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
	$('.submit').off('click');
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
	$('.pledge').on('click',create.pledgeCause);
	$('.dopledge').on('click',create.transferPledge);
	$('.invests').on('click',create.showInvests);

	$('.spreadablespread').on("click",spread.openSpreadableSpread);
	$('.eventspread').on("click",spread.openEventSpread);
	$('#spreadpost').on("click",spread.submitSpread);
	$('#eventpost').on("click",spread.submitEvent);
	$('.spreadable,.event').on("click",spread.loadTextObject);
	$('.spread').on('click',spread.showSpread);
	$('.spreadspread').click(spread.spreadSpreadable);

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
	$('.fan').on('click',play.fan);
	$('.playlist').on('click',play.playlistObject);
	$('.monetize').on('click',play.monetizeVideo);
	
	$('.deletable').on('click',$.fn.deleteObject);

	$('.purchase').on("click",store.openDeliverable);
	$('.product').on("click",store.openProduct);
	$('.buyable').on("click",store.buyMoreCredits);
	$('.creation').on("click",store.createNewProduct);
	$('.products').on("click",store.showProducts);
	$('.calculate').on("click",store.calculatePrice);
	$('.moreproducts').on("click",store.showMoreProducts);
	$('.cancelpurchase').on("click",store.cancelPurchase);
	$('.deliver').on("click",store.calculateDelivery);
	$('.payment').on("click",store.pay);
	
	$('.place').on("click",$.fn.showPlaceView);
	$('.new').on("click",$(this).newSelection);
	$('#Direita').on("click",$.fn.showMessage);
	$('.social').on("click",$.fn.gotoSocial);
	$('#upload').on("click",$.fn.input);
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
	$('.submit').on('click',function(event){ $('form').tosubmit(event); });
	
	$('.cancel,.close').on("click",$.fn.closeDialog);
	$('.mosaic-block').on("click",function(){ $.e.value = false; });
	$('.login').on("click",$.fn.showLoginView);
	$('.register').on("click",$.fn.showRegisterView);
	$('.who').on("click",$.fn.slideWhoPage);
	$('.what').on("click",$.fn.slideWhatPage);
	$('.how').on("click",$.fn.slideHowPage);
	$('.about').on("click",$.fn.showAbout);
	$('.terms').on("click",$.fn.showTerms);
	$('.copyright').on("click",$.fn.showCopyright);
	$('.rules').on("click",$.fn.showRules);
	$('.contact').on("click",$.fn.showContact);
}
