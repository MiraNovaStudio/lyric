def main() {
    dsk logfile = disk("run.log")

    exec("echo Build started") ->> logfile
    exec("echo Compiling...") ->> logfile
    exec("echo Done") ->> logfile

    logfile.close()

    str content
    dsk reader = disk("run.log")
    content <- reader
    reader.close()
    print(content)

    reader.delete()
}
