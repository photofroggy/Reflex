
import os

def __modules__():
    mods = {}
    for f in os.listdir('./reflex/rules'):
        if f in ('__init__.py', '__init__.pyc'):
            continue
        mod_name, ext = os.path.splitext(f)
        if not ext in '.pyc' or not ext:
            continue
        if not mod_name in mods.keys():
            mod = __import__('reflex.rules', fromlist=[mod_name])
            mods[mod_name] = getattr(mod, mod_name)
    return mods


# EOF
