import requests
from time import sleep

class Bumper(object):
    def __init__(self):
        super(Bumper, self).__init__()

        self._token = None

        self._channel_ids = open('channels.txt','r+').read().splitlines()

        self._cooldown = 1
        self._running = True

        self._msg = None

    def newFile(self, list, fileName):
        file = open(fileName + ".txt", "w+")
        file.truncate(0)

        for strip in list:
            file.write(strip + "\n")

        return

    def check_token(self):
        dc_status_check = requests.get('https://discord.com/api/v6/auth/login', headers = {'Authorization': self._token}).status_code

        if dc_status_check == 200:
            print('\n[' + RGB(158, 212, 155,'Success') + '] Token is working correctly!')
            return
        
        else:
            return "Invalid Token"



    def send_message(self,channel_id):
        send_status_code = requests.post('https://discord.com/api/v9/channels/%s/messages' %channel_id, headers = {'Authorization': self._token}, data={'content':self._msg}).status_code

        if send_status_code == 200:
            return 'success'

        else:
            return 'error'


    def start_loop(self):
        while self._running:
            time_to_sleep = self._cooldown * 60 * 60
            
            for channel_id in self._channel_ids:
                if self.send_message(channel_id) == 'success':
                    print('[' + RGB(158, 212, 155,'Success') + '] Sent Auto-Bump message to ' + channel_id)
                
                else:
                    try : 
                        self._channel_ids.remove(channel_id)
                        self.newFile(self._channel_ids,'channels')

                        print('[' + RGB(232, 60, 83,'Error') + '] Un-Able to Auto-Bump message to ' + channel_id)
                        print('[' + RGB(232, 60, 83,'Removed') + '] Channel ID: ' + channel_id + 'Exiting program.')

                    except : 
                        print('[' + RGB(232, 60, 83,'Error') + '] Un-Able to Auto-Bump message to ' + channel_id)
                        print('[' + RGB(232, 60, 83,'Error') + '] Un-Able to remove ' + channel_id + 'Exiting program.')
                        self._running = False
                        exit()

            print('[' + RGB(249, 252, 189,'Cooldown') + '] Sleeping for ' + str(self._cooldown) + ' Hour\s!\n')
            sleep(int(time_to_sleep))

def RGB(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

def Script():

    ab = Bumper()

    ab._msg = open("message.txt").read()

    print('[' + RGB(255, 166, 200,'x_x') + '] Made with love by grotesque <3\n')
    
    ab._token = input('[' + RGB(249, 252, 189,'>') + '] Token: ')

    if ab.check_token() == "Invalid Token":
        print('\n[' + RGB(232, 60, 83,'Failed') + '] Invalid Token!')
        exit()


    print('\n[' + RGB(255, 166, 200,'x_x') + '] Channels: ' + str(sum(1 for line in open('channels.txt'))))
    ab._cooldown = int(input('[' + RGB(255, 166, 200,'x_x') + '] Current Delay (Hour): '))

    input('\n[' + RGB(255, 166, 200,'x_x') + '] Press ENTER to Start: ')
    print('\n[' + RGB(255, 166, 200,'x_x') + '] Logs will show up below\n')
    ab.start_loop()

if __name__ == '__main__':
    Script()
