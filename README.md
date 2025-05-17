# **Contactgram** - Simple yet Powerful Telegram Contact Bot

<p align="center">
  <a href="https://github.com/theseekerofficial">
    <kbd>
      <img width="200" src="https://i.ibb.co/35LvkK8F/bot-pic.jpg" alt="MLWA Connect Icon" style="border: 4px solid #4CAF50; border-radius: 20px; padding: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    </kbd>
  </a>
</p>

A powerful, feature-packed Telegram bot built using Python with asynchronous programming style. Contactgram helps you manage contacts and automate tasks with ease!

---

## 🛠 **Features**:
- Easy-to-use yet highly customizable Telegram bot.
- Admin management with the ability to set multiple admins.
- Fully asynchronous and designed for scalability.
- Autoconfiguration of bot commands, description, and settings during deployment.
- Support for detailed message forwarding to admins for better tracking.
- Customizable welcome message with an image.
- **Mark as Seen** button: Notifies users that their message has been seen.
- Instant message transfer system: Sends messages to admins or users with minimal delay.
- **Reply Mode**: Toggle between sending normal messages and replying directly to user messages.
- **Forward Mode**: Allows admins to forward messages directly to users when they forward a message to the bot.


## 📝 **Commands**:

Below is the list of available commands for the Contactgram bot:

- `/start`: Start the bot and initialize the interaction.
- `/help`: Get detailed help and instructions on how to use the bot.
- `/togglereply`: Toggle between sending normal messages and sending replies to the user's messages. [Only for admin team]
- `/forwardmode`: Instead of sending messages directly to users, forward messages when an admin forwards a message to the bot. Usage: `/forwardmode <user tg id>`. Example: `/forwardmode 123456789`. Also admins can active this mode using reply to a user message. [Only for admin team]

---

## ⚙️ **Settings Configuration (`settings.env`)**:

This is where all the core configuration for the bot is stored. Below is the list of available settings:

| **Setting**                 | **Description**                                                                                                                                     |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `BOT_TOKEN`                 | Bot token from BotFather                                                                                                                            |
| `ADMIN_TEAM`                | List of Telegram user IDs for admins, separated by commas                                                                                           |
| `MONGO_URI`                 | URI for MongoDB connection                                                                                                                          |
| `TIMEZONE`                  | Admin's timezone (use `Asia/Colombo` format)                                                                                                        |
| `AUTO_CONFIG`               | Set to 'True' for auto configuration during bot deployment                                                                                          |
| `BOT_NAME`                  | Name of the bot used for auto configuration                                                                                                         |
| `BOT_DESCRIPTION`           | Description for the bot for auto configuration                                                                                                      |
| `BOT_SHORT_DESCRIPTION`     | Short description for the bot during auto configuration                                                                                             |
| `SET_BOT_CMD`               | Set to `True` if you want to auto set bot commands during configuration                                                                             |
| `ENABLE_DETAILED_FORWARD`   | Set to `True` to enable forwarding messages to admins instead of simple forwarding.                                                                 |
| `WELCOME_MESSAGE`           | Message that users will see when they start the bot with `/start`                                                                                   |
| `WELCOME_IMAGE_URL`         | Optional image URL that will be sent along with the welcome message                                                                                 |
| `START_WEB_APP`             | Start the web interface. If this not set to `True` you cannot use /openwebapp cmd                                                                   |
| `QUART_SECRET_KEY`          | This is like your web app password. Any String allowed. More randomness = More Secure. Do not use `$` symbol                                        |
| `WEB_APP_PORT`              | Port number of web interface. (Recommended to not to change)                                                                                        |
| `SAVE_MESSAGES`             | Save messages to mongodb to see in web interface. Set to `True`                                                                                     |
| `INTERFACE_ACCESS_PASSWORD` | Admin password to access web app. Any String. More randomness = More Secure. Do not use `$` symbol                                                  |
| `ENABLE_CMD_LOGS`           | If set to `True` all bot cmd usage (Both admin and user) will be saved to mongodb  can be see in web interface.                                     |
| `ENABLE_BUTTON_CLICK_LOGS`  | If set to `True` all user and admin inline button clicks will be saved to mongodb and can be see in web interface.                                  |
| `WEB_APP_URL`               | Your domain or server ip. If using a domain see [Nginx Configuration](#Nginx). Example Values: (`https://contactgram.com` or `http://52.168.45.24`) |

---

## Nginx Configuration

To use the web interface with a domain, you need to set up Nginx with the following configuration:

### ✅ Step 1: Install Nginx

### On Ubuntu/Debian:
```bash
sudo apt update 
sudo apt install nginx -y
```

### ▶️ Step 2: Start and Enable Nginx
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

To check if Nginx is running:
```bash
sudo systemctl status nginx
```

### 🧾 Step 3: Add nginx template

- Copy the `contactgram.ngnix` file in assets folder in this repo to `/etc/nginx/sites-available/` directory on your server.
- Replace the `your-domain.com` with your domain (No https://, http://, or www. prefix. Just the domain name like contactgram.com)
- Run the following command to create a symbolic link:
```bash
sudo ln -s /etc/nginx/sites-available/contactgram.ngnix /etc/nginx/sites-enabled/
```

### Step 4: Test and Restart Nginx
- Test Nginx configuration using this cmd:
```bash
sudo nginx -t
```
- If you see output like 
```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
- You are good to go. Restart Nginx using this cmd:
```bash
sudo systemctl restart nginx
```

- Good Job! You can now access the web interface at your-domain.com
---


## 🚀 **Deployment Instructions**:

1. **Give a Star**:  
   Don't forget to show your support by giving a ⭐ to the repository:  
   [Star Contactgram on GitHub](https://github.com/theseekerofficial/Contactgram)

2. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repository/Contactgram.git
    cd Contactgram
    ```

3. **Rename the settings file:**
    - Rename `sample_settings.env` to `settings.env`:
    ```bash
    mv sample_settings.env settings.env
    ```

4. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
    ```

5. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the bot:**
    ```bash
    python3 bot.py
    ```

---

## 🚦 **Version:**

- Contactgram Version: 1.5.0

---

## 🌟 **Demo Bot**:

Check out the **Contactgram** bot in action here:

[Contactgram Demo Bot](https://t.me/The_Seeker_Contact_Robot)

---

## 📞 **Contact The Seeker**:

If you need any assistance or want to contribute to the project, feel free to reach out:

- [Telegram - Contactgram](https://t.me/The_Seeker_Contact_Robot)
- [Telegram - MrUnknown114](https://t.me/MrUnknown114)
- Email: [caveoftheseekers@gmail.com](mailto:caveoftheseekers@gmail.com)
- [Channel - Master Torrenz Updates](https://t.me/Maste_Torrenz_Updates)
---

## 💡 **Contributors**:

Contributors are always welcome! Feel free to fork the project, improve upon it, and send pull requests. Together, we can make **Contactgram** even better.

---

## 🎨 **Bot Styling**:

Make your bot even more personal by customizing the **Welcome Message** and **Welcome Image**. Here’s how it looks when you customize the settings:

- **Welcome Message**:  
  "Welcome to Contactgram! We're glad to have you. How can I assist you today?"

- **Welcome Image**:  
  Upload your custom welcome image via any online image service or use the URL of the image you prefer.

---

## 🎉 **Stay Connected & Updated**:

Make sure to follow the updates and contribute to the **Contactgram** project. Join the community, provide feedback, and be a part of the future of **Contactgram**!


