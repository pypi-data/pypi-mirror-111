import codecs
import random

SCALING_AUTO = -1

def get_random_id():
    return random.randint(1000000, 100000000)

class Application:
    def __init__(self, name):
        self.random_id = get_random_id()
        self.name = name
        self.scale = 1

    def scale_to(self, scale=SCALING_AUTO):
        if(scale < SCALING_AUTO or scale == 0):
            raise(f"Cannot set scaling to {scale}. Scaling must be 1 or greater")
        elif(scale == SCALING_AUTO):
            self.scale = random.randint(1, 1000)
        else:
            self.scale = scale
        return self

    def get_app_arn(self):
        return f"arn:aws:infinidash::{self.random_id}:{self.name}"

    def get_rescaled_instances(self):
        applications = list()

        for _ in range(1, self.scale):
            applications.append(Application(self.name))
        
        return applications


class InfinidashClient:
    def __init__(self):
        self.encrypted_key = ""

    def encrypt(self, key):
        self.encrypted_key = codecs.encode(key, "rot_13")
        return self

    def publish(self):
        return self

    def application(self, name):
        return Application(name)