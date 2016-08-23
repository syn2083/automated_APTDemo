/**
 * Created by venom on 8/19/2016.
 */
// Submit post on submit
$('#start').click(function() {
$.get('/start_demo/', function(data){
    $('#demo_status').html(data['demo_status']);
    $('#server_message').html(data['server_message']);
});
});
$('#stop').click(function() {
$.get('/stop_demo/', function(data){
    $('#demo_status').html(data);
});
});
