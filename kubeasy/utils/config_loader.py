# Configuration defaults will be read here
def load_default_configuration(func):
    print("Something - decorator")
    func.asdf = "asdf"
    print(dir(func))

    print(vars(func))
    print(f"from decorator: {func.asdf}")
    return func


# Configuration required by admins will be read here
def load_enforced_configuration(**kwargs):
    pass


class ConfigLoader(object):

    def __init__(self):
        pass
