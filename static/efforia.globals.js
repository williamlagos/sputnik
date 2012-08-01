var CurrentTime = new Date()
var CurrentYear = CurrentTime.getFullYear()-13

$.e = {
	w:window.innerWidth,
	h:window.innerHeight,
	currentTime:CurrentTime,
	selection:false,
	price:1.19,
	option:0,
	token:'',
	objects:[],
	openedMenu:false,
	value:true, 
	marginFactor:10,
	marginTop:0,
	initial:false,
	currentYear:CurrentYear,
	birthdayOpt:{
		defaultDate:'-13y',
		dateFormat:'d MM, yy',
		changeMonth:true,
		changeYear:true,
		yearRange:"1915:"+CurrentYear,
		showOn: "button",
		buttonImage: "images/calendar.png",
		buttonImageOnly: true,
		onClose: function(){ this.focus(); }
	},
	eventOption:{
		changeMonth:true,
		changeYear:true,
		showOn: "button",
		buttonImage: "images/calendar.png",
		buttonImageOnly: true,
		onClose: function(){ this.focus(); }
	},
	uploadOpt:{
		url:'expose',
		type:'POST',
		beforeSend:$.fn.verifyValues,
		xhr:$.fn.uploadProgress,
		success:$.fn.finishUpload
	},
	control:" ui-button ui-widget ui-state-default ui-corner-all\" style=\"padding: .4em 1em;\"><span class=\"ui-icon "
}