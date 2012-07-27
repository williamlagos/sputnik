$.fn.createEvents = function(){
	$.ajaxSetup({cache:false});
	$('#radio').buttonset();
	$('#id_username,#id_email,#id_last_name,#id_first_name').addClass('eraseable');
	$('#payment').children().find('input[type=image]').attr('width','240');
	$('#payment').children().find('input[type=image]').attr('src','images/paypal.png');
	$('#payment').children().find('input[type=image]').click($.fn.getRealPrice);
	$('#overlay').hide();	
	$('#datepicker').datepicker($.e.birthdayOpt);
	$('#start_time,#end_time').datepicker($.e.eventOption);
	$('#datepicker').datepicker('option',$.datepicker.regional['pt-BR']);
	
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
}
