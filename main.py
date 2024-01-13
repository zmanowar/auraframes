from auraframes.aura import Aura

if __name__ == '__main__':
    aura = Aura()
    aura.login()
    aura.frame_api.get_frames()

# TODO: Port cloning / dumping example from working main.