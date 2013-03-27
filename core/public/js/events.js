$.fn.clearEvents = function(){
	$('#Canvas')
	.off('mousedown')
	.off('mouseup')
	.off('mousemove');
	
	$('.app').off('click');
	$('.pages').off('click');
	$('.login').off('click');
	$('.logout').off('click');
	$('.register').off('click');
	$('.option').off('click');
	$('.upload').off('click');
	$('.procfg').off('click');
	$('.placecfg').off('click');
	$('.controlcfg').off('click');
	$('.change').off('click');
	$('.integration,.social').off('click');
	$('.deletable').off('click');
	$('.submit').off('click');
	$('.explore').off('submit');
	$('.brand').off('click');
	$('.brand').off('hover');
	$('.participate').off('click');
	$('.next').off('click');
	
	$('.following').off('click');
	$('.profile').off('click');
	$('.unfollow').off('click');
	$('.unfollow').off('hover');
	$('.follow').off('click');
	
	$('.spreaded').off('click');
	$('.objectspread').off('click');
	$('.uploadspread').off('click');
	$('.videospread').off('click');
	$('.imagespread').off('click');
	$('.eventspread').off('click');
	$('.postspread').off('click');
	$('.pagespread').off('click');
	$('.spreadable').off('click');
	$('.playable').off('click');
	$('.event').off('click');
	$('.image').off('click');
	$('.page').off('click');
	$('.pagesave').off('click');
	$('.spread').off('click');
	
	$('.objectpledge').off('click');
	$('.pledge').off('click');
	$('.promoted').off('click');
	$('.movementcreate').off('click');
	$('.keyword').off('click');
	$('.promote').off('click');
	$('.objectpromote').off('click');
	$('.project').off('click');
	$('.movement').off('click');
	$('.projectcreate').off('click');
	$('.linkcreate').off('click');
	$('.backers').off('click');
	
	$('.purchase').off('click');
	$('.product').off('click');
	$('.buyable').off('click');
	$('.submitproduct').off('click');
	$('.products').off('click');
	$('.calculate').off('click');
	$('.moreproducts').off('click');
	$('.cancelpurchase').off('click');
	$('.deliver').off('click');
	$('.payment').off('click');
	$('.cartmore').off('click'); 
	$('.cart').off('click');
}

$.fn.eventLoop = function(){
	$.fn.clearEvents();
	
	$('#Canvas')
	.on('mousedown',spin.holdHelix)
	.on('mouseup',spin.releaseHelix)
	.on('mousemove',spin.moveHelix);
	if($('.block-transparent').length) $.e.marginFactor = 0;
	else $.e.marginFactor = 10;
	
	$('a').on('click',function(){ this.blur(); });
	$('.app').on('click',$(this).showContext);
	$('.pages').on('click',$(this).showPage);
	$('.login').on('click',$.fn.authenticate);
	$('.logout').on('click',$.fn.logout);
	$('.register').on('click',$.fn.showParticipate);
	$('.option').on('click',$(this).changeOption);
	$('.upload').on('click',$.fn.input);
	$('.procfg').on('click',$.fn.submitChanges);
	$('.placecfg').on('click',$.fn.submitPlace);
	$('.controlcfg').on('click',$.fn.submitControl);
	$('.change').on('click',$.fn.doNothing);
	$('.integration,.social').on('click',$(this).redirect);
	$('.deletable').on('click',$.fn.deleteObject);
	$('.submit').on('click',function(event){ $('form').tosubmit(event); });
	$('.explore').on('submit',$(this).submitSearch);
	$('.brand').on('click',$.fn.reloadMosaic);
	$('.brand').on('hover',$.fn.brandHover);
	$('.participate').on('click',$.fn.participate)
	$('.next').on('click',$.fn.nextTutorial);
	
	$('.following').on('click',$.fn.showFollowing);
	$('.profile').on('click',$.fn.showProfile);
	$('.unfollow').on('click',$.fn.unfollow);
	$('.unfollow').on('hover',$.fn.unfollowHover);
	$('.follow').on('click',$.fn.follow);

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
	$('.backers').on('click',create.showBackers);

	$('.purchase').on('click',store.openDeliverable);
	$('.product').on('click',store.openProduct);
	$('.buyable').on('click',store.buyMoreCredits);
	$('.submitproduct').on('click',store.submitProduct);
	$('.products').on('click',store.showProducts);
	$('.calculate').on('click',store.calculatePrice);
	$('.moreproducts').on('click',store.showMoreProducts);
	$('.cancelpurchase').on('click',store.cancelPurchase);
	$('.deliver').on('click',store.calculateDelivery);
	$('.payment').on('click',store.pay);
	$('.cartmore').on('click',store.putOnCart); 
	$('.cart').on('click',store.showProductCart);
}
