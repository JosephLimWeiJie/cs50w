document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener(
        'click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener(
        'click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener(
        'click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener(
        'click', compose_email);
    document.querySelector('#compose-form').onsubmit = send_email;

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#view-emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
 }

function load_mailbox(mailbox) {

    toggle_email_view(mailbox);

    // Show the mailbox name
    document.querySelector("#emails-view").innerHTML = `
        <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Fetch the relevant emails
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            for (index = 0; index < emails.length; index++) {
                const email = emails[index];
                const email_border_div = document.createElement('div');
                email_border_div.style.border = '1px solid grey';
                email_border_div.style.borderRadius = '8px';
                email_border_div.style.marginBottom = '12px';

                if (email.read == true) {
                    email_border_div.style.background = 'lightgrey';
                } else {
                    email_border_div.style.background = 'white';
                }

                // Construct the contents for an email
                email_border_div.innerHTML = `
                    <div class='email-content'>
                        <div class='email-sender-div'>
                            <p style="font-size: 20px; padding-left: 5px;">
                                <strong>
                                    ${get_email_username(email.sender)}
                                </strong>
                            </p>
                        </div>
                        <div class='email-subject-div'>
                            <p style='padding-left: 5px;'>
                                Subject: ${email.subject}
                            </p>
                        </div>
                        <div class='email-timestamp-div'>
                            <p style="font-size: 12px; color: grey;
                                padding-left: 5px;">
                                ${email.timestamp}
                            </p>
                        </div>
                    </div>`;

                email_border_div.addEventListener(
                    'click', () => view_email(email.id, mailbox));

                document.querySelector('#emails-view').appendChild(
                    email_border_div);
            }
        });

}

function send_email() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
        method: 'POST',
            body: JSON.stringify({
              recipients: recipients,
              subject: subject,
              body: body
          })
        })
        .then(response => response.json())
        .then(result => {
            load_mailbox('sent');
        })

    return false;
}

function view_email(email_id, mailbox) {

    // Show the individual email view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#view-emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Clear out previous email entries to prevent them from displaying
    document.querySelector('#view-emails-view').innerHTML = '';

    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {

            // Constuct the container of the viewing email
            const email_border_div = document.createElement('div');
            email_border_div.innerHTML = `
                <div class='email-content'>
                    <div class='email-sender-div'>
                        <p>
                            <strong>From: </strong>${email.sender}
                        </p>
                    </div>
                    <div class='email-recipents-div'>
                        <p>
                            <strong>To: </strong>${email.recipients}
                        </p>
                    </div>
                    <div class='email-subject-div'>
                        <p>
                            <strong> Subject: </strong>${email.subject}
                        </p>
                    </div>
                    <div class='email-timestamp-div'>
                        <p style="font-size: 12px; color: grey;">
                            ${email.timestamp}
                        </p>
                    </div>
                    <div class='email-body-div'>
                        <hr>
                        <p>${email.body}</p>
                    </div>
                </div>
                <hr>`;

            document.querySelector('#view-emails-view').append(
                email_border_div);

                // Create the 'Reply' button
                reply_button_border_div = document.createElement('div');
                reply_button_border_div.innerHTML =
                    `<button class="btn btn-sm btn-outline-primary"
                    id='reply-btn' style='margin-bottom: 8px;'>Reply</button>`;
                reply_button_border_div.addEventListener(
                    'click', () => reply_email(email_id));
                document.querySelector('#view-emails-view').append(
                    reply_button_border_div);

                // Create 'Archive' button if email is under 'inbox'
                if (mailbox == 'inbox') {
                    button_border_div = document.createElement('div');
                    button_border_div.innerHTML =
                        `<button class="btn btn-sm btn-outline-primary"
                        id='archive-btn'>Archive</button>`;
                    button_border_div.addEventListener(
                        'click', () => archive_email(email_id));
                    document.querySelector('#view-emails-view').append(
                        button_border_div);

                // Create 'Unarchive' button if email is under 'archive'
                } else if (mailbox == 'archive') {
                    button_border_div = document.createElement('div');
                    button_border_div.innerHTML =
                        `<button class="btn btn-sm btn-outline-primary"
                        id='archive-btn'>Unarchive</button>`;
                    button_border_div.addEventListener(
                        'click', () => unarchive_email(email_id));
                    document.querySelector('#view-emails-view').append(
                        button_border_div);
                }
            });

    // Update email.read in database
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    });
}

function archive_email(email_id) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    });

    load_mailbox('inbox');
}

function unarchive_email(email_id) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
    });

    load_mailbox('inbox');
}

function reply_email(email_id, mailbox) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#view-emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            const recipent = email.sender;
            var subject = email.subject;
            const timestamp = email.timestamp;

            // Check and pre-fill subject with 'Re:'
            if (subject.includes("RE: ")) {
                subject = subject;
            } else {
                subject = "RE: " + subject;
            }

            // Pre-fill body with timestamp and sender's info
            if (mailbox == 'sent') {
                var body = email.body;
            } else {
                var body = `On ${timestamp} ${recipent} wrote:
                    \n ${email.body}`;
            }

            document.querySelector('#compose-recipients').value = recipent;
            document.querySelector('#compose-subject').value = subject;
            document.querySelector('#compose-body').value = body;

        }
    );
}

/* This functions toggles the display of the respective views when the user
   clicks on the respective emails button. */
function toggle_email_view(mailbox) {

    if (mailbox == "inbox") {
        document.querySelector('#emails-view').style.display = 'block';
        document.querySelector('#view-emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
    } else if (mailbox == "sent") {
        document.querySelector('#emails-view').style.display = 'block';
        document.querySelector('#view-emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
    } else {
        document.querySelector('#emails-view').style.display = 'block';
        document.querySelector('#view-emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
    }
}

/* This function formats a given email username and return the user's first
   name. */
function get_email_username(email) {
    var username = email.split("@");
    var first_name = username[0];
    return first_name.charAt(0).toUpperCase() + first_name.slice(1);
}
