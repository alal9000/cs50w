document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'))
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'))
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'))
    document.querySelector('#compose').addEventListener('click', compose_email)
  
    // By default, load the inbox
    load_mailbox('inbox')
    
  });
  
  function compose_email() {
    
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none'
    document.querySelector('#compose-view').style.display = 'block'
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = ''
    document.querySelector('#compose-subject').value = ''
    document.querySelector('#compose-body').value = ''
  
    let to = document.querySelector('#compose-recipients').value
    let subject = document.querySelector('#compose-subject').value
    let body = document.querySelector('#compose-body').value
  
    document.querySelector('#compose-form').onsubmit = () => {
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
      console.log(result)
      load_mailbox('sent');
    });
    return false;
  }}
  
  function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block'
    document.querySelector('#compose-view').style.display = 'none'
    document.querySelector('#display-view').style.display = 'none'
  
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`
  
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      emails.forEach(email => email_row(email))
    })
  }
  
  function email_row(email) {
    const maildiv = document.createElement("div");
    const sender = document.createElement('h4');
    const subject = document.createElement('p');
    const timestamp = document.createElement('p');
    maildiv.id = 'mail';
  
    sender.innerHTML = email.sender;
    subject.innerHTML = email.subject;
    timestamp.innerHTML = email.timestamp;
  
    if (email.read == true) {
    maildiv.style.backgroundColor = 'gray';
    }
    else {
      maildiv.style.backgroundColor = 'white';
    }
    
    document.querySelector('#emails-view').appendChild(maildiv);
    maildiv.appendChild(sender);
    maildiv.appendChild(subject);
    maildiv.appendChild(timestamp);
  
    maildiv.addEventListener('click', () => view_email(email));
    
  }
  
  function view_email(email) {
    document.querySelector('#display-view').textContent = '';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#display-view').style.display = 'block';
  
    fetch('/emails/'+`${email.id}`)
    .then(response => response.json())
    .then(email => {
        console.log(email)
        const maildiv = document.createElement("div");
        const sender = document.createElement("h4");
        const recipients = document.createElement("p");
        const subject = document.createElement("p");
        const timestamp = document.createElement("p");
        const body = document.createElement("p");
        const button = document.createElement("button");
  
        sender.innerHTML = email.sender;
        recipients.innerHTML = email.recipients;
        subject.innerHTML = email.subject;
        timestamp.innerHTML = email.timestamp;
        body.innerHTML = email.body;
  
        document.querySelector('#display-view').appendChild(maildiv);
        maildiv.appendChild(sender);
        maildiv.appendChild(subject);
        maildiv.appendChild(timestamp);
        maildiv.appendChild(body);
        maildiv.appendChild(recipients);
        maildiv.appendChild(button);
  
        button.textContent = email.archived ? "Unarchive" : "Archive";
        button.addEventListener('click', () => email.archived ? unarchive_email(email) : archive_email(email));
    });
    fetch('/emails/'+`${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  }
  
  function archive_email(email) {
    fetch('/emails/'+`${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    load_mailbox('inbox')
  }
  
  function unarchive_email(email) {
    fetch('/emails/'+`${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    load_mailbox('inbox')
  }