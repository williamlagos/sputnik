$.fn.clearEvents = function(){
	$('.app').off('click');
	$('.pages').off('click');
	$('.login').off('click');
	$('.option').off('click');
	$('.upload').off('click');
	$('.procfg').off('click');
	$('.placecfg').off('click');
	$('.controlcfg').off('click');
	$('.change').off('click');
	$('.integration').off('click');
	$('.deletable').off('click');
	
	$('.pledge').off('click');
	$('.spreaded').off('click');
	$('.objectspread').off('click');
	$('.uploadspread').off('click');
	$('.videospread').off('click');
	$('.imagespread').off('click');
	$('.eventspread').off('click');
	$('.postspread').off('click');
	$('.pagespread').off('click');
	$('.listspread').off('click');
	$('.spreadable').off('click');
	$('.playable').off('click');
	$('.event').off('click');
	$('.image').off('click');
	$('.page').off('click');
	$('.spread').off('click');
	
	$('.objectpledge').off('click');
	$('.pledge').off('click');
	$('.promoted').off('click');
	$('.movementcreate').off('click');
	$('.keyword').off('click');
	$('.promote').off('click');
	$('.objectpromote').off('click');
	$('.promote').off('click');
	$('.movement').off('click');
	$('.causable').off('click');
	$('.projectcreate').off('click');
	$('.linkcreate').off('click');
	
	$('#Canvas')
	.off('mousedown').off('mouseup').off('mousemove');

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
	$('.social').off("click");
	$('.eraseable').off("click");
	$('.select').off("change");
	$('.selection').off("click");
	$('.back').off("click");
	
	$('#password').off("click");
	$('.overlay').off("click");
	$('.loadable').off("click");
	$('.profile').off("click");
	$('.block').off("click");
	$('.login').off("click");
	$('.register').off("click");
	$('.who').off("click");
	$('.what').off("click");
	$('.how').off("click");
	$('.filter').off("click");
	$('#explore').off("submit");
	$('.back').off("click");
	$('.favorites').off("click");
	$('.cart').off("click");
	$('.submit').off('click');
	$('.cancel,.close').off("click");
	$('.unfan').off('click');
	$('.profilefan').off('click');
	$('.logout').off('click');
}

$.fn.eventLoop = function(){
	$.fn.clearEvents();
	
	$('a').on('click',function(){ this.blur(); });
	$('.app').on('click',$(this).showContext);
	$('.pages').on('click',$(this).showPage);
	$('.login').on('click',$.fn.authenticate);
	$('.option').on('click',$(this).changeOption);
	$('.upload').on('click',$.fn.input);
	$('.procfg').on('click',$.fn.submitChanges);
	$('.placecfg').on('click',$.fn.submitPlace);
	$('.controlcfg').on('click',$.fn.submitControl);
	$('.change').on('click',$.fn.doNothing);
	$('.integration').on('click',$(this).redirect);
	$('.deletable').on('click',$.fn.deleteObject);

	$('.spreaded').on('click',spread.showSpreaded);
	$('.objectspread').on('click',spread.spreadObject);
	$('.uploadspread').on('click',play.submitContent);
	$('.videospread').on('click',play.submitVideoInfo);
	$('.imagespread').on('click',spread.submitImage);
	$('.eventspread').on('click',spread.submitEvent);
	$('.postspread').on('click',spread.submitSpread);
	$('.pagespread').on('click',spread.submitPage);
	$('.spreadable').on('click',spread.showSpreadable);
	$('.playable').on('click',play.showPlayable);
	$('.event').on('click',spread.showEvent);
	$('.image').on('click',spread.showImage);
	$('.page').on('click',spread.showPageEdit);
	$('.pagesave').on('click',spread.savePage);
	$('.spread').on('click',spread.spreadSpread);
	$('#Espaco').on('hide',play.hidePlayable);

	$('#Canvas')
	.on('mousedown',spin.holdHelix)
	.on('mouseup',spin.releaseHelix)
	.on('mousemove',spin.moveHelix);
	
	$('.objectpledge').on('click',create.transferPledge);
	$('.pledge').on('click',create.pledgeProject);
	$('.promoted').on('click',create.showPromoted);
	$('.movementcreate').on('click',create.submitMovement);
	$('.keyword').on('click',create.selectKeyword);
	$('.promote').on('click',create.promoteProject);
	$('.objectpromote').on('click',create.promoteObject);
	$('.project').on('click',create.showProject);
	$('.movement').on('click',create.showMovement);
	$('.projectcreate').on('click',create.submitCause);
	$('.linkcreate').on('click',create.submitVideo);
	
	$('.invests').on('click',create.showInvests);
	
	$('#content').on("click",play.submitPlay);
	$('.video').on("click",play.getVideoInformation);
	$('.playlist').on('click',play.playlistObject);
	$('.monetize').on('click',play.monetizeVideo);

	$('.purchase').on("click",store.openDeliverable);
	$('.product').on("click",store.openProduct);
	$('.buyable').on("click",store.buyMoreCredits);
	$('.submitproduct').on("click",store.submitProduct);
	$('.products').on("click",store.showProducts);
	$('.calculate').on("click",store.calculatePrice);
	$('.moreproducts').on("click",store.showMoreProducts);
	$('.cancelpurchase').on("click",store.cancelPurchase);
	$('.deliver').on("click",store.calculateDelivery);
	$('.payment').on("click",store.pay);
	$('.cartmore').on("click",store.putOnCart); 
	
	$('.place').on("click",$.fn.showPlaceView);
	$('.new').on("click",$(this).newSelection);
	$('#Direita').on("click",$.fn.showMessage);
	$('.social').on("click",$.fn.gotoSocial);
	$('.eraseable').on("click",$(this).edit);
	$('.select').on("change",$.fn.changeSelection);
	$('.selection').on("click",$(this).createSelection);
	$('.back').on("click",$.fn.showMenus);
	$('#causeupload').on("click",$(this).tosubmit);
	$('#password').on("click",$.fn.submitPasswordChange);
	$('.overlay').on("click",$(this).select);
	$('.loadable').on("click",$.fn.loadMoreMosaic);
	$('.profile').on("click",$.fn.loadProfileObject);
	$('.filter').on("click",explore.selectFilter);
	$('#explore').on("submit",explore.submitSearch);
	$('.overlay').on("click",$(this).clickContent);
	$('.back').on("click",function(event){ $.fn.showMenus(); });
	$('.favorites').on("click",$(this).showMosaic);
	
	$('.cart').on("click",store.showProductCart);
	$('.submit').on('click',function(event){ $('form').tosubmit(event); });
	$('.unfan').on('click',$.fn.unFan);
	$('.profilefan').on('click',$.fn.profileFan);
	$('.creditinfo').on('click',$.fn.creditInfo);
	$('.navigation').on('click',$.fn.navigationInfo);
	$('.finish').on('click',$.fn.finishTutorial);
	
	$('.logout').on('click',$.fn.logout);
	$('.cancel,.close').on("click",$.fn.closeDialog);
	$('.block').on("click",function(){ $.e.value = false; });
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
	if($('.block-transparent').length) $.e.marginFactor = 0;
	else $.e.marginFactor = 10;
}
