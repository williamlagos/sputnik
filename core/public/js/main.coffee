$(document).ready ->
  $('.btn').on 'click', (event) ->
    event.preventDefault()
    $.get 'enter', $('.navbar-form').serialize(), (data) ->
      window.location = '/'
      