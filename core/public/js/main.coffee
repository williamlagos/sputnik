$(document).ready ->
  $('.navbar-form').on 'submit', (event) ->
    event.preventDefault()
    $.get 'enter', $('.navbar-form').serialize(), (data) ->
      window.location = '/'
  $('#Grade').getInitialFeed()
  $('.block').mosaic()
      