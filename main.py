from auraframes.aura import Aura

if __name__ == '__main__':
    aura = Aura()
    aura.login('username', 'password')
    aura.frame_api.get_frames()
