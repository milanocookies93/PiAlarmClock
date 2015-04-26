var client = require('twilio')('AC5bc10b06dfef6a0d19cfef184406cd74', 'c7fb839a2ebd320b392654eaa01cb22a');

client.sendMessage({

    to:'+16309950526',
    from: '+13313056100',
    body: 'Rainbow Unicorn Ninja wants you to wake up! https://myspideysenseistingling.files.wordpress.com/2011/09/behold_a_rainbow_unicorn_ninja_by_jess4921.jpg'

}, function(err, responseData) { //this function is executed when a response is received from Twilio

   
});
