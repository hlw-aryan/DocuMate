css = '''
<style>
  .chat-container {
    display: flex;
    flex-direction: column;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    color: #d4d4d4;
  }

  .chat-message {
    display: flex;
    margin-bottom: 1rem;
  }

  .chat-message.user {
    justify-content: flex-end;
  }

  .chat-message.bot {
    justify-content: flex-start;
  }

  .chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
  }

  .chat-message .avatar img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    margin: 0; /* Reset margin */
    padding: 0; /* Reset padding */
  }

  .chat-message .message {
    max-width: 70%;
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    background-color: #2b2b2b;
    color: #fff;
  }

  .chat-message.bot .message {
    background-color: #2b2b2b;
    color: #fff;
  }
</style>
'''
bot_template = '''
<div class="chat-container">
  <div class="chat-message user">
  <div class="message">{{MSG}}</div>
    <div class="avatar">
      <img src='https://i.imgur.com/ljfqd6O.png' alt="Bot">
    </div>
  </div>
'''

user_template ='''
  <div class="chat-message bot">
    <div class="avatar">
      <img src="https://i.imgur.com/IgX5kZz.png" alt="User">
    </div>
    <div class="message">{{MSG}}</div>
  </div>
</div>
'''