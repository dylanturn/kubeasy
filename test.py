from modulefinder import ModuleFinder

finder = ModuleFinder()
finder.run_script("kergiva.py")
for name, mod in finder.modules.items():
    print(name)