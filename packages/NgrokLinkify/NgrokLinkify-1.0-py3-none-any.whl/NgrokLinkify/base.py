import configparser
import logging
from dataclasses import dataclass
from datetime import datetime
import argparse
import requests
from git import Repo
from telegram.ext import CommandHandler, Updater


@dataclass
class GithubPagesConfig:
    repo_path : str
    commit_comment: str
    pages_file_content: str

@dataclass
class TelegramConfig:
    telegram_bot_token : str
    telegram_success_msg :  str
    telegram_failure_msg :  str

@dataclass
class DefaultConfig:
    ngrok_url : str
    log_file : str

class base:
    """Use this class to expose your ngrok tunnnels in a easy to use way. You can either start a telegram bot to return current public urls or use github pages to redirect to the tunnel. You can setup this script as a systemd service to do this at every boot. 

    """
    git_config : GithubPagesConfig
    telegram_config : TelegramConfig
    default_config: DefaultConfig
    def get_public_urls(self):
        """Returns the public URLs for all the ngrok tunnels running on the current system

        Returns:
            list: list containing formatted string containing tunnel name and its public url
        """
        #TODO: change method signature to return list of dicts
        response = requests.get(self.default_config.ngrok_url)
        try:
            if response.status_code != 200:
                return None
            public_urls = []
            response = response.json()
            for tunnel in response.get('tunnels'):
                public_urls.append(tunnel.get('name')+ " : " + tunnel.get('public_url'))
            return public_urls
        except Exception:
            logging.error("Exception occured", exc_info=True)
            return None

    def telegram_url_command_handler(self, update, context):
        """Handler for the telegram bot. Returns current public URLS as a message
        """
        urls = self.get_public_urls()
        if urls:
            public_urls_string = "\n".join(urls)
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.telegram_success_msg.format(public_urls_string))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.telegram_failure_msg)

    def commit_URL_github_pages(self):
        """Gets the public URLs and commits them to github pages repo to enable redirection to the ngrok tunnel. Set the pages_file_content variable in GithubPagesConfig to modify the page content. 
        """
        try:
            public_urls = self.get_public_urls()
            repo = Repo(self.git_config.repo_path)
            repo.remotes.origin.pull()
            for x in public_urls:
                tunnel_name = x.split(":")[0]
                url = x.split(" : ")[1]
                file_name = self.git_config.repo_path +tunnel_name.strip()+".md"
                with open(file_name,"w+") as f:
                    file = self.git_config.pages_file_content.format(tunnel_name,url)
                    f.write(file)
                repo.index.add([file_name])
            repo.index.commit(self.git_config.commit_comment)
            origin = repo.remote(name='origin')
            origin.push()
        except Exception as e:
            logging.error("Exception occured", exc_info=True)

    def parse_config(self, file="./config.ini"):
        """Parse the configuration file

        Args:
            file (str, optional): Path to the configuration file. Defaults to "./config.ini".
        """
        config = configparser.RawConfigParser()
        config.read(file)
        if 'Default' in config:
            self.default_config = DefaultConfig(config['Default']['NgrokUrl'],config['Default']['LogFile'])
        if 'Git' in config:
            self.git_config = GithubPagesConfig(config['Git']['RepoPath'],config['Git']['CommitComment'],config['Git']['PagesContent'])
        if 'Telegram' in config:
            self.telegram_config = TelegramConfig(config['Telegram']['BotToken'],config['Telegram']['SuccessMsg'],config['Telegram']['FailureMsg'])

    def set_logger(self):
        """Set logger config
        """
        logging.basicConfig(filename=self.default_config.log_file, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    def init_telegram_bot(self):
        """Initialize the telegram bot
        """
        updater = Updater(token=self.telegram_config.telegram_bot_token, use_context=True)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('url', self.telegram_url_command_handler)
        dispatcher.add_handler(start_handler)
        updater.start_polling()

    def __init__(self, run_telegram_bot, update_github_pages, config_file = None) -> None:
        """Initialize the NgrokLinkify class

        Args:
            run_telegram_bot (boolean): Run the telegram bot or not
            update_github_pages (boolean): Update the github pages repo with redirect
            config_file (string, optional): configuration file location. Defaults to None.
        """
        if config_file:
            self.parse_config(config_file)
        self.set_logger()
        if update_github_pages:
            self.commit_URL_github_pages()
        if run_telegram_bot:
            self.init_telegram_bot()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A utility to expose your ngrok tunnels using Github Pages and/or a telegram bot")
    parser.add_argument("--config",default="./config.ini",help="Path to the configuration file")
    parser.add_argument("--runTelegram", default=True, help="True if you want the telegram bot to run" )
    parser.add_argument("--updateGithubPages", default=True, help="True if you want to expose your public URLs using redirection from github pages" )
    args = parser.parse_args()
    ngrok_linkify = base(args.runTelegram, args.updateGithubPages, args.config)