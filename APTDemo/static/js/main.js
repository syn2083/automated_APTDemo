/**
 * Created by venom on 8/19/2016.
 */
// Submit post on submit
$('#demo-config-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    update_demo();
});
// AJAX for posting
function update_demo() {
    console.log("update_demo is working!") // sanity check
    console.log($('#demo-text').val())
};
