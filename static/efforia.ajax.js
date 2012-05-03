$(document).ready(function(){
var currentTime = new Date();
$('.dialogo').click(function(event){
	event.preventDefault();
	$.ajax({
		url:this.href,
		success: function(data){
			$('#caixa').dialog('destroy');
			$('#caixa').empty();
			$('#caixa').html(data);
			$('#caixa').dialog({title:'Entrar no Efforia',height:'auto',width:'auto',modal:true});
			alert('Opened!');
			currentYear = currentTime.getFullYear()-13
			$('#datepicker').datepicker({
				defaultDate:'-13y',
				dateFormat:'mm/dd/yy',
				changeMonth:true,
				changeYear:true,
				yearRange:"1915:"+currentYear,
				showOn: "button",
				buttonImage: "images/calendar.png",
				buttonImageOnly: true,
				onClose: function(){ this.focus(); }
			});
		}
	});
});
/*$('.popup').click(function(event){
	event.preventDefault();
	$(".popup").popupwindow();
});*/
});
