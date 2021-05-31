document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

//¨****************************************************************
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  
}
//¨****************************************************************

function load_mailbox(mailbox) {

  
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  inbox();


}

//¨****************************************************************

document.addEventListener('DOMContentLoaded', function(){

  document.querySelector('#compose-form').onsubmit = function(){
    const recipient = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: `${recipient}`,
          subject: `${subject}`,
          body: `${body}`
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    }).catch(error => {
      alert("Looks like the recipient(s) doesn't exist, verify that field please!");
    });
    return false;
    
  }

});

//¨****************************************************************

function populate(email){
  var list = document.createElement('ul');
  var listitem = document.createElement('li');
  var ref = document.createElement('a');
  ref.href = "/emails/"+emails.id; // this should redirect to the selected email.
  var itemrecipient = document.createTextNode(email.recipients+" | ");
  var itemsubject = document.createTextNode(email.subject+" | ");  
  var itemtimestamp = document.createTextNode(email.timestamp+" | ");
  listitem.appendChild(itemrecipient);
  listitem.appendChild(itemsubject);
  listitem.appendChild(itemtimestamp);
  list.appendChild(listitem);
   document.getElementById('emails-view').append(list);
}

function inbox(){
  fetch('/emails/inbox')
.then(response => response.json())
.then(emails => {  
   for (let index = 0; index < emails.length; index++) {
     var email = emails[index];
    populate(email);    
   }
}); 

}