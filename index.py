import os

def invalid_dir(path):
    if not os.path.isdir(path):
        print('Sorry. '+ path +' is not a valid directory')
        return True 

def get_total(folder, ext):
    count = 0
    for file_name in os.listdir(folder):
        if file_name.endswith(ext):
            count+=1
    return count
def calc_percentage(val, totalVal):
    return str(int(val/totalVal * 100)) + "%"

def get_file_extensions(path):
    extension_set = set()
    for file_name in os.listdir(path):
        extension_set.add(file_name.split(".")[-1])
    extension_set.discard("DS_Store")
    return extension_set

def get_inputs(): 
    inputs = {}
    source = raw_input('Please provide full path of folder to copy from\n').strip()
    if invalid_dir(source): return inputs
    extension_options = get_file_extensions(source)
    if len(extension_options) == 0:
        print('Sorry, No files to copy found..')
        return inputs
    else:
        options = 'Great. The following are the possible extensions to copy: '
        for ext in extension_options:
            options += ext
            options += ", "
        options += '\nPlease type bellow the extension you would like to copy.\n'
    ext = raw_input(options)
    if ext not in extension_options:
        print('Sorry. '+ext+' is an invalid file extension.')
        return inputs
    dest = raw_input('You chose to copy all '+ext+' files. \nNow please provide full path of folder to copy to\n').strip()
    if invalid_dir(dest): return inputs
    total = get_total(source, ext)
    confirm = raw_input('\nAre you sure you want to copy all '+str(total)+' '+ext+' files from\n'+ source +'\nto \n' + dest +'? \n Enter Y/N\n')
    inputs["source"] = source
    inputs["ext"] = ext
    inputs["dest"] = dest
    inputs["total"] = total
    inputs["confirm"] = confirm
    return inputs

def copy(inputs):
    source = inputs["source"]
    ext = inputs["ext"]
    dest = inputs["dest"]
    total = inputs["total"]
    total_copied, total_skipped = 0, 0
    for file_name in os.listdir(source):
        if file_name.endswith(ext):
            if os.path.exists(dest+'/'+file_name):
                print(file_name +' already exists in '+dest+' skipped copy.')
                total_skipped += 1
            else: 
                total_copied += 1
                print('Copying '+file_name+'. '+str(total_copied)+ ' of '+ str(total)+' ('+calc_percentage(total_copied, total)+' done)')
                os.popen('cp "'+source+'/'+file_name+ '" "' + dest+'/'+file_name+'"')

    print('All Done! \nCopied: '+ str(total_copied) +' files. Skipped: '+ str(total_skipped) +' files')

def process():
    inputs = get_inputs()
    if('confirm' not in inputs):
        print('Exiting.')
        return 
    if(inputs["confirm"].lower() == 'y'):
        copy(inputs)

process()
