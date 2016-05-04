$('#check_bag').click(function() {
    var payload = JSON.stringify({ first_name: $( "#formFirstNameInput" ).val(), last_name: $( "#formLastNameInput" ).val(), flight_number: $( "#formFlightNumberInput" ).val()});
    $.ajax(
    {
        url : "/api/create",
        type: "POST",
        contentType: "application/json",
        data : payload,
        dataType: 'json',
        success:function(data, textStatus, jqXHR)
        {
            $( "#response" ).html('<div class="alert alert-success" role="alert">Your bag tracking number is: <strong>' + data['bag_id'] + '</strong></div>');
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            $( "#response" ).html('<div class="alert alert-danger" role="alert">' + JSON.parse(jqXHR['responseText'])['message'] + '</div>');
        }
    });
});

$('#get_bag_status').click(function() {
    var bag_id = $( "#formBagTrackingInput" ).val();
    $.ajax(
    {
        url : "/api/status/" + bag_id,
        type: "GET",
        success:function(data, textStatus, jqXHR)
        {
            if (data['bag_status_details']) {
                var bag_details = " <br/>Bag Details: " + data['bag_status_details'];
            } else {
                var bag_details = "";
            }
            $( "#response" ).html('<div class="alert alert-success" role="alert">Bag Status: ' + data['bag_status'] + ' at ' + data['bag_status_time'] + bag_details + '</div>');
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            $( "#response" ).html('<div class="alert alert-danger" role="alert">' + JSON.parse(jqXHR['responseText'])['message'] + '</div>');
        }
    });
});

$('#update_bag_status').click(function() {
     var payload = JSON.stringify({ bag_id: $( "#formBagTrackingInput" ).val(), event_name: $( "#StatusSelect" ).val(), event_details: $( "#formBagStatusDetails" ).val() });
     $.ajax(
     {
         url : "/api/update",
         type: "POST",
         contentType: "application/json",
         data : payload,
         dataType: 'json',
         success:function(data, textStatus, jqXHR)
         {
            $( "#response" ).html('<div class="alert alert-success role="alert">' + JSON.parse(jqXHR['responseText'])['message'] + '</div>');
         },
         error: function(jqXHR, textStatus, errorThrown)
         {
            $( "#response" ).html('<div class="alert alert-danger" role="alert">' + JSON.parse(jqXHR['responseText'])['message'] + '</div>');
         }
     });
 });
