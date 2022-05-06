document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    document.querySelector('form').onsubmit = send;
  
    // By default, load the inbox
    load_mailbox('inbox')
    
  });
  
  function compose_email() {
  
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

  }
  
  function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
  
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
    if (mailbox == 'inbox') {
  
      fetch('/emails/inbox')
      .then(response => response.json())
      .then(emails => {
      // Print emails
      console.log(emails);
      emails.forEach(email => add(email));
  
      // ... do something else with emails ...
  
      
  });
    }
    if (mailbox == 'sent') {
      fetch('/emails/sent')
      .then(response => response.json())
      .then(emails => {
        console.log(emails);
        emails.forEach(email => add(email));
      })
    }
    if (mailbox === 'archive') {
      fetch('/emails/archive')
      .then(response => response.json())
      .then(emails => {
        console.log(emails);
        emails.forEach(email => add(email));
      })
      
    }
  }
  
  
  function send() {
    let to = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;
  
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: to,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        
        console.log(result);
        
    });
    load_mailbox('sent')
    return false;
  }
  
  
  function add(email) {
      
    const element = document.createElement('div');
    element.innerHTML = email.sender + email.subject.bold() + email.timestamp + email.id;
    element.id = 'new';
    var email_id = email.id;
    var sender = email.sender;
    var recipient = email.recipient;
    var body = email.body;
    element.addEventListener('click', function() {
        element.id = 'old';
        fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            // Print email
            console.log(email);
            display();
  
      // ... do something else with email ...
      
  
  });
    });
    document.querySelector('#emails-view').append(element);
    element.innerHTML = email.sender + email.subject.bold() + email.timestamp + email.id;
  }
  
  
  function display() {
      // Show compose view and hide other views
      console.log('this function ran');
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
  
      fetch(`/emails/${email_id}`)
      .then(response => response.json())
      .then(email => {
      // Print email
      console.log(email);
      const element2 = document.createElement('div');
      element2.innerHTML = email.sender + email.subject.bold() + email.timestamp + email.id;
  
      // ... do something else with email ...
  });
  
  
  }