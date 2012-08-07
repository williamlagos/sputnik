var CurrentTime = new Date()
var CurrentYear = CurrentTime.getFullYear()-13
var canvas = new fabric.Canvas('efforia');

$.e = {
	w:window.innerWidth,
	h:window.innerHeight,
	marginMax:0,
	helix:null,
	widthNow:$('html').width(),
	heightNow:$('html').height(),
	radians:180/Math.PI, 
	cX:canvas.width/2,
	cY:canvas.height/2,
	last:0,
	velocity:0.001,
	acceleration:0.1,
	holding:false,
	clicked:false,
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