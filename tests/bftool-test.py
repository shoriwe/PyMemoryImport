import PyMemoryImport.import_zip


def main():
    zip_bytes = open("Modules/bftool.zip", "rb").read()
    module = PyMemoryImport.import_zip.import_zip_from_bytes("bftool", zip_bytes, False)
    print(tuple(filter(lambda n: not n.startswith("__"), vars(module.Process).keys())))
    print(len(tuple(filter(lambda n: not n.startswith("__"), vars(module.Process).keys()))))
    arguments = module.Arguments.Arguments(
        success_function=print,
        debug=True,
        function_=lambda x: len(x) > 1,
        wordlists_iterables={0: ["a", "ab"]}
    )
    runner = module.Runner.Runner()
    runner.run(arguments)


if __name__ == '__main__':
    main()
