let currUser = JSON.parse(document.getElementById('currUser').textContent);
let withuserID = JSON.parse(document.getElementById('withuserID').textContent);

let userBlock = document.getElementById(withuserID);
userBlock.classList.add('active');

const curruserID = Number(JSON.parse(document.getElementById('curruserID').textContent));

document.querySelector('#sendButton').onclick = function(e) {
    const messageInput = document.querySelector('#message_input');
    const message = messageInput.value;
    receiverSocket.send(JSON.stringify(
        {
            message: message,
            senderID: curruserID,
        }
    ));

    const newDiv = document.createElement('div');
    newDiv.className = ['alert', 'alert-primary', 'toMessage'].join(" ");
    newDiv.innerText = message;
    document.querySelector('.card-body').appendChild(newDiv);
    newDiv.scrollIntoView(true);

    console.log('Sent to ' + receiverSocket.url);
    messageInput.value = '';
};

document.body.onkeydown = (ev) => {
    if (ev.key === 'Enter') {
        document.querySelector('#sendButton').click();
    }
}

const receiverSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    withuserID +
    '/'
);

const senderSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    curruserID +
    '/'
)

senderSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.senderID == withuserID) {
        const newDiv = document.createElement('div');
        newDiv.className = ['alert', 'alert-secondary', 'fromMessage'].join(" ");
        newDiv.innerText = data.message;
        document.querySelector('.card-body').appendChild(newDiv);
        newDiv.scrollIntoView(true);
    } else {
        const senderMessageCount = document.getElementById('unreadCount'+ data.senderID);
        senderMessageCount.innerText = `${(parseInt(senderMessageCount.innerText) || 0) + 1}`
    }

};

document.body.onload = () => {
    setTimeout(() => {
        let JSONString = JSON.parse(JSON.parse(document.getElementById('this-chat').textContent));
        
        // document.querySelector('#chat-text').value = JSON.parse(document.getElementById('this-chat').textContent);
        JSONString.forEach((ele) => {
            const { senderID, receiver, content } = ele;
            const newDiv = document.createElement('div');
            // console.log(currUser, withUser);
            if (senderID == curruserID) {
                newDiv.className = ['alert', 'alert-primary', 'toMessage'].join(" ");
            } else if (senderID == withuserID) {
                newDiv.className = ['alert', 'alert-secondary', 'fromMessage'].join(" ");
            }
            newDiv.innerText = content;
            document.querySelector('.card-body').appendChild(newDiv);
            newDiv.scrollIntoView(true);
        })

        const messageCount = document.getElementById('unreadCount'+ withuserID);
        messageCount.innerText = '';
        
    }, 1000)
}
