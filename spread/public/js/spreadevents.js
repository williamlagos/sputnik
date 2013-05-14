$.fn.unloadEvents = function(){
	$('.spreaded').off('click');
	$('.productspread').off('click');
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
	$('.purchase').off('click');
	$('.product').off('click');
	$('.buyable').off('click');
	$('.products').off('click');
	$('.calculate').off('click');
	$('.moreproducts').off('click');
	$('.cancelpurchase').off('click');
	$('.deliver').off('click');
	$('.payment').off('click');
	$('.cartmore').off('click'); 
	$('.cart').off('click');
}

$.fn.listenEvents = function(){
	$('.spreaded').on('click',spread.showSpreaded);
	$('.productspread').on('click',store.submitProduct);
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
	$('.purchase').on('click',store.openDeliverable);
	$('.product').on('click',store.openProduct);
	$('.buyable').on('click',store.buyMoreCredits);
	$('.products').on('click',store.showProducts);
	$('.calculate').on('click',store.calculatePrice);
	$('.moreproducts').on('click',store.showMoreProducts);
	$('.cancelpurchase').on('click',store.cancelPurchase);
	$('.deliver').on('click',store.calculateDelivery);
	$('.payment').on('click',store.pay);
	$('.cartmore').on('click',store.putOnCart); 
	$('.cart').on('click',store.showProductCart);
}

$.fn.mainLoop = function(){
    $.fn.unloadEvents();
    $.fn.listenEvents();
}

$(document).ready($.fn.mainLoop);
