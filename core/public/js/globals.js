var CurrentTime = new Date()
var CurrentYear = CurrentTime.getFullYear()-13
var simpleEditor = {
	lists:false,
	image:false,
	color:true,
	link:false,
	locale:'pt-BR' }
var advancedEditor = {
	lists:true,
	image:true,
	color:true,
	link:true,
	html:true,
	locale:'pt-BR' }
var uploader = {
	url: 'images',
	type: 'POST',
	beforeSend: function(){ $('.send').button('loading'); },
	success: function (data) {
		$('#Espaco').modal('hide');
		$('#Grade').html(data)
	}}
var datepick = { 
	format:'dd/mm/yyyy',
	language:'pt-BR' }

$.e = {
	spin:false,
	editorOpt:advancedEditor,
	uploadOpt:uploader,
	datepickerOpt:datepick,
	w:window.innerWidth,
	h:window.innerHeight,
	lastObject:'',
	lastId:'',
	marginMax:0,
	angle:0,
	widthNow:$('html').width(),
	heightNow:$('html').height(),
	last:0,
	velocity:0,
	acceleration:50,
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
	position:0,
	lastVideo:'',
	videos:[],
	playerOpt:{
		width: 790, // the width of the player
		height: 430, // the height of the player
		autoPlay: true,
		showinfo: false,
		autoHide: true,
		iframed: true,
		showControls: 0,
		preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
		onPlayerEnded: play.playAgain
	},
	birthdayOpt:{
		defaultDate:'-13y',
		//dateFormat:'d MM, yy',
		changeMonth:true,
		changeYear:true,
		yearRange:"1915:"+CurrentYear,
		showOn: "button",
		buttonImage: "images/calendar.png",
		buttonImageOnly: true,
		onClose: function(){ this.focus(); }
	},
	deadlineOpt:{
		changeMonth:true,
		changeYear:true,
		showOn: "button",
		minDate: "0d",
		maxDate: "+1Y",
		buttonImage: "images/calendar.png",
		buttonImageOnly: true,
		onClose: function(){ this.focus(); }
	},
	uploadOpt:{
		url:'expose',
		type:'POST',
		beforeSend:function(){ $('#Espaco').Progress(); },
		xhr:play.uploadProgress,
		success:play.finishUpload
	},
	control:'ui-button ui-widget ui-state-default ui-corner-all'
}