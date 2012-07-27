$.fn.eventLoop = function(){
	if(!$.e.context){ $('*').unbind(); }
	
	$('.causablespread').click(create.openCausableSpread);
	$('#selectupload').click(create.selectVideo);
	$('#causeupload').submit(create.submitCause);
	$('.causable').click(create.openCausable);
	$('.message').click(create.loadListContext);
	$('.movement,.schedule').click(create.loadListMosaic);

	$('.spreadablespread').click(spread.openSpreadableSpread);
	$('.eventspread').click(spread.openEventSpread);
	$('#spreadpost').click(spread.submitSpread);
	$('#eventpost').click(spread.submitEvent);
	$('.spreadable,.event').click(spread.loadTextObject);

	$('#content').click(play.submitPlay);
	$('.playable').click(play.loadPlayObject);
	$('.video').click(play.getVideoInformation);

	$('.purchase').click(store.openDeliverable);
	$('.product').click(store.openProduct);
	$('.buyable').click(store.buyMoreCredits);
	$('.creation').click(store.createNewProduct);
	$('.products').click(store.showProducts);
	$('.calculate').click(store.calculatePrice);
	
	$('.place').click($.fn.registerPlace);
	$('.new').click($.fn.newItem);
	$('#Direita').click($.fn.showMessage);
	$('.social').click($.fn.gotoSocial);
	$('#upload').click($.fn.fileInput);
	$('.register').click($.fn.loadNewDialog);
	$('.eraseable').click($(this).editNewField);
	$('.select').change($.fn.changeSelection);
	$('.selection').click($(this).createSelection);
	$('.return').click($.fn.showMenus);
	$('#causeupload').click($(this).submitTrigger);

	$('#id_username,#id_email,#id_last_name,#id_first_name,#datepicker').keyup($.fn.sendNewField);
	$('#datepicker').keydown($.fn.sendNewField);
	$('#password').click($.fn.submitPasswordChange);
	$('.mosaic-overlay').click($(this).clickContent);
	$('.loadable').click($.fn.loadMoreMosaic);
	$('.profile').click($.fn.loadProfileObject);
	$('.mosaic-block').click(function(){ $.e.value = false; });
	$('.login').click($.fn.showLoginView);
	$('.register').click($.fn.showRegisterView);
	$('.who').click($.fn.slideWhoPage);
	$('.what').click($.fn.slideWhatPage);
	$('.how').click($.fn.slideHowPage);
	$('input[type=file]').fileUpload($.e.uploadOpt);
	$('.filter').click(function(event){
		event.preventDefault();
		if(!$.e.openedMenu){
			$('#Menu').slideDown("slow");
			$.e.openedMenu = true;	
		}else{
			$('#Menu').slideUp("slow");
			$('.lupa').focus();
			$.e.openedMenu = false;
		}
	});
	$('#explore').submit(function(event){
		event.preventDefault(); 
		$.get($.fn.getSearchFilters(this.action,$(this).serialize()),{},function(data){
			$.fn.hideMenus();
			$('#Grade').loadMosaic(data);
		});
	});
	$('.mosaic-overlay').click(function(event){ $.fn.clickContent(event,$(this)); });
	$('.return').click(function(event){ $.fn.showMenus(); });
	$('#play').click(function(event){$.fn.showContext(event,'play',function(data){$.fn.showDataContext('O que você quer tocar hoje?',data);});});
	$('#create').click(function(event){$.fn.showContext(event,'create',function(data){$.fn.showDataContext('O que você pretende criar hoje?',data);});});
	$('#spread').click(function(event){$.fn.showContext(event,'spreads',function(data){$.fn.showDataContext('O que você quer espalhar hoje?',data);});});
	$('.favorites').click(function(event){$.fn.showContext(event,'favorites',function(data){ $('#Grade').loadMosaic(data); $.fn.hideMenus(); });});
	$('.config').click(function(event){$.fn.showContext(event,'config',function(data){$.fn.showDataContext('Teste',data);});});
	$('.cart').click(function(event){
		event.preventDefault();
		$.get('cart',{},function(data){
			$('#Grade').loadMosaic(data);
		});
	});
	$('.cancel').click(function(event){
		event.preventDefault();
		$('#Espaco').dialog('destroy');
		$('#Player').tubeplayer('destroy');
	});
}
