$(document).ready ->
  $('.btn').on 'click', (event) ->
    event.preventDefault()
    $.get 'enter', $('.navbar-form').serialize(), (data) ->
      console.log JSON.stringify(data)
      console.log data['username']
      