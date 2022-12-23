let currUser = JSON.parse(document.getElementById('currUser').textContent);
let withUser = JSON.parse(document.getElementById('withUser').textContent);

let userBlock = document.getElementById(withUser);
userBlock.classList.add('active');

const user_username = JSON.parse(document.getElementById('user_username').textContent);

document.querySelector('#sendButton').onclick = function(e) {
    const messageInput = document.querySelector('#message_input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify(
        {
            message,
            username: user_username,
        }
    ));
    messageInput.value = '';
};

document.body.onkeydown = (ev) => {
    if (ev.key === 'Enter') {
        document.querySelector('#sendButton').click()
    }
}

const chatboxName = JSON.parse(document.getElementById('chatbox-name').textContent);
const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    chatboxName +
    '/'
);


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    // document.querySelector('#chat-text').value += (data.message + ' sent by ' + data.username + '\n');
    const newDiv = document.createElement('div');
    if (data.username == currUser) {
        newDiv.className = ['alert', 'alert-primary', 'toMessage'].join(" ");
    } else if (data.username == withUser) {
        newDiv.className = ['alert', 'alert-secondary', 'fromMessage'].join(" ");
    }
    newDiv.innerText = data.message;
    document.querySelector('.card-body').appendChild(newDiv);
    newDiv.scrollIntoView(true);
};

document.body.onload = () => {
    setTimeout(() => {
        let JSONString = JSON.parse(JSON.parse(document.getElementById('this-chat').textContent));
        
        // document.querySelector('#chat-text').value = JSON.parse(document.getElementById('this-chat').textContent);
        JSONString.forEach((ele) => {
            const { sender, receiver, content } = ele;
            const newDiv = document.createElement('div');
            // console.log(currUser, withUser);
            if (sender == currUser) {
                newDiv.className = ['alert', 'alert-primary', 'toMessage'].join(" ");
            } else if (sender == withUser) {
                newDiv.className = ['alert', 'alert-secondary', 'fromMessage'].join(" ");
            }
            newDiv.innerText = content;
            document.querySelector('.card-body').appendChild(newDiv);
            newDiv.scrollIntoView(true);
        })
    }, 1000)
}
