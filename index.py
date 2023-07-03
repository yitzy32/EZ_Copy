import os

def invalid_dir(path):
    if not os.path.isdir(path):
        print('Sorry. '+ path +' is not a valid directory')
        return True 

def get_total(source, dest, ext):
    totals = {}
    to_copy = set()
    to_skip = set()
    for file_name in os.listdir(source):
        if file_name.endswith(ext):
            to_copy.add(file_name)
    for file_name in os.listdir(dest):
        if file_name.endswith(ext):
            to_copy.discard(file_name)
            to_skip.add(file_name)
    totals['to_copy'] = len(to_copy)
    totals['to_skip'] = len(to_skip)
    return totals

def calc_percentage(val, totalVal):
    return str(int(val/totalVal * 100)) + "%"

def get_file_extensions(path):
    extension_set = set()
    for file_name in os.listdir(path):
        extension_set.add(file_name.split(".")[-1])
    extension_set.discard("DS_Store")
    return extension_set

def format_path(str):
    return str.replace("\\", "").strip()

def get_inputs(): 
    inputs = {}
    source = format_path(input('Please provide full path of folder to copy from\n'))
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
    ext = input(options)
    if ext not in extension_options:
        print('Sorry. '+ext+' is an invalid file extension.')
        return inputs
    dest = format_path(input('You chose to copy all '+ext+' files. \nNow please provide full path of folder to copy to\n'))
    if invalid_dir(dest): return inputs
    totals = get_total(source, dest, ext)
    if totals['to_copy'] == 0:
        print('No new files found to copy.')
        return inputs
    message = ''
    if totals['to_skip'] > 0:
        message += 'Found '+ str(totals['to_skip']) + ' files that already exist in ' + dest + '. Those files will be skipped.'
    message += '\nAre you sure you want to copy all '+str(totals['to_copy'])+' '+ext+' files from\n'+ source +'\nto \n' + dest +'? \n Enter Y/N\n'
    confirm = input(message)
    inputs["source"] = source
    inputs["ext"] = ext
    inputs["dest"] = dest
    inputs["total_copy"] = totals['to_copy']
    inputs["total_skip"] = totals['to_skip']
    inputs["confirm"] = confirm
    return inputs

def copy(inputs):
    source = inputs["source"]
    ext = inputs["ext"]
    dest = inputs["dest"]
    total_to_copy = inputs["total_copy"]
    total_copied, total_skipped = 0, 0
    for file_name in os.listdir(source):
        if file_name.endswith(ext):
            if os.path.exists(dest+'/'+file_name):
                total_skipped += 1
            else: 
                total_copied += 1
                print('Copying '+file_name+'. '+str(total_copied)+ ' of '+ str(total_to_copy)+' ('+calc_percentage(total_copied, total_to_copy)+' done)')
                os.popen('cp "'+source+'/'+file_name+ '" "' + dest+'/'+file_name+'"')

    print('All Done! \nCopied: '+ str(total_copied) +' files. Skipped: '+ str(total_skipped) +' files')

def process():
    inputs = get_inputs()
    if('confirm' not in inputs or inputs['confirm'].lower() == 'n'):
        print('Exiting.')
        return 
    if(inputs["confirm"].lower() == 'y'):
        copy(inputs)

process()
