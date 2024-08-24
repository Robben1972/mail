```markdown
 Aiogram Email Bot

This project is a Telegram bot built using the `aiogram` framework. It allows users to start an interaction, enter their email, and send emails through the bot. The bot also supports a search feature to retrieve user information from a PostgreSQL database.

 Features

- User Registration: Users can register by providing their email and password.
- Email Sending: Registered users can send emails to specific addresses directly from the bot.
- User Search: The bot can list users stored in the database and send emails to selected users.
- Form Handling: The bot uses `aiogram.fsm` to handle different stages of user interaction.

 Prerequisites

- Python 3.7+
- PostgreSQL database
- Aiogram
- SQLAlchemy

 Installation

1. Clone the repository:

   bash
   git clone git@github.com:Robben1972/mail.git
   cd repo-name
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database:**

   Create a PostgreSQL database and configure your `engine` connection string in the `db.py` file.

5. **Configure the Bot:**

   - Replace `BOT_TOKEN` in the script with your actual Telegram bot token.
   - Replace email configuration in the `send` function to include your email credentials.

6. **Run the bot:**

   ```bash
   python main.py
   ```

## Usage

1. **Start the bot:**

   Use the `/start` command to begin the interaction.

2. **Register:**

   Follow the prompts to register your email and password.

3. **Send an email:**

   Use the `/give` command to retrieve and select a user to send an email.

4. **Message Handling:**

   The bot will guide you through each step, ensuring proper data collection and email sending.
